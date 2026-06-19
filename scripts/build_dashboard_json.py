#!/usr/bin/env python3

import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path


ROOT = Path("/Users/macminiagent/Documents/projects/biz-acquisition-tracker")
CSV_PATH = ROOT / "data" / "candidates.csv"
OUT_PATH = ROOT / "app" / "public" / "data" / "dashboard.json"
UNDERWRITING_DIR = ROOT / "data" / "underwriting"
SBA_PRIME_RATE = 0.0675
SBA_EQUITY_INJECTION = 0.10
SBA_TERM_YEARS = 10


def load_candidates():
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_underwriting_details():
    details = {}
    for path in UNDERWRITING_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        sections = {}
        current = None

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if line.startswith("## "):
                current = line[3:].strip()
                sections[current] = []
                continue
            if current:
                sections[current].append(raw_line.rstrip())

        def clean_lines(name):
            return [line.strip() for line in sections.get(name, []) if line.strip()]

        def section_text(name):
            lines = clean_lines(name)
            return " ".join(lines) if lines else ""

        def section_bullets(name):
            lines = clean_lines(name)
            return [line[2:].strip() for line in lines if line.startswith("- ")]

        details[path.stem] = {
            "overview": section_bullets("Overview"),
            "why_it_fits": section_text("Why It Fits"),
            "revenue_and_cash_flow_view": section_bullets("Revenue And Cash Flow View"),
            "key_risks": section_text("Key Risks"),
            "financing_view": section_bullets("Financing View"),
            "missing_facts": section_bullets("Missing Facts"),
            "preliminary_verdict": section_bullets("Preliminary Verdict"),
        }
    return details


def parse_money(value):
    if not value:
        return None
    cleaned = value.strip().upper().replace("$", "").replace(",", "")
    multiplier = 1
    if cleaned.endswith("M"):
        multiplier = 1_000_000
        cleaned = cleaned[:-1]
    elif cleaned.endswith("K"):
        multiplier = 1_000
        cleaned = cleaned[:-1]
    try:
        return float(cleaned) * multiplier
    except ValueError:
        return None


def format_money(value):
    if value is None:
        return "-"
    rounded = int(round(value))
    return f"${rounded:,.0f}"


def sba_rate_for_loan_amount(loan_amount):
    if loan_amount is None:
        return None
    if loan_amount <= 50_000:
        return SBA_PRIME_RATE + 0.065
    if loan_amount <= 250_000:
        return SBA_PRIME_RATE + 0.06
    if loan_amount <= 350_000:
        return SBA_PRIME_RATE + 0.045
    return SBA_PRIME_RATE + 0.03


def monthly_payment(principal, annual_rate, term_years):
    if not principal or annual_rate is None or not term_years:
        return None
    months = term_years * 12
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return principal / months
    factor = math.pow(1 + monthly_rate, months)
    return principal * ((monthly_rate * factor) / (factor - 1))


def build_sba_view(row):
    purchase_price = parse_money(row.get("bestimate"))
    annual_cash_flow = parse_money(row.get("cash_flow"))
    if purchase_price is None:
        return {}

    equity_injection = purchase_price * SBA_EQUITY_INJECTION
    loan_amount = purchase_price - equity_injection
    interest_rate = sba_rate_for_loan_amount(loan_amount)
    estimated_monthly_payment = monthly_payment(loan_amount, interest_rate, SBA_TERM_YEARS)
    annual_debt_service = estimated_monthly_payment * 12 if estimated_monthly_payment is not None else None
    dscr = (annual_cash_flow / annual_debt_service) if annual_cash_flow and annual_debt_service else None

    if dscr is None:
        feasibility = "unknown"
    elif dscr >= 1.25:
        feasibility = "looks serviceable"
    elif dscr >= 1.0:
        feasibility = "tight"
    else:
        feasibility = "stretched"

    return {
        "purchase_price_estimate": format_money(purchase_price),
        "equity_injection": format_money(equity_injection),
        "loan_amount": format_money(loan_amount),
        "interest_rate": f"{interest_rate * 100:.2f}%" if interest_rate is not None else "-",
        "term_years": SBA_TERM_YEARS,
        "monthly_payment": format_money(estimated_monthly_payment),
        "annual_debt_service": format_money(annual_debt_service),
        "cash_flow_coverage": f"{dscr:.2f}x" if dscr is not None else "-",
        "feasibility": feasibility,
    }


def build_summary(rows):
    summary = {
        "total": len(rows),
        "qualified": 0,
        "screening": 0,
        "contacted": 0,
        "diligence": 0,
        "highPriority": 0,
        "underwritingPending": 0,
        "researchPending": 0,
    }
    for row in rows:
        status = row.get("status", "").strip()
        priority = row.get("priority", "").strip()
        underwriting_status = row.get("underwriting_status", "").strip()
        research_status = row.get("research_status", "").strip()

        if status in summary:
            summary[status] += 1
        if priority == "high":
            summary["highPriority"] += 1
        if underwriting_status in ("", "pending"):
            summary["underwritingPending"] += 1
        if research_status in ("", "pending"):
            summary["researchPending"] += 1
    return summary


def sort_key(row):
    priority_rank = {"high": 0, "medium": 1, "low": 2}
    status_rank = {"qualified": 0, "contacted": 1, "screening": 2, "diligence": 3, "sourced": 4, "pass": 5}
    return (
        priority_rank.get(row.get("priority", ""), 9),
        status_rank.get(row.get("status", ""), 9),
        -(int(row.get("years_in_business", "0") or 0)),
    )


def main():
    rows = load_candidates()
    underwriting_details = load_underwriting_details()
    ordered = sorted(rows, key=sort_key)

    for row in ordered:
        slug = slugify(row.get("name", ""))
        row["underwriting_details"] = underwriting_details.get(slug, {})
        row["sba_loan_view"] = build_sba_view(row)

    payload = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "loanAssumptions": {
            "program": "Illustrative SBA 7(a) acquisition scenario",
            "primeRate": "6.75%",
            "equityInjection": "10%",
            "termYears": 10,
            "rateMethod": "Uses SBA variable-rate ceilings by loan size as a conservative estimate.",
            "asOf": "2026-06-19",
        },
        "summary": build_summary(rows),
        "candidates": ordered,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
