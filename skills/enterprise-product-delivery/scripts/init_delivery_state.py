#!/usr/bin/env python3
"""Initialize non-destructive delivery state in a software project."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


MODES = {"greenfield", "feature", "workflow-change", "integration", "migration", "remediation"}
PROFILES = {"Q0", "Q1", "Q2", "Q3"}


def write_new(path: Path, content: str) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--name", required=True)
    parser.add_argument("--mode", choices=sorted(MODES), required=True)
    parser.add_argument("--quality", choices=sorted(PROFILES), required=True)
    parser.add_argument("--objective", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")
    if root in {Path("/"), Path.home().resolve()}:
        raise SystemExit("Refusing to initialize a broad system directory")

    delivery = root / ".codex" / "delivery"
    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    state_path = delivery / "STATE.json"
    if manifest_path.exists() or state_path.exists():
        raise SystemExit(f"Delivery state already exists: {delivery}")

    delivery.mkdir(parents=True, exist_ok=True)
    (delivery / "evidence").mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    manifest = f"""schema_version: 1
project:
  name: {quote(args.name)}
  mode: {quote(args.mode)}
  quality_profile: {quote(args.quality)}
  objective: {quote(args.objective)}
  target_users: []
  in_scope: []
  out_of_scope: []
autonomy:
  reversible_product_decisions: allowed
  reversible_technical_decisions: allowed
  dependency_changes: conditional
  schema_migrations: conditional
  external_writes: denied
  production_deploy: denied
  destructive_actions: denied
budgets:
  max_delivery_cycles: 3
  max_failed_attempts_per_check: 3
  time_limit: ""
  cost_limit: ""
required_gates: [G0, G1, G2, G3, G4, G5, G6, G7, G8]
"""
    state = {
        "schema_version": 1,
        "project_mode": args.mode,
        "quality_profile": args.quality,
        "current_stage": "S0_INTAKE",
        "gate_status": {f"G{i}": "pending" for i in range(9)},
        "active_slice": None,
        "blocked_items": [],
        "failed_attempts": {},
        "invalidated_artifacts": [],
        "last_verified_at": None,
        "next_action": "Complete the autonomy contract and G0 evidence",
        "created_at": now,
        "updated_at": now,
    }

    write_new(manifest_path, manifest)
    write_new(state_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    write_new(delivery / "ASSUMPTIONS.md", "# Assumptions\n\n| ID | Class | Claim | Evidence | Validation | Status |\n|---|---|---|---|---|---|\n")
    write_new(delivery / "DECISIONS.md", "# Decisions\n\n")
    write_new(delivery / "PROGRESS.md", f"# Progress\n\n- {now}: Delivery state initialized at S0.\n")
    write_new(delivery / "BLOCKED.md", "# Blocked\n\nNo blocked items.\n")
    write_new(delivery / "TRACEABILITY.md", "# Traceability\n\n| ID | Outcome | Product Rule | Design | Implementation | Positive Test | Negative Test | Evidence | Status |\n|---|---|---|---|---|---|---|---|---|\n")
    print(delivery)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
