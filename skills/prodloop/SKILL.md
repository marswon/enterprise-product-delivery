---
name: prodloop
description: Orchestrate evidence-backed software product delivery from discovery and product definition through UX and technical design, implementation, independent verification, release readiness, and outcome review. Use when the user asks AI to build or substantially change a product or enterprise system end to end, especially when quality, autonomy, resumability, or production readiness matter. Do not use for a narrow code fix with an already complete specification, advice-only product discussion, or a request that does not authorize implementation.
---

# Enterprise Product Delivery

Deliver the right product, not merely finished code. Treat the work as a gated state machine with persistent evidence outside the conversation.

## Runtime And Paths

This Skill supports Codex and Kimi Code. Invocation syntax differs, but the delivery lifecycle is the same.

1. Resolve `SKILL_DIR` as the absolute directory containing this loaded `SKILL.md`. Kimi Code may expose `${KIMI_SKILL_DIR}`; other runtimes may provide the loaded Skill path directly. Do not resolve `references/` or `scripts/` from the product repository.
2. Run every bundled helper as `python3 "<SKILL_DIR>/scripts/<script>.py" ...`, replacing `<SKILL_DIR>` with the resolved absolute path.
3. New projects store state in `<project-root>/.prodloop/`.
4. For backward compatibility, if `.codex/delivery/` exists and `.prodloop/` does not, resume the legacy directory. If both exist, stop and ask which state is authoritative; never merge or choose silently.

## Non-Negotiable Invariants

1. Separate facts, verified experience, assumptions, unknowns, and conflicts.
2. Do not enter implementation before product and solution gates pass.
3. Trace every in-scope outcome to design, implementation, tests, and evidence.
4. Let objective checks judge what they can. Use an independent checker for judgment-heavy work.
5. Do not let the maker alter frozen acceptance criteria or declare final acceptance.
6. Never turn a proposal, mock, unverified command, or generated artifact into a completed-delivery claim.
7. Stop on missing authority, consequential ambiguity, irreversible action, evidence failure, or exhausted retry budget.
8. Treat chat context as disposable; preserve durable truth and a bounded resume packet before compaction or handoff.

## Start Or Resume

1. Read repository instructions and inspect the current worktree before writing delivery metadata.
2. Locate state using the Runtime And Paths rules. If `STATE.json` exists, first read `CONTEXT.md` when present, then the manifest, state, blocks, and current-stage artifacts. Resume `next_action`; do not restart without evidence that upstream work is invalid. If legacy state lacks context artifacts, run `<SKILL_DIR>/scripts/enable_context_management.py --project-root <project-root>`. If this delivery includes interface work and lacks `interface_scope`, run `enable_ui_delivery.py`; if it includes charts, analytical dashboards, maps, monitoring views, or generated visual reports and lacks `visualization_scope`, run `enable_data_visualization.py`. Resolve all helpers from `SKILL_DIR`; they preserve backups and do not overwrite existing artifacts.
3. If no state exists, classify project context, mode, quality profile, human-facing interface scope, and data-visualization scope using [project-modes.md](references/project-modes.md). Agree or explicitly default the autonomy contract, then run `<SKILL_DIR>/scripts/init_delivery_state.py` with the project root, name, context, mode, quality, objective, `--interface-scope in-scope|out-of-scope`, and `--visualization-scope in-scope|out-of-scope`. Use `undetermined` only while G0 remains pending.
4. Read [lifecycle-and-gates.md](references/lifecycle-and-gates.md), [context-and-memory.md](references/context-and-memory.md), and only the other references required for the current stage.
5. Validate state after each gate or transition with `<SKILL_DIR>/scripts/validate_state.py --project-root <project-root>`.

Do not create delivery metadata for advice, review, explanation, or diagnosis-only requests. Those requests do not authorize implementation.

## Stage Routing

