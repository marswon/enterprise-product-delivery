# Autonomy And Stop Policy

Autonomy is delegated decision-making inside a bounded contract, not permission for external or irreversible action.

## Autonomous

- reversible implementation choices consistent with repository conventions;
- local naming, organization, tests, and error handling that preserve business meaning;
- low-risk UX details inside an approved flow and design system;
- isolated, budgeted, fully recoverable experiments.

Record consequential choices in `DECISIONS.md`: context, options, choice, evidence, impact, rollback.

## Conditional

Dependencies, schema, contracts, permissions, public behavior, compatibility, frozen design changes, private data, paid or external services require an explicit manifest condition and evidence that it is satisfied.

## Denied Unless Explicitly Authorized

Production changes, material deletion, destructive migration, sending/publishing/purchasing/payment/account actions, weakened controls, and product scope expansion.

## Blocking Record

In `BLOCKED.md`, record stable ID/date, stage and scope, missing authority/fact/permission, checks and evidence, safe options/tradeoffs, recommendation, and unaffected work. Use global `BLOCKED` only when the whole next action cannot proceed.

## Retry And Stop

- Three identical failures without new evidence require a changed approach or block.
- Never increase budgets or permissions silently.
- Restore when a safe change falls below baseline.
- Stop immediately for suspected data loss, exposure, unauthorized mutation, or unreliable rollback.
- At budget exhaustion, deliver verified partial results; do not compress standards into a false success.
