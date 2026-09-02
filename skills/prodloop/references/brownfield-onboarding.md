# Brownfield Onboarding

Take over the affected system before designing its change. The goal is sufficient verified understanding of the change surface, not exhaustive documentation of the entire repository.

## Bound The Takeover

Record repository revision and worktree state, requested outcome, affected users and workflows, likely modules and integrations, excluded areas, available environments, and the evidence budget. Preserve user changes. Do not clean, reset, migrate, install, or rewrite merely to make inspection easier.

A prior `codebase-audit` is evidence input, not automatic truth. Recheck its revision, scope, failed commands, unknowns, and any facts likely to have changed.

## Required Artifacts

Complete these files in the active prodloop state directory before G1 passes:

- `CURRENT_SYSTEM_BASELINE.md`: revision, environment, documented versus observed startup/build/test behavior, representative user-path results, pre-existing failures, and unavailable checks.
- `SYSTEM_MAP.md`: relevant entry points, modules, runtime boundaries, data stores, integrations, deployment path, and owners or authority sources.
- `BEHAVIOR_CONTRACT.md`: existing user-visible behavior, business rules, state transitions, permissions, data invariants, interfaces, compatibility promises, and unknown contracts.
- `CHANGE_IMPACT.md`: direct and transitive change surface across UI, logic, data, permissions, integrations, operations, and users; include evidence and confidence.
- `REGRESSION_SCOPE.md`: behaviors that must remain stable, positive and negative checks, fixtures or acceptance judges, missing coverage, and risk-based regression commands.
- `TECH_DEBT_BOUNDARY.md`: relevant debt to fix now, debt to leave unchanged, rationale, and triggers that would require scope or architecture reconsideration.

Each initialized file contains `Status: pending`. Replace it with `Status: complete` only when the content is supported by evidence and consequential unknowns are resolved or explicitly blocked.

## Investigation Rules

1. Start from repository instructions, manifests, entry points, schemas, routes, tests, deploy configuration, relevant history, and actual critical-path behavior.
2. Trace representative flows end to end instead of inferring the system from folder names or framework conventions.
3. Distinguish documented, observed, inferred, unknown, and conflicting claims. A command that could not run is not a passing baseline.
4. Treat existing tests, schemas, public interfaces, stored data, permissions, and user habits as candidate contracts until evidence says otherwise.
5. Limit analysis to the requested outcome plus transitive risk. Do not turn takeover into an unbounded rewrite or general cleanup program.
6. Separate pre-existing failures from regressions introduced by this delivery. Neither may be hidden.

## G1 Brownfield Gate

Pass only when the current revision and environment are identified; representative behavior is observed or its absence explained; the affected system and data path are traceable; compatibility and regression obligations are explicit; change impact is bounded; and unknowns that could change product meaning, data integrity, permissions, or release safety are resolved or blocked.
