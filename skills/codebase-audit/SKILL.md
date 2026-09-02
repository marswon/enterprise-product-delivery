---
name: codebase-audit
description: Perform a bounded, evidence-backed audit of an established software repository to explain its architecture, runtime behavior, contracts, risks, and change surface without implementing fixes. Use when the user wants to understand, take over, assess, or prepare changes to an existing codebase. Do not use for implementation, a full product delivery, or a narrow bug with an already known cause.
---

# Codebase Audit

Build a trustworthy working model of the relevant codebase. Optimize for decision usefulness and evidence, not exhaustive file summaries.

## Boundary

This is an audit-only Skill. Read and run proportionate diagnostic checks, but do not edit product files, install or upgrade dependencies, clean the worktree, change configuration, migrate data, deploy, or implement fixes unless the user separately authorizes that action. Commands that may write caches, generated files, databases, or external state require explicit consideration and authorization.

Never expose secrets or unnecessary private data. Record inaccessible evidence and failed checks instead of inferring success.

## Audit Contract

Before deep inspection, establish:

- audit question and intended decision;
- repository root, revision, branch, and worktree state;
- systems, flows, or modules in scope and explicitly out of scope;
- available runtime, test, deployment, and operational evidence;
- time or depth budget and required confidence.

If the request is broad, default to architecture, one representative critical path, data and permission boundaries, build/test/deploy truth, and the highest-impact risks. State sampling limits.

## Evidence Passes

1. **Topology:** read repository instructions, manifests, entry points, module boundaries, schemas, routes, tests, infrastructure, deployment files, and relevant history.
2. **Runtime truth:** compare documented commands with observed results where safe; distinguish passing, failing, blocked, skipped, and unavailable checks.
3. **Critical path:** trace representative user or system flows across interface, logic, data, permissions, integrations, failure handling, and operations.
4. **Contracts and change surface:** identify public interfaces, stored-data invariants, compatibility obligations, acceptance judges, shared owners, and likely transitive impact.
5. **Risk and unknowns:** prioritize findings by consequence and evidence strength; separate relevant technical debt from unrelated cleanup opportunities.

For each material claim label it `observed`, `documented`, `inferred`, `unknown`, or `conflict`, and cite the file, command, runtime observation, or source supporting it.

## Deliverable

Return a concise audit with:

1. scope, revision, worktree state, and evidence limitations;
2. system purpose and relevant architecture map;
3. representative execution and data flow;
4. build, test, runtime, deployment, and operational baseline;
5. behavior, interface, data, permission, and compatibility contracts;
6. findings ordered by severity, with evidence and impact;
7. change-surface guidance for the user's intended work;
8. unknowns and the cheapest next verification actions;
9. a clear confidence and coverage statement.

Do not create repository files unless the user requests a persistent report. When persistence is authorized, write `CODEBASE_AUDIT.md` or the requested path without modifying product code.

## Prodloop Handoff

When the audit will feed `$prodloop`, map verified content to `CURRENT_SYSTEM_BASELINE.md`, `SYSTEM_MAP.md`, `BEHAVIOR_CONTRACT.md`, `CHANGE_IMPACT.md`, `REGRESSION_SCOPE.md`, and `TECH_DEBT_BOUNDARY.md`. Include repository revision, scope, timestamps or freshness constraints, failed checks, and unknowns so prodloop can decide what must be revalidated. The audit does not pass prodloop G1 by itself and does not authorize implementation.

## Completion

Complete when the stated audit question can be answered within the declared coverage, every material conclusion has evidence or an uncertainty label, failed and unavailable checks are visible, and recommendations do not masquerade as implemented fixes.
