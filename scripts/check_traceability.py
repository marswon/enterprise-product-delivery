#!/usr/bin/env python3
"""Check the delivery traceability Markdown table for structural gaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED = ["ID", "Outcome", "Product Rule", "Design", "Implementation", "Positive Test", "Negative Test", "Evidence", "Status"]
STATUSES = {"planned", "in_progress", "verified", "blocked", "deferred", "out_of_scope"}


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--require-complete", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.project_root).resolve() / ".codex" / "delivery" / "TRACEABILITY.md"
    errors: list[str] = []
    if not path.is_file():
        print(json.dumps({"valid": False, "errors": [f"Missing {path}"]}, ensure_ascii=False, indent=2))
        return 1

    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.lstrip().startswith("|")]
    if len(lines) < 2:
        errors.append("Traceability table header and separator are required")
        rows: list[list[str]] = []
    else:
        if cells(lines[0]) != EXPECTED:
            errors.append(f"Unexpected header: {cells(lines[0])}")
        rows = [cells(line) for line in lines[2:]]

    seen: set[str] = set()
    for number, row in enumerate(rows, start=1):
        if len(row) != len(EXPECTED):
            errors.append(f"Row {number} has {len(row)} cells; expected {len(EXPECTED)}")
            continue
        item_id, outcome, rule, design, implementation, positive, negative, evidence, status = row
        label = item_id or f"Row {number}"
        if not item_id:
            errors.append(f"Row {number} has no ID")
        elif item_id in seen:
            errors.append(f"Duplicate ID: {item_id}")
        seen.add(item_id)
        if status not in STATUSES:
            errors.append(f"{label} has invalid status: {status}")
        if not outcome or not rule:
            errors.append(f"{label} is missing outcome or product rule")
        if args.require_complete and status == "verified":
            missing = [name for name, value in [("Design", design), ("Implementation", implementation), ("Positive Test", positive), ("Negative Test", negative), ("Evidence", evidence)] if not value]
            if missing:
                errors.append(f"{label} is verified but missing: {', '.join(missing)}")
        if args.require_complete and status in {"planned", "in_progress", "blocked"}:
            errors.append(f"{label} is not in a terminal delivery status: {status}")
    if args.require_complete and not rows:
        errors.append("Complete delivery requires at least one traceability row")

    result = {"valid": not errors, "rows": len(rows), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
