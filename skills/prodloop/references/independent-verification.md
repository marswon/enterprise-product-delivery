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

When `interface_scope` is `in-scope`, read [business-ui-design.md](business-ui-design.md), judge against the frozen `UI_CONTRACT.md`, and record raw task, browser, viewport, role, fixture, screenshot, and accessibility evidence in `UI_VERIFICATION.md`. A static screenshot cannot prove task completion, error recovery, permission behavior, keyboard use, or responsive interaction.

When `visualization_scope` is `in-scope`, read [data-visualization-design.md](data-visualization-design.md), judge against the frozen `DATA_VIS_CONTRACT.md`, and record source reconciliation, metric fixtures, rendered scales, labels, interaction, access, freshness/failure, responsive, and accessibility evidence in `DATA_VIS_VERIFICATION.md`. A plausible-looking chart is not evidence that its aggregation or message is correct.

For critical controls, deliberately create a safe failure, prove red, restore, then prove green. Report blocking defects, accepted risks, unverified areas, and suggestions separately.

G6 passes only when mandatory checks pass, critical tasks/failures have evidence, drift is explained, and the checker did not modify the judge. Required UI and data-visualization verification reports must be marked complete.
