#!/usr/bin/env python3
"""Validate and record a bounded prodloop context checkpoint."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STATE_DIR = ".prodloop"
LEGACY_STATE_DIR = ".codex/delivery"
REASONS = {"soft-limit", "action-interval", "gate", "slice", "before-compaction", "handoff", "completion", "manual"}
RUNTIMES = {"codex", "kimi", "other"}
COMPACTION_MODES = {"automatic", "command", "none", "unavailable"}
REQUIRED_SECTIONS = [
    "Objective And Scope",
    "Current State And Gates",
    "Frozen Decisions And Assumptions",
    "Active Slice And Changed Paths",
    "Verification And Evidence",
    "Open Risks, Blocks, And Unknowns",
    "Exact Next Action",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--state-dir", help="State directory relative to project root or absolute path")
    parser.add_argument("--reason", choices=sorted(REASONS), required=True)
    parser.add_argument("--revision", default="unknown")
    parser.add_argument("--runtime", choices=sorted(RUNTIMES), default="other")
    parser.add_argument("--compaction-mode", choices=sorted(COMPACTION_MODES), default="unavailable")
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


def section_body(content: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = content.splitlines()
    matches = [index for index, line in enumerate(lines) if line == marker]
    if not matches:
        raise SystemExit(f"CONTEXT.md is missing required section: {heading}")
    if len(matches) > 1:
        raise SystemExit(f"CONTEXT.md repeats required section: {heading}")
    start = matches[0] + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).strip()


def clean_cell(value: str, label: str) -> str:
    if "|" in value or "\n" in value or "\r" in value:
        raise SystemExit(f"{label} cannot contain table separators or newlines")
    return value.strip() or "unknown"


def read_summary_max_chars(manifest_path: Path) -> int:
    in_context_block = False
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line == "context_management:":
            in_context_block = True
            continue
        if in_context_block and line and not line.startswith(" "):
            break
        if in_context_block and line.strip().startswith("summary_max_chars:"):
            raw = line.split(":", 1)[1].strip()
            try:
                value = int(raw)
            except ValueError:
                raise SystemExit("context_management.summary_max_chars must be an integer") from None
            if value < 1000:
                raise SystemExit("context_management.summary_max_chars must be at least 1000")
            return value
    return 12000


def main() -> int:
    args = parse_args()
    if args.runtime == "codex" and args.compaction_mode not in {"automatic", "none"}:
        raise SystemExit("Codex compaction mode must be automatic or none")
    if args.runtime == "kimi" and args.compaction_mode not in {"command", "none"}:
        raise SystemExit("Kimi Code compaction mode must be command or none")
    root = Path(args.project_root).resolve()
    delivery = resolve_delivery_dir(root, args.state_dir)
    state_path = delivery / "STATE.json"
    context_path = delivery / "CONTEXT.md"
    history_path = delivery / "CONTEXT_HISTORY.md"
    manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
    if not state_path.is_file() or not context_path.is_file() or not history_path.is_file() or not manifest_path.is_file():
        raise SystemExit("Context management is not initialized")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    content = context_path.read_text(encoding="utf-8")
    max_chars = read_summary_max_chars(manifest_path)
    if len(content) > max_chars:
        raise SystemExit(f"CONTEXT.md exceeds {max_chars} characters: {len(content)}")
    bodies = {heading: section_body(content, heading) for heading in REQUIRED_SECTIONS}
    for heading, body in bodies.items():
        if not body or body.lower() in {"tbd", "todo", "unknown"} or "TODO:" in body:
            raise SystemExit(f"CONTEXT.md section is empty or unresolved: {heading}")
    next_action = state.get("next_action")
    if not isinstance(next_action, str) or not next_action.strip():
        raise SystemExit("STATE.json.next_action must be a non-empty string")
    if next_action.strip() not in bodies["Exact Next Action"]:
        raise SystemExit("CONTEXT.md Exact Next Action must include STATE.json.next_action verbatim")

    count = state.get("context_checkpoint_count", 0)
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise SystemExit("STATE.json.context_checkpoint_count must be a non-negative integer")
    checkpoint_id = f"CP-{count + 1:04d}"
    now = datetime.now(timezone.utc).isoformat()
    stage = clean_cell(str(state.get("current_stage", "unknown")), "stage")
    revision = clean_cell(args.revision, "revision")
    reason = clean_cell(args.reason, "reason")
    runtime = clean_cell(args.runtime, "runtime")
    compaction_mode = clean_cell(args.compaction_mode, "compaction mode")
    history_reason = f"{reason} [runtime={runtime}; compaction={compaction_mode}]"

    state["context_checkpoint_count"] = count + 1
    state["last_context_checkpoint_at"] = now
    state["material_actions_since_checkpoint"] = 0
    state["context_checkpoint_due"] = False
    state["context_checkpoint_reasons"] = []
    state["updated_at"] = now
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(f"| {checkpoint_id} | {now} | {history_reason} | {stage} | {revision} | {len(content)} |\n")

    print(json.dumps({
        "checkpoint": checkpoint_id,
        "time": now,
        "reason": reason,
        "runtime": runtime,
        "compaction_mode": compaction_mode,
        "stage": stage,
        "revision": revision,
        "characters": len(content),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
