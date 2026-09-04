#!/usr/bin/env python3
"""Add bounded context and durable-memory artifacts to existing prodloop state."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--state-dir", help="State directory relative to project root or absolute path")
    parser.add_argument("--soft-limit-k", type=int, default=120)
    parser.add_argument("--checkpoint-percent", type=int, default=80)
    parser.add_argument("--checkpoint-interval-actions", type=int, default=8)
    parser.add_argument("--summary-max-chars", type=int, default=12000)
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


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    if args.soft_limit_k <= 0 or args.checkpoint_interval_actions <= 0:
        raise SystemExit("Context limits and intervals must be positive")
    if not 1 <= args.checkpoint_percent <= 100:
        raise SystemExit("Checkpoint percent must be between 1 and 100")
    if args.summary_max_chars < 1000:
        raise SystemExit("Summary max chars must be at least 1000")

    root = Path(args.project_root).resolve()
    delivery = resolve_delivery_dir(root, args.state_dir)
    state_path = delivery / "STATE.json"
    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    if not state_path.is_file() or not manifest_path.is_file():
        raise SystemExit("Existing delivery state is missing STATE.json or DELIVERY_MANIFEST.yaml")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    manifest = manifest_path.read_text(encoding="utf-8")
    context_defaults = {
        "context_checkpoint_count": 0,
        "last_context_checkpoint_at": None,
        "material_actions_since_checkpoint": 0,
        "context_checkpoint_due": False,
        "context_checkpoint_reasons": [],
    }
    state_changed = any(key not in state for key in context_defaults)
    manifest_changed = "\ncontext_management:\n" not in f"\n{manifest}"
    if state_changed or manifest_changed:
        state_backup = delivery / "STATE.before-context-enable.json"
        manifest_backup = delivery / "DELIVERY_MANIFEST.before-context-enable.yaml"
        if not state_backup.exists():
            shutil.copy2(state_path, state_backup)
        if not manifest_backup.exists():
            shutil.copy2(manifest_path, manifest_backup)
    if state_changed:
        for key, value in context_defaults.items():
            state.setdefault(key, value)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if manifest_changed:
        suffix = "" if manifest.endswith("\n") else "\n"
        manifest += (
            suffix
            + "context_management:\n"
            + f"  soft_limit_k: {args.soft_limit_k}\n"
            + f"  checkpoint_at_percent: {args.checkpoint_percent}\n"
            + f"  checkpoint_interval_actions: {args.checkpoint_interval_actions}\n"
            + f"  summary_max_chars: {args.summary_max_chars}\n"
            + "  external_memory: candidate-only\n"
        )
        manifest_path.write_text(manifest, encoding="utf-8")

    next_action = str(state.get("next_action", "")).strip() or "Repair missing STATE.json.next_action"
    created = []
    if write_if_missing(
        delivery / "CONTEXT.md",
        "# Working Context\n\n"
        "## Objective And Scope\n\n"
        "TODO: Reconstruct from the delivery manifest and current product contract.\n\n"
        "## Current State And Gates\n\n"
        f"TODO: Stage is {state.get('current_stage', 'unknown')}; reconstruct all gate status from STATE.json.\n\n"
        "## Frozen Decisions And Assumptions\n\n"
        "TODO: Read DECISIONS.md and ASSUMPTIONS.md; summarize only currently applicable entries.\n\n"
        "## Active Slice And Changed Paths\n\n"
        "TODO: Reconstruct from STATE.json, PROGRESS.md, traceability, and the worktree.\n\n"
        "## Verification And Evidence\n\n"
        "TODO: Reconstruct current pass, fail, blocked, and not-run evidence before checkpointing.\n\n"
        "## Open Risks, Blocks, And Unknowns\n\n"
        "TODO: Read BLOCKED.md and current-stage artifacts before checkpointing.\n\n"
        "## Exact Next Action\n\n"
        f"{next_action}\n",
    ):
        created.append("CONTEXT.md")
    if write_if_missing(
        delivery / "CONTEXT_HISTORY.md",
        "# Context History\n\n"
        "| Checkpoint | Time | Reason | Stage | Revision | Characters |\n"
        "|---|---|---|---|---|---|\n",
    ):
        created.append("CONTEXT_HISTORY.md")
    if write_if_missing(
        delivery / "MEMORY_CANDIDATES.md",
        "# Memory Candidates\n\n"
        "Candidate-only. Promotion outside this repository requires explicit authority.\n\n"
        "| ID | Reusable Lesson | Evidence | Scope | Confidence | Owner | Review Date | Status |\n"
        "|---|---|---|---|---|---|---|---|\n",
    ):
        created.append("MEMORY_CANDIDATES.md")

    print(json.dumps({
        "state_dir": str(delivery),
        "state_changed": state_changed,
        "manifest_changed": manifest_changed,
        "created": created,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
