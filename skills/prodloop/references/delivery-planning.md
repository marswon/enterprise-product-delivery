# Delivery Planning

Convert approved design into independently verifiable vertical slices.

## Real Baseline

Run repository-specific install, build, tests, lint/type checks, startup, migrations, and representative interaction. Detect placeholders, ignored exits, skips, inaccessible paths, environmental failure, and dirty-worktree constraints. Record exact command, date, exit status, and relevant output in `BASELINE.md`.

Permission failure or missing dependencies are not a passing baseline. Do not rewrite user changes to obtain a clean baseline.

## Slice Record

For each slice record linked requirement/design, user-visible outcome, implementation boundary/allowed paths, dependencies/shared owners, data/permission/interface/UX/operational effects, positive/negative/recovery/regression checks, evidence, and rollback.

Order by dependency and risk retirement. Build a thin running skeleton early, then deepen it without spreading unfinished horizontal layers.

## Freeze The Judge

Identify acceptance scripts, fixtures, contracts, schemas, and design references acting as judge. The maker cannot weaken/delete/skip/replace them. A wrong judge requires a separately authorized correction.

## Traceability

Maintain:

`ID | Outcome | Product Rule | Design | Implementation | Positive Test | Negative Test | Evidence | Status`

Avoid pipe characters inside cells. Run `<SKILL_DIR>/scripts/check_traceability.py --project-root <project-root>` before G4 and add `--require-complete` before delivery. Resolve `SKILL_DIR` from the loaded Skill, not from the product repository.

G4 passes when baseline evidence is real, slices are bounded, dependencies/owners are explicit, the judge is frozen, state is resumable, and every in-scope requirement has a row.
