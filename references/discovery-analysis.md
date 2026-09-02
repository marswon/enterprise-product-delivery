# Discovery And Analysis

Discovery establishes what is true before defining what to build.

## Investigate

- Read repository rules, source, tests, schemas, routes, relevant history, and product documents.
- Reproduce current behavior with real commands or interaction where possible.
- Map actors, tasks, inputs, decisions, handoffs, outputs, failures, and authority of record.
- Identify existing capabilities and mature foundations before proposing new construction.
- Collect direct evidence: reports, tickets, analytics, logs, interviews, workflow artifacts, or observed behavior.
- Record unavailable evidence instead of substituting generic assumptions.

For `greenfield`, compare the problem with current alternatives, including manual or non-software approaches. For existing systems, preserve hidden contracts and distinguish documented behavior from actual behavior.

Label material claims as `fact`, `verified_experience`, `assumption`, `unknown`, or `conflict`. Do not let confident prose erase these labels.

## `DISCOVERY.md`

Include objective/boundary, users/stakeholders/current workflow, system/data map, pain and evidence, alternatives/capabilities, constraints/dependencies/risks, classified claims, candidate problem statement, and evidence that would disprove the direction.

## G1

Pass only when the core problem has evidence, current behavior is reproducible or its absence explained, consequential conflicts are resolved or blocked, and product definition can proceed without presenting assumptions as facts.
