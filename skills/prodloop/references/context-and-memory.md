# Context Budget And Durable Memory

Treat the conversation as a disposable working buffer. The repository and `.prodloop/` artifacts are the durable source of truth.

## Default Budget

New deliveries use these configurable defaults:

- soft context limit: `120K` tokens;
- checkpoint trigger: `80%` of the soft limit, approximately `96K` tokens;
- fallback trigger: every `8` material actions;
- compact working summary: at most `12000` characters.

These are prodloop checkpoint-preparation thresholds, not Codex's internal automatic-compaction threshold and not a claim about when Kimi Code will compact. Use exact token triggers only when the runtime exposes trustworthy context usage. Do not estimate token counts from intuition or claim that compaction occurred without runtime evidence. When usage is unavailable, checkpoint at the fallback triggers below.

A material action changes code, a contract, a decision, a gate, a test result, a block, or the active slice. Routine file reads and repeated polls do not count.

After each material action run `track_context_budget.py` with its default `material-action` event. For a gate, slice change, expected long output, handoff, or completion, pass the matching `--event`. When trustworthy usage is available, also pass `--reported-context-k <k>`. The helper persists the action count and checkpoint reasons so they survive session loss.

## Memory Layers

Keep four layers distinct:

1. **Transient conversation:** exploratory reasoning, tool chatter, and raw outputs. It may be compacted or discarded.
2. **Current working set:** `.prodloop/CONTEXT.md`, a bounded resume packet for the active stage and slice.
3. **Project truth:** product/solution contracts, state, decisions, assumptions, traceability, tests, evidence, and repository history. These override any summary.
4. **Cross-project candidates:** `.prodloop/MEMORY_CANDIDATES.md`, containing only verified lessons that may be reusable. They are not automatically promoted to an external memory system.

Never use a summary as the only copy of a frozen requirement, authorization, unresolved conflict, failed check, security boundary, migration fact, or release evidence.

## Checkpoint Triggers

Create a checkpoint before any of the following:

- reported context use reaches the configured trigger;
- the fallback material-action interval is reached;
- a gate passes, fails, or is invalidated;
- the active vertical slice changes;
- a long investigation, build, test, or browser run is likely to produce substantial output;
- the runtime is about to compact, hand off, pause, or start a new session;
- the agent notices repeated rereading, forgotten constraints, conflicting summaries, or degraded recall.

Do not interrupt an atomic edit or migration merely to checkpoint. Finish or safely roll back the atomic operation first.

## Checkpoint Procedure

1. Move durable facts into their owning artifacts. Do not dump raw conversation into `CONTEXT.md`.
2. Rewrite `CONTEXT.md` from current evidence. Include objective and scope, current state/gates, frozen decisions and assumptions, active slice and changed paths, verification and evidence pointers, open risks/blocks/unknowns, and the exact `STATE.json.next_action`.
3. Keep the packet self-contained but bounded. Replace old narrative with current conclusions and file/evidence pointers.
4. Run `python3 "<SKILL_DIR>/scripts/checkpoint_context.py" --project-root <project-root> --reason <reason> [--revision <git-revision>] --runtime <codex|kimi|other> --compaction-mode <automatic|command|none|unavailable>`. The script reads `summary_max_chars` from the manifest and records the selected runtime route in checkpoint history. This route is not proof that host compaction has already occurred.
5. Follow the runtime-specific route only after step 4 succeeds:
   - **Codex:** use `--runtime codex --compaction-mode automatic` before expected automatic compaction. Let Codex compact automatically; do not invent a manual command.
   - **Kimi Code:** use `--runtime kimi --compaction-mode command`, then execute `/compact`. Never execute `/compact` before durable facts, material failures, evidence pointers, and the exact `next_action` are saved and validated.
   - **No compaction needed:** use `--compaction-mode none`. Do not repeatedly call `/compact` when no meaningful context has accumulated merely because a gate or final checkpoint was recorded.
   - **Other or unsupported host:** use the documented host mechanism or record `unavailable`; never claim the checkpoint itself reduced runtime tokens.
6. After Codex automatic compaction, Kimi `/compact`, or session resume, reload `STATE.json`, `CONTEXT.md`, the manifest, `BLOCKED.md`, and current-stage artifacts. Then retrieve only the additional references and older evidence named by those files instead of reloading the whole history.

The checkpoint script validates structure, size, and exact next action, records the runtime and selected compaction route in `CONTEXT_HISTORY.md`, updates `STATE.json`, and resets the material-action counter. It does not compact the model runtime itself. Runtime UI or command evidence is still required before stating that compaction actually happened.

## Writing A Useful Working Set

Prefer exact identifiers and evidence pointers over prose:

- repository revision and dirty-worktree note;
- current stage, gate statuses, active slice, and next action;
- frozen requirement, decision, assumption, block, and traceability IDs;
- changed paths and ownership boundaries;
- commands/checks with pass, fail, blocked, or not-run status;
- unresolved questions and what evidence will resolve them.

Exclude superseded exploration, repeated command output, general tutorials, abandoned options already recorded in `DECISIONS.md`, and source text that can be retrieved cheaply.

## Long-Term Memory Policy

Project-local durable memory is required; an external long-memory or vector system is optional.

Add a cross-project candidate only when it is reusable, evidence-backed, and materially changes future decisions. Record source, scope, confidence, owner, review date, and status. Keep project-specific secrets, customer data, credentials, transient errors, and unverified guesses out.

Promote candidates outside the repository only with explicit authority and a defined destination, access boundary, version, expiry/review rule, and rollback path. Prefer structured filtering by project, domain, version, authority, and freshness before semantic retrieval. Do not inject an entire memory store into every session.

Use a vector or knowledge-graph layer only when project artifacts no longer fit practical indexed retrieval, cross-project reuse is frequent, and measurable retrieval failures justify the additional governance. A larger context window alone is not a reason to build one.

## Failure And Recovery

If `CONTEXT.md` conflicts with project artifacts, treat it as stale, repair it from primary evidence, and record a new checkpoint. If a checkpoint omits a material unknown or failed check, invalidate it rather than silently continuing. Never lower product or verification standards to meet the context budget.
