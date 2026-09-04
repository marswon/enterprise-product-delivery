#!/usr/bin/env python3
"""Track material actions and decide whether a prodloop context checkpoint is due."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"
EVENTS = {"material-action", "gate", "slice", "long-output", "handoff", "completion", "manual"}
BOUNDARY_EVENTS = EVENTS - {"material-action"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--state-dir", help="State directory relative to project root or absolute path")
    parser.add_argument("--event", choices=sorted(EVENTS), default="material-action")
    parser.add_argument("--reported-context-k", type=float)
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


def read_context_config(manifest_path: Path) -> tuple[int, int, int]:
    values = {
        "soft_limit_k": 120,
        "checkpoint_at_percent": 80,
        "checkpoint_interval_actions": 8,
    }
    in_context_block = False
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line == "context_management:":
            in_context_block = True
            continue
        if in_context_block and line and not line.startswith(" "):
            break
        if in_context_block and ":" in line:
            key, raw = (part.strip() for part in line.split(":", 1))
            if key in values:
                try:
                    values[key] = int(raw)
                except ValueError:
                    raise SystemExit(f"context_management.{key} must be an integer") from None
    if values["soft_limit_k"] <= 0 or values["checkpoint_interval_actions"] <= 0:
        raise SystemExit("Context limits and intervals must be positive")
    if not 1 <= values["checkpoint_at_percent"] <= 100:
        raise SystemExit("Context checkpoint percent must be between 1 and 100")
    return (
        values["soft_limit_k"],
        values["checkpoint_at_percent"],
        values["checkpoint_interval_actions"],
    )


def main() -> int:
    args = parse_args()
    if args.reported_context_k is not None and args.reported_context_k < 0:
        raise SystemExit("reported-context-k cannot be negative")
    root = Path(args.project_root).resolve()
    delivery = resolve_delivery_dir(root, args.state_dir)
    state_path = delivery / "STATE.json"
    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    if not state_path.is_file() or not manifest_path.is_file():
        raise SystemExit("Context management is not initialized")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    soft_limit_k, checkpoint_percent, interval = read_context_config(manifest_path)
    actions = state.get("material_actions_since_checkpoint", 0)
    if not isinstance(actions, int) or isinstance(actions, bool) or actions < 0:
        raise SystemExit("material_actions_since_checkpoint must be a non-negative integer")
    if args.event == "material-action":
        actions += 1

    raw_reasons = state.get("context_checkpoint_reasons", [])
    if not isinstance(raw_reasons, list) or not all(isinstance(item, str) and item for item in raw_reasons):
        raise SystemExit("context_checkpoint_reasons must be a list of non-empty strings")
    reasons = set(raw_reasons)
    threshold_k = soft_limit_k * checkpoint_percent / 100
    if actions >= interval:
        reasons.add("action-interval")
    if args.reported_context_k is not None and args.reported_context_k >= threshold_k:
        reasons.add("soft-limit")
    if args.event in BOUNDARY_EVENTS:
        reasons.add(args.event)

    now = datetime.now(timezone.utc).isoformat()
    state["material_actions_since_checkpoint"] = actions
    state["context_checkpoint_due"] = bool(reasons)
    state["context_checkpoint_reasons"] = sorted(reasons)
    state["updated_at"] = now
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "checkpoint_due": bool(reasons),
        "reasons": sorted(reasons),
        "material_actions_since_checkpoint": actions,
        "action_interval": interval,
        "reported_context_k": args.reported_context_k,
        "checkpoint_threshold_k": threshold_k,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
