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

## Start Or Resume

1. Read repository instructions and inspect the current worktree before writing delivery metadata.
2. Locate state using the Runtime And Paths rules. If `STATE.json` exists, read the manifest, state, progress, blocks, and current stage artifacts. Resume `next_action`; do not restart without evidence that upstream work is invalid. If this delivery includes interface work and legacy state lacks `interface_scope`, run `<SKILL_DIR>/scripts/enable_ui_delivery.py --project-root <project-root> --interface-scope in-scope` before advancing a gate; it preserves backups and does not overwrite existing UI artifacts.
3. If no state exists, classify project context, mode, quality profile, and whether a human-facing interface is in scope using [project-modes.md](references/project-modes.md), agree or explicitly default the autonomy contract, then run `<SKILL_DIR>/scripts/init_delivery_state.py` with the project root, name, context, mode, quality, objective, and `--interface-scope in-scope|out-of-scope`. Use `undetermined` only while G0 remains pending.
4. Read [lifecycle-and-gates.md](references/lifecycle-and-gates.md) and only the references required for the current stage.
5. Validate state after each gate or transition with `<SKILL_DIR>/scripts/validate_state.py --project-root <project-root>`.

Do not create delivery metadata for advice, review, explanation, or diagnosis-only requests. Those requests do not authorize implementation.

## Stage Routing

| State | Read and apply |
|---|---|
| `S0_INTAKE` | [project-modes.md](references/project-modes.md), [autonomy-and-stop-policy.md](references/autonomy-and-stop-policy.md), [enterprise-quality-profiles.md](references/enterprise-quality-profiles.md) |
| `S1_DISCOVERY` | [discovery-analysis.md](references/discovery-analysis.md); for `brownfield`, also [brownfield-onboarding.md](references/brownfield-onboarding.md) |
| `S2_PRODUCT_DEFINITION` | [product-definition.md](references/product-definition.md); when an interface is in scope, also [business-ui-design.md](references/business-ui-design.md) |
| `S3_SOLUTION_DESIGN` | [product-ux-design.md](references/product-ux-design.md), [solution-architecture.md](references/solution-architecture.md); when an interface is in scope, also [business-ui-design.md](references/business-ui-design.md) and, only when visual direction is unresolved, [visual-design-references.md](references/visual-design-references.md) |
| `S4_DELIVERY_PLANNING` | [delivery-planning.md](references/delivery-planning.md) |
| `S5_IMPLEMENTATION` | [implementation-loop.md](references/implementation-loop.md); when an interface is in scope, enforce the frozen `UI_CONTRACT.md` |
| `S6_INDEPENDENT_VERIFICATION` | [independent-verification.md](references/independent-verification.md); when an interface is in scope, apply [business-ui-design.md](references/business-ui-design.md) and complete `UI_VERIFICATION.md` |
| `S7_RELEASE_READINESS`, `S8_DELIVERY`, `S9_OUTCOME_REVIEW` | [release-and-outcomes.md](references/release-and-outcomes.md) |
| `BLOCKED`, `REWORK`, `STOPPED` | [autonomy-and-stop-policy.md](references/autonomy-and-stop-policy.md), then the responsible stage reference |

For a `brownfield` project, G1 cannot pass until the six takeover artifacts defined in [brownfield-onboarding.md](references/brownfield-onboarding.md) are evidence-backed and marked complete. A prior `$codebase-audit` report may supply evidence, but verify its repository revision, scope, and freshness before reuse.

For schema V3 state, G0 cannot pass until `interface_scope` is explicitly `in-scope` or `out-of-scope`. When it is `in-scope`, G3 requires a complete `UI_CONTRACT.md`, and G6 requires a complete `UI_VERIFICATION.md`. Visual polish is not evidence of task usability.

## Execution Loop

1. Read current authority, inputs, state, blocks, and budget.
2. Perform the smallest in-scope action that produces new evidence.
3. Save decisions, progress, blocks, changed assumptions, commands, and evidence immediately.
4. Run the current gate. A gate passes only from evidence, not narrative.
5. On pass, record it, advance state and `next_action`, then validate state.
6. On failure, identify the responsible upstream stage, invalidate dependent evidence, and enter `REWORK`.
7. On missing authority or evidence, enter `BLOCKED`. On a hard stop, enter `STOPPED` and deliver honestly.

When implementation is authorized, continue until delivery or a defined stop condition. Do not stop merely to present a plan.

## Independence

Use a separate agent or isolated read-only checking pass when available and authorized. Give the checker the frozen objective, specification, quality profile, candidate, and raw evidence, but not the maker's intended conclusion. If true independence is unavailable, disclose that limitation.

## Completion

Completion requires `G8` to pass. Production deployment is optional unless explicitly authorized; an evidence-backed deployable candidate may be the valid delivery. Outcome review occurs later when real usage evidence exists.

Before reporting completion, validate state, run `<SKILL_DIR>/scripts/check_traceability.py --project-root <project-root> --require-complete`, distinguish completed/blocked/unverified/deferred work, and report actual verification plus anything that could not be verified.
