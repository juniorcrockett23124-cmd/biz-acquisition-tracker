#!/usr/bin/env python3

import csv
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path("/Users/macminiagent/Documents/projects/biz-acquisition-tracker")
CSV_PATH = ROOT / "data" / "candidates.csv"
OUT_PATH = ROOT / "app" / "public" / "data" / "dashboard.json"
UNDERWRITING_DIR = ROOT / "data" / "underwriting"


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

    payload = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "summary": build_summary(rows),
        "candidates": ordered,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
