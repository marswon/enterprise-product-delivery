# Lifecycle And Gates

The lifecycle is a state machine, not a checklist. Advance only when the current gate has evidence. If upstream authority changes, invalidate every downstream artifact that depends on it.

| State | Purpose | Gate | Required evidence |
|---|---|---|---|
| `S0_INTAKE` | Bound project and authority | `G0` | Mode, profile, objective, scope, authority, budgets, stops |
| `S1_DISCOVERY` | Establish current truth and problem | `G1` | Sources, reproduction, fact/assumption split, conflicts |
| `S2_PRODUCT_DEFINITION` | Freeze user and business behavior | `G2` | Roles, journeys, rules, states, permissions, measures, non-goals |
| `S3_SOLUTION_DESIGN` | Design usable and operable behavior | `G3` | UX, alternatives, architecture, contracts, risks, test strategy |
| `S4_DELIVERY_PLANNING` | Create bounded vertical slices | `G4` | Real baseline, dependencies, ownership, frozen checks, traceability |
| `S5_IMPLEMENTATION` | Build and integrate | `G5` | Running candidate, tests, migrations, decisions, controlled drift |
| `S6_INDEPENDENT_VERIFICATION` | Judge against original objective | `G6` | Product, UX, engineering, data, security, failure evidence |
| `S7_RELEASE_READINESS` | Prove release and recovery | `G7` | Config, migration, monitoring, runbook, rollback, authority |
| `S8_DELIVERY` | Deliver or deploy candidate | `G8` | Version identity, reproducibility, evidence-consistent report |
| `S9_OUTCOME_REVIEW` | Compare real results to baseline | n/a | Usage, business measures, incidents, feedback, decision |

Gate statuses are `pending`, `passed`, `failed`, `invalidated`, or `not_required`. Record why anything is `not_required`. Never infer pass from a later state being active.

Each gate decision records checker or checking mode, criteria, raw sources/commands/screenshots/logs, failures, accepted risk, and invalidated downstream artifacts. Do not store secrets or unnecessary personal/production data.

## Rework Routing

- wrong problem or evidence -> `S1`;
- unclear rule, scope, role, state, or measure -> `S2`;
- unusable flow, architecture, migration, or verification design -> `S3`;
- bad baseline, dependency, slicing, ownership, or judge -> `S4`;
- implementation defect -> `S5`;
- checker/evidence defect -> remain `S6` and repair checking;
- deployment/recovery defect -> `S7`.

Record invalidation before rework so later sessions cannot reuse stale green evidence.
