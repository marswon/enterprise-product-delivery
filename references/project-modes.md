# Project Modes

Choose one primary mode and at most two secondary modes. Record evidence, mode-specific risks, shortened/expanded stages, and what would force reclassification.

- `greenfield`: start from an idea or unmet need. Discovery and product definition are mandatory. Compare buy, adapt, integrate, and build. Main risk: polished solution to an unverified problem.
- `feature`: change an existing system. Treat actual behavior, data, permissions, tests, patterns, and user habits as evidence. Main risk: locally correct code breaking an existing workflow.
- `workflow-change`: change an enterprise process. Model actors, responsibility, states, approvals, rejection, cancellation, reopening, handoffs, and audit. Do not translate coordination ambiguity directly into UI.
- `integration`: connect owned systems. Freeze contracts, authority of record, authentication, idempotency, retries, ordering, reconciliation, partial failure, and version handoff. Stop rather than guess a missing contract.
- `migration`: move behavior or data. Inventory sources, mappings, invalid/duplicate records, validation, coexistence, cutover, rollback, backup, and recovery.
- `remediation`: repair defects or quality. Establish reproduction and impact, distinguish root cause from symptom, add regression evidence, and prove monitoring detects recurrence.

A narrow fix with a complete specification may not need this skill unless it carries migration, enterprise, cross-system, or ambiguous product risk.
