#!/usr/bin/env python3

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path("/Users/macminiagent/Documents/projects/biz-acquisition-tracker")
CSV_PATH = ROOT / "data" / "candidates.csv"
OUT_PATH = ROOT / "app" / "public" / "data" / "dashboard.json"


def load_candidates():
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
    ordered = sorted(rows, key=sort_key)
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
