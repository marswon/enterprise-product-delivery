# Enterprise Quality Profiles

Choose the lowest profile that honestly matches exposure. AI may recommend raising it; only the authorized owner may lower it.

- `Q0 Exploration`: hypotheses, running proof, representative examples, visible limits, no production claim, continue/change/stop decision. Mocks only outside the core hypothesis and visibly labeled.
- `Q1 Internal Tool`: Q0 plus identity where needed, roles, validation, durable data, errors, logs, basic accessibility, backup/export and verified restoration, dependency/license review, operator instructions.
- `Q2 Production Business`: Q1 plus permission matrix, audit, migration/rollback, monitoring/alerts, capacity/performance baseline, security review, compatibility, recovery, support ownership, staged release, tested restore, user documentation.
- `Q3 Enterprise Critical`: Q2 plus tenant isolation, least privilege, threat model, change approval, recovery objectives/exercise, dependency degradation, capacity, incident ownership, compliance evidence, retention, key rotation, and organization controls.

This skill coordinates Q3 but cannot invent organizational policy or replace professional approval. Missing controls block a Q3 completion claim.

Record mandatory controls, `not_required` controls with rationale, measurement, owner, and evidence. Feature/test counts and automation percentage are not quality proxies.
