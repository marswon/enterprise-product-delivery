# Project Modes

Classify project context separately from delivery mode.

## Context

- `greenfield`: no existing production behavior, user workflow, persistent data, or compatibility contract is being changed.
- `brownfield`: an existing repository, deployed behavior, user workflow, persistent data, integration, or operational contract constrains the change. A new feature inside an established system is brownfield.

When uncertain, use `brownfield` until evidence shows that no existing contract can be affected. For brownfield work, read [brownfield-onboarding.md](brownfield-onboarding.md).

## Mode

Choose one primary mode and at most two secondary modes. Record evidence, mode-specific risks, shortened/expanded stages, and what would force reclassification.

- `greenfield`: build a new product or bounded capability. Discovery and product definition are mandatory. Compare buy, adapt, integrate, and build. Main risk: polished solution to an unverified problem. This mode may still use `brownfield` context when built inside an established platform.
- `feature`: change an existing system. Treat actual behavior, data, permissions, tests, patterns, and user habits as evidence. Main risk: locally correct code breaking an existing workflow.
- `workflow-change`: change an enterprise process. Model actors, responsibility, states, approvals, rejection, cancellation, reopening, handoffs, and audit. Do not translate coordination ambiguity directly into UI.
- `integration`: connect owned systems. Freeze contracts, authority of record, authentication, idempotency, retries, ordering, reconciliation, partial failure, and version handoff. Stop rather than guess a missing contract.
- `migration`: move behavior or data. Inventory sources, mappings, invalid/duplicate records, validation, coexistence, cutover, rollback, backup, and recovery.
- `remediation`: repair defects or quality. Establish reproduction and impact, distinguish root cause from symptom, add regression evidence, and prove monitoring detects recurrence.

A narrow fix with a complete specification may not need this skill unless it carries migration, enterprise, cross-system, or ambiguous product risk.
