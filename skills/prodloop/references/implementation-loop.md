# Implementation Loop

Implement one bounded vertical slice at a time while preserving product and solution contracts.

1. Read linked requirements, design, baseline, constraints, and state.
   When `interface_scope` is `in-scope`, also read the frozen `UI_CONTRACT.md`; use its primary component system and approved exceptions rather than introducing a second UI library.
2. Reproduce the relevant baseline before changing behavior where practical.
3. Implement the smallest coherent outcome across needed layers.
4. Run nearest objective checks, then integration/regression checks proportional to blast radius.
5. Exercise defined negative, permission, recovery, and concurrency paths.
6. Update traceability, decisions, progress, blocks, and evidence immediately.
7. Integrate only after the slice meets its checks.

For interface slices, exercise the slice in a real browser during implementation with the contract's representative fixtures and viewports. Do not defer all rendering, text-fit, responsive, focus, or state checks to S6.

Forbidden false progress: deleting/skipping tests; weakening assertions, thresholds, schemas or acceptance scripts; mocking the core claim; hard-coding results; swallowing failures; replacing real integration with static UI; or changing business scope without returning to the responsible gate.

When evidence breaks an assumption, stop the affected slice, record it, identify the responsible upstream stage, invalidate dependents, and re-enter implementation only after that gate passes.

G5 passes when all in-scope slices run, checks pass, baseline has not silently regressed, required migrations/contracts exist, and deviations have authorized decisions and evidence.
