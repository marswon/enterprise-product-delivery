#!/usr/bin/env python3
"""Validate prodloop delivery state and gate ordering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STAGES = [
    "S0_INTAKE", "S1_DISCOVERY", "S2_PRODUCT_DEFINITION", "S3_SOLUTION_DESIGN",
    "S4_DELIVERY_PLANNING", "S5_IMPLEMENTATION", "S6_INDEPENDENT_VERIFICATION",
    "S7_RELEASE_READINESS", "S8_DELIVERY", "S9_OUTCOME_REVIEW",
]
SPECIAL_STAGES = {"BLOCKED", "REWORK", "STOPPED"}
GATE_VALUES = {"pending", "passed", "failed", "invalidated", "not_required"}
MODES = {"greenfield", "feature", "workflow-change", "integration", "migration", "remediation"}
PROFILES = {"Q0", "Q1", "Q2", "Q3"}
CONTEXTS = {"greenfield", "brownfield"}
INTERFACE_SCOPES = {"undetermined", "in-scope", "out-of-scope"}
SCHEMA_VERSIONS = {1, 2, 3}
DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"
BROWNFIELD_ARTIFACTS = [
    "CURRENT_SYSTEM_BASELINE.md",
    "SYSTEM_MAP.md",
    "BEHAVIOR_CONTRACT.md",
    "CHANGE_IMPACT.md",
    "REGRESSION_SCOPE.md",
    "TECH_DEBT_BOUNDARY.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--state-dir", help="State directory relative to project root or absolute path")
    return parser.parse_args()


def resolve_delivery_dir(root: Path, explicit: str | None) -> tuple[Path | None, list[str]]:
    if explicit:
        path = Path(explicit).expanduser()
        delivery = path.resolve() if path.is_absolute() else (root / path).resolve()
        try:
            delivery.relative_to(root)
        except ValueError:
            return None, [f"State directory must be inside project root: {delivery}"]
        return delivery, []

    candidates = [root / DEFAULT_STATE_DIR, root / LEGACY_STATE_DIR]
    existing = [path for path in candidates if path.exists()]
    if len(existing) > 1:
        return None, [f"Multiple delivery state directories exist: {', '.join(str(path) for path in existing)}"]
    return (existing[0] if existing else candidates[0]), []


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    delivery, errors = resolve_delivery_dir(root, args.state_dir)
    if delivery is None:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    state_path = delivery / "STATE.json"
    if not (delivery / "DELIVERY_MANIFEST.yaml").is_file():
        errors.append("Missing DELIVERY_MANIFEST.yaml")
    if not state_path.is_file():
        errors.append("Missing STATE.json")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [f"Invalid STATE.json: {exc}"]}, ensure_ascii=False, indent=2))
        return 1

    schema_version = state.get("schema_version")
    if schema_version not in SCHEMA_VERSIONS:
        errors.append(f"schema_version must be one of {sorted(SCHEMA_VERSIONS)}")
    context = state.get("project_context")
    if schema_version in {2, 3} and context not in CONTEXTS:
        errors.append("project_context is invalid")
    if state.get("project_mode") not in MODES:
        errors.append("project_mode is invalid")
    if state.get("quality_profile") not in PROFILES:
        errors.append("quality_profile is invalid")
    stage = state.get("current_stage")
    if stage not in set(STAGES) | SPECIAL_STAGES:
        errors.append("current_stage is invalid")

    gates = state.get("gate_status")
    if not isinstance(gates, dict):
        errors.append("gate_status must be an object")
        gates = {}
    for index in range(9):
        gate = f"G{index}"
        if gate not in gates:
            errors.append(f"Missing {gate}")
        elif gates[gate] not in GATE_VALUES:
            errors.append(f"Invalid status for {gate}: {gates[gate]}")

    interface_scope = state.get("interface_scope")
    if schema_version == 3:
        if interface_scope not in INTERFACE_SCOPES:
            errors.append("interface_scope is invalid")
        elif gates.get("G0") == "passed" and interface_scope == "undetermined":
            errors.append("G0 passed but interface_scope is undetermined")

    if stage in STAGES:
        for index in range(min(STAGES.index(stage), 9)):
            gate = f"G{index}"
            if gates.get(gate) not in {"passed", "not_required"}:
                errors.append(f"{stage} requires {gate} to be passed or not_required")
    if stage == "BLOCKED" and not state.get("blocked_items"):
        errors.append("BLOCKED state requires a blocked_items entry")
    if not isinstance(state.get("next_action"), str) or not state.get("next_action", "").strip():
        errors.append("next_action must be a non-empty string")

    for filename in ["ASSUMPTIONS.md", "DECISIONS.md", "PROGRESS.md", "BLOCKED.md", "TRACEABILITY.md"]:
        if not (delivery / filename).is_file():
            errors.append(f"Missing {filename}")

    if schema_version in {2, 3} and context == "brownfield":
        for filename in BROWNFIELD_ARTIFACTS:
            artifact = delivery / filename
            if not artifact.is_file():
                errors.append(f"Missing brownfield artifact: {filename}")
            elif gates.get("G1") == "passed" and "Status: complete" not in artifact.read_text(encoding="utf-8"):
                errors.append(f"G1 passed but brownfield artifact is incomplete: {filename}")

    if schema_version == 3:
        for filename in ["UI_CONTRACT.md", "UI_VERIFICATION.md"]:
            if not (delivery / filename).is_file():
                errors.append(f"Missing {filename}")
        if interface_scope == "in-scope":
            ui_contract = delivery / "UI_CONTRACT.md"
            ui_verification = delivery / "UI_VERIFICATION.md"
            if gates.get("G3") == "passed" and ui_contract.is_file():
                if "Status: complete" not in ui_contract.read_text(encoding="utf-8"):
                    errors.append("G3 passed but UI_CONTRACT.md is incomplete")
            if gates.get("G6") == "passed" and ui_verification.is_file():
                if "Status: complete" not in ui_verification.read_text(encoding="utf-8"):
                    errors.append("G6 passed but UI_VERIFICATION.md is incomplete")

    result = {"valid": not errors, "state_dir": str(delivery), "stage": stage, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
