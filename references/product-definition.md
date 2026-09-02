# Product Definition

Translate evidence into a product contract before choosing implementation.

Define target roles; trigger, context, intent, and outcome; primary and exception journeys; entities, states, transitions, rules, permissions, and ownership; validation, cancellation, rejection, retry, reopening, recovery, and data lifecycle; success measures with baseline/formula/source/period/owner; scope, non-goals, compatibility, deferred work; and assumptions with validation actions.

Separate business outcome, product behavior, proposed implementation, and constraint. Treat implementation suggestions as hypotheses unless explicitly fixed.

## Vertical Outcome Slices

A slice completes a user or business outcome across UI/API, rules, data, permissions, and feedback. Avoid horizontal plans such as frontend then backend then database unless infrastructure blocks every outcome.

Each slice states actor/trigger, happy and exception paths, data/state effects, permission/audit behavior, observable result, and exclusions.

## `PRODUCT_SPEC.md`

Use stable requirement IDs. Include journeys, rules, state transitions, permission matrix, acceptance scenarios, measures, non-goals, and unresolved decisions. Use structured representations where they reduce ambiguity, not to fill a template.

## G2

Pass only when every in-scope capability has a user, scenario, rule, and observable result; critical states and permissions are defined; product-semantic ambiguity is resolved; and non-goals prevent expansion.
