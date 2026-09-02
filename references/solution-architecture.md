# Solution Architecture

Select the simplest architecture satisfying approved behavior and quality. Compare adapting, buying, integrating, and building when mature capabilities may exist.

Cover what applies: system context/ownership/modules/data flow; domain identifiers/invariants/lifecycle/authority; API/event contracts/version/auth/idempotency/order/retry/timeout/reconciliation; transaction/consistency boundaries; schema/history/migration/validation/coexistence/cutover/rollback; failure/degradation/recovery/monitoring/capacity; privacy/secrets/audit/retention/tenant isolation/dependencies/licenses; build/deploy/environments/compatibility/operations.

For consequential choices, document context, forces, realistic options, decision, evidence, consequences, rollback/migration, and reconsideration triggers. Do not justify the first familiar technology after the fact.

Before implementation, define how to prove business invariants, permission denial, isolation, concurrency/duplication/retry/order, migration correctness/reversibility, dependency failure, performance assumptions, and alert response.

G3 passes when the solution covers approved flows, critical risks have tests and recovery, contracts are explicit, migration and operations are designed where relevant, and planning can proceed without inventing architecture under deadline.
