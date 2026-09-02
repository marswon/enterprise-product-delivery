# Independent Verification

Judge the candidate from the frozen objective and raw evidence, not the maker's summary.

Prefer a separate agent or isolated read-only pass. Provide objective, product spec, solution design, profile, baseline, candidate, and commands, but not the intended verdict. The checker reports; it does not fix. Disclose reduced assurance when independent context is unavailable.

Apply relevant lenses:

- product: real user/business tasks and exceptions;
- UX: real browser/device interaction, states, responsive behavior, keyboard/accessibility;
- functional: unit, contract, integration, end-to-end, compatibility, regression;
- data: invariants, migration validation, update/delete, recovery;
- permission/security: unauthorized, role, tenant, input, secret, dependency checks;
- reliability: timeout, retry, duplication, ordering, concurrency, dependency failure;
- performance: representative workload and thresholds;
- operations: logs, metrics, traces, alerts, backup, restore, rollback, runbook.

For critical controls, deliberately create a safe failure, prove red, restore, then prove green. Report blocking defects, accepted risks, unverified areas, and suggestions separately.

G6 passes only when mandatory checks pass, critical tasks/failures have evidence, drift is explained, and the checker did not modify the judge.