| State | Read and apply |
|---|---|
| `S0_INTAKE` | [project-modes.md](references/project-modes.md), [autonomy-and-stop-policy.md](references/autonomy-and-stop-policy.md), [enterprise-quality-profiles.md](references/enterprise-quality-profiles.md) |
| `S1_DISCOVERY` | [discovery-analysis.md](references/discovery-analysis.md); for `brownfield`, also [brownfield-onboarding.md](references/brownfield-onboarding.md) |
| `S2_PRODUCT_DEFINITION` | [product-definition.md](references/product-definition.md); when an interface is in scope, also [business-ui-design.md](references/business-ui-design.md); when data visualization is in scope, also [data-visualization-design.md](references/data-visualization-design.md) |
| `S3_SOLUTION_DESIGN` | [product-ux-design.md](references/product-ux-design.md), [solution-architecture.md](references/solution-architecture.md); when an interface is in scope, also [business-ui-design.md](references/business-ui-design.md) and, only when visual direction is unresolved, [visual-design-references.md](references/visual-design-references.md); when data visualization is in scope, also [data-visualization-design.md](references/data-visualization-design.md) |
| `S4_DELIVERY_PLANNING` | [delivery-planning.md](references/delivery-planning.md) |
| `S5_IMPLEMENTATION` | [implementation-loop.md](references/implementation-loop.md); enforce the frozen `UI_CONTRACT.md` and `DATA_VIS_CONTRACT.md` when their scopes are in-scope |
| `S6_INDEPENDENT_VERIFICATION` | [independent-verification.md](references/independent-verification.md); complete `UI_VERIFICATION.md` and `DATA_VIS_VERIFICATION.md` when their scopes are in-scope |
| `S7_RELEASE_READINESS`, `S8_DELIVERY`, `S9_OUTCOME_REVIEW` | [release-and-outcomes.md](references/release-and-outcomes.md) |
| `BLOCKED`, `REWORK`, `STOPPED` | [autonomy-and-stop-policy.md](references/autonomy-and-stop-policy.md), then the responsible stage reference |

For a `brownfield` project, G1 cannot pass until the six takeover artifacts defined in [brownfield-onboarding.md](references/brownfield-onboarding.md) are evidence-backed and marked complete. A prior `$codebase-audit` report may supply evidence, but verify its repository revision, scope, and freshness before reuse.

For schema V4/V5 state, G0 cannot pass until both `interface_scope` and `visualization_scope` are explicitly `in-scope` or `out-of-scope`. When a scope is `in-scope`, G3 requires its complete contract and G6 requires its complete verification report. Schema V5 also requires the context-management artifacts. Visual polish is not evidence of task usability or data truth.

## Execution Loop

1. Read current authority, inputs, state, blocks, and budget.
2. Perform the smallest in-scope action that produces new evidence.
3. Save decisions, progress, blocks, changed assumptions, commands, and evidence immediately.
4. After a material action or boundary event, run `<SKILL_DIR>/scripts/track_context_budget.py --project-root <project-root> [--event <event>] [--reported-context-k <k>]`. When it reports `checkpoint_due`, apply [context-and-memory.md](references/context-and-memory.md) before the next non-atomic action.
5. Run the current gate. A gate passes only from evidence, not narrative.
6. On pass, record it, advance state and `next_action`, then validate state.
7. On failure, identify the responsible upstream stage, invalidate dependent evidence, and enter `REWORK`.
8. On missing authority or evidence, enter `BLOCKED`. On a hard stop, enter `STOPPED` and deliver honestly.

When implementation is authorized, continue until delivery or a defined stop condition. Do not stop merely to present a plan.

## Independence

Use a separate agent or isolated read-only checking pass when available and authorized. Give the checker the frozen objective, specification, quality profile, candidate, and raw evidence, but not the maker's intended conclusion. If true independence is unavailable, disclose that limitation.

## Completion

Completion requires `G8` to pass. Production deployment is optional unless explicitly authorized; an evidence-backed deployable candidate may be the valid delivery. Outcome review occurs later when real usage evidence exists.

Before reporting completion, create a final context checkpoint, validate state, run `<SKILL_DIR>/scripts/check_traceability.py --project-root <project-root> --require-complete`, distinguish completed/blocked/unverified/deferred work, and report actual verification plus anything that could not be verified. Cross-project memory remains candidate-only unless the user explicitly authorizes promotion.
