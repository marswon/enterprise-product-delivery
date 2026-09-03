#!/usr/bin/env python3
"""Add data-visualization scope and gate artifacts to existing prodloop state."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"
VISUALIZATION_SCOPES = {"in-scope", "out-of-scope"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--state-dir", help="State directory relative to project root or absolute path")
    parser.add_argument("--visualization-scope", choices=sorted(VISUALIZATION_SCOPES), required=True)
    return parser.parse_args()


def resolve_delivery_dir(root: Path, explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        delivery = path.resolve() if path.is_absolute() else (root / path).resolve()
        try:
            delivery.relative_to(root)
        except ValueError:
            raise SystemExit(f"State directory must be inside project root: {delivery}") from None
        return delivery

    existing = [path for path in (root / DEFAULT_STATE_DIR, root / LEGACY_STATE_DIR) if path.exists()]
    if len(existing) > 1:
        raise SystemExit(f"Multiple delivery state directories exist: {', '.join(str(path) for path in existing)}")
    if not existing:
        raise SystemExit("No existing prodloop delivery state found")
    return existing[0]


def set_manifest_scope(content: str, scope: str) -> str:
    lines = content.splitlines()
    experience_index = next((index for index, line in enumerate(lines) if line == "experience:"), None)
    if experience_index is None:
        suffix = "" if content.endswith("\n") else "\n"
        return content + suffix + f'experience:\n  visualization_scope: "{scope}"\n'

    end = next(
        (index for index in range(experience_index + 1, len(lines)) if lines[index] and not lines[index].startswith(" ")),
        len(lines),
    )
    for index in range(experience_index + 1, end):
        if lines[index].lstrip().startswith("visualization_scope:"):
            lines[index] = f'  visualization_scope: "{scope}"'
            return "\n".join(lines) + "\n"
    lines.insert(experience_index + 1, f'  visualization_scope: "{scope}"')
    return "\n".join(lines) + "\n"


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    delivery = resolve_delivery_dir(root, args.state_dir)
    state_path = delivery / "STATE.json"
    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    if not state_path.is_file() or not manifest_path.is_file():
        raise SystemExit("Existing delivery state is missing STATE.json or DELIVERY_MANIFEST.yaml")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    changed = state.get("visualization_scope") != args.visualization_scope
    if changed:
        state_backup = delivery / "STATE.before-data-vis-enable.json"
        manifest_backup = delivery / "DELIVERY_MANIFEST.before-data-vis-enable.yaml"
        if not state_backup.exists():
            shutil.copy2(state_path, state_backup)
        if not manifest_backup.exists():
            shutil.copy2(manifest_path, manifest_backup)
        state["visualization_scope"] = args.visualization_scope
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = set_manifest_scope(manifest_path.read_text(encoding="utf-8"), args.visualization_scope)
        manifest_path.write_text(manifest, encoding="utf-8")

    status = "pending" if args.visualization_scope == "in-scope" else "not_required"
    created = []
    contract = delivery / "DATA_VIS_CONTRACT.md"
    if write_if_missing(
        contract,
        "# Data Visualization Contract\n\n"
        f"Status: {status}\n\n"
        "## Audience, Decision, And Action\n\n"
        "## Metric Definitions, Sources, And Reconciliation\n\n"
        "## Chart Choices, Alternatives, And Encoding Rules\n\n"
        "## Filters, Drill-Down, Permissions, And Exports\n\n"
        "## Missing, Stale, Partial, And Failed Data\n\n"
        "## Accessibility, Responsive Behavior, And Performance\n\n"
        "## Representative Fixtures And Verification Plan\n",
    ):
        created.append(contract.name)
    verification = delivery / "DATA_VIS_VERIFICATION.md"
    if write_if_missing(
        verification,
        "# Data Visualization Verification\n\n"
        f"Status: {status}\n\n"
        "## Candidate, Environment, And Independent Checker\n\n"
        "## Source Reconciliation And Metric Fixtures\n\n"
        "## Scales, Units, Labels, Color, And Extreme Values\n\n"
        "## Filters, Drill-Down, Permissions, And Failure States\n\n"
        "## Browser, Responsive, Accessibility, And Performance Evidence\n\n"
        "## Blocking Defects, Accepted Risks, And Unverified Areas\n",
    ):
        created.append(verification.name)

    print(json.dumps({
        "state_dir": str(delivery),
        "visualization_scope": args.visualization_scope,
        "state_changed": changed,
        "created": created,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
