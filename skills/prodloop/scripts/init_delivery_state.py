#!/usr/bin/env python3
"""Initialize non-destructive delivery state in a software project."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


MODES = {"greenfield", "feature", "workflow-change", "integration", "migration", "remediation"}
PROFILES = {"Q0", "Q1", "Q2", "Q3"}
CONTEXTS = {"greenfield", "brownfield"}
INTERFACE_SCOPES = {"undetermined", "in-scope", "out-of-scope"}
DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"
BROWNFIELD_ARTIFACTS = {
    "CURRENT_SYSTEM_BASELINE.md": "# Current System Baseline",
    "SYSTEM_MAP.md": "# System Map",
    "BEHAVIOR_CONTRACT.md": "# Behavior Contract",
    "CHANGE_IMPACT.md": "# Change Impact",
    "REGRESSION_SCOPE.md": "# Regression Scope",
    "TECH_DEBT_BOUNDARY.md": "# Tech Debt Boundary",
}


def write_new(path: Path, content: str) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--name", required=True)
    parser.add_argument("--context", choices=sorted(CONTEXTS))
    parser.add_argument("--mode", choices=sorted(MODES), required=True)
    parser.add_argument("--quality", choices=sorted(PROFILES), required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument(
        "--interface-scope",
        choices=sorted(INTERFACE_SCOPES),
        default="undetermined",
        help="Whether this delivery adds or changes a human-facing interface",
    )
    parser.add_argument(
        "--state-dir",
        help=f"State directory relative to project root or absolute path (default: {DEFAULT_STATE_DIR})",
    )
    return parser.parse_args()


def resolve_explicit_state_dir(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")
    if root in {Path("/"), Path.home().resolve()}:
        raise SystemExit("Refusing to initialize a broad system directory")

    default_delivery = root / DEFAULT_STATE_DIR
    legacy_delivery = root / LEGACY_STATE_DIR
    if args.state_dir:
        delivery = resolve_explicit_state_dir(root, args.state_dir)
    else:
        delivery = default_delivery

    try:
        delivery.relative_to(root)
    except ValueError:
        raise SystemExit(f"State directory must be inside project root: {delivery}") from None

    existing = {path for path in (default_delivery, legacy_delivery, delivery) if path.exists()}
    if existing:
        joined = ", ".join(str(path) for path in sorted(existing))
        raise SystemExit(f"Delivery state already exists: {joined}")

    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    state_path = delivery / "STATE.json"

    delivery.mkdir(parents=True, exist_ok=True)
    (delivery / "evidence").mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    context = args.context or ("greenfield" if args.mode == "greenfield" else "brownfield")
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    manifest = f"""schema_version: 3
project:
  name: {quote(args.name)}
  context: {quote(context)}
  mode: {quote(args.mode)}
  quality_profile: {quote(args.quality)}
  objective: {quote(args.objective)}
  target_users: []
  in_scope: []
  out_of_scope: []
experience:
  interface_scope: {quote(args.interface_scope)}
  primary_component_system: ""
  visual_references: []
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
        "schema_version": 3,
        "project_context": context,
        "project_mode": args.mode,
        "quality_profile": args.quality,
        "interface_scope": args.interface_scope,
        "current_stage": "S0_INTAKE",
        "gate_status": {f"G{i}": "pending" for i in range(9)},
        "active_slice": None,
        "blocked_items": [],
        "failed_attempts": {},
        "invalidated_artifacts": [],
        "last_verified_at": None,
        "next_action": (
            "Complete the autonomy contract and G0 evidence, then perform brownfield takeover"
            if context == "brownfield"
            else "Complete the autonomy contract and G0 evidence"
        ),
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
    ui_status = "not_required" if args.interface_scope == "out-of-scope" else "pending"
    write_new(
        delivery / "UI_CONTRACT.md",
        "# UI Contract\n\n"
        f"Status: {ui_status}\n\n"
        "## Context And Critical Tasks\n\n"
        "## Information Architecture And Business Patterns\n\n"
        "## States, Permissions, And Recovery\n\n"
        "## Tables, Forms, And Data Density\n\n"
        "## Responsive And Accessibility Constraints\n\n"
        "## Component System And Visual Direction\n\n"
        "## Representative Fixtures And Verification Plan\n",
    )
    write_new(
        delivery / "UI_VERIFICATION.md",
        "# UI Verification\n\n"
        f"Status: {ui_status}\n\n"
        "## Candidate, Environment, And Checker\n\n"
        "## Task And State Evidence\n\n"
        "## Viewports, Input, And Accessibility Evidence\n\n"
        "## Visual Consistency And Data Density Evidence\n\n"
        "## Blocking Defects, Accepted Risks, And Unverified Areas\n",
    )
    if context == "brownfield":
        for filename, heading in BROWNFIELD_ARTIFACTS.items():
            write_new(delivery / filename, f"{heading}\n\nStatus: pending\n")
    print(delivery)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
