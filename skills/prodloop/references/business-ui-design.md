# Business Interface Design

Design enterprise interfaces around work, records, decisions, and exceptions. Do not treat a dashboard template or a marketing-site aesthetic as a product design.

## Scope Decision

At S0 set `interface_scope` to `in-scope` when the delivery adds or changes a human-facing web, desktop, mobile, or embedded interface. Set it to `out-of-scope` only with a recorded reason. Keep it `undetermined` until evidence is sufficient; G0 cannot pass in that state.

For brownfield work, inventory the current component system, tokens, layouts, interaction conventions, accessibility behavior, and visual regressions before proposing replacement. Prefer the established system unless evidence shows it cannot support the frozen product contract. Do not redesign unrelated screens to make one feature look consistent.

## Three Layers

Keep these decisions separate and resolve them in order:

1. **Product structure:** roles, objects, states, permissions, information architecture, and end-to-end tasks from `PRODUCT_SPEC.md`.
2. **Business interaction patterns:** list-detail, record workspace, search/filter/view, bulk action, approval, configuration, monitoring, and recovery behavior.
3. **Visual language:** brand, type, color, spacing, shape, imagery, and motion.

A visual reference cannot repair a missing workflow. A component library cannot decide business meaning.

## Pattern Router

Use official sources as pattern evidence, not as permission to copy a vendor's identity. Check current maintenance, license, framework compatibility, and existing project constraints before adopting code.

| Product surface | Primary pattern references | Useful strengths |
|---|---|---|
| General Chinese CRM, project, approval, and administration | [Ant Design](https://ant.design/), [Ant Design Pro](https://pro.ant.design/), [TDesign](https://tdesign.tencent.com/) | Dense forms and tables, record pages, steps, permissions, Chinese text and multi-platform implementation |
| ERP, finance, procurement, manufacturing, and master data | [SAP Fiori](https://experience.sap.com/fiori-design-web/), [UI5](https://ui5.github.io/webcomponents/) | List reports, object pages, worklists, value help, analytical pages, approvals, enterprise roles |
| Cloud, AI, data administration, and complex configuration | [Cloudscape](https://cloudscape.design/) | App layout, collection views, property filters, split panels, wizards, resource detail and creation flows |
| CRM record workspaces and sales/service workflows | [Salesforce Lightning](https://www.lightningdesignsystem.com/) | Record detail, activity timeline, related data, pipeline and console patterns; reference guidance only unless license and implementation fit are verified |
| Industrial operations, infrastructure, logs, alerts, and topology | [PatternFly](https://www.patternfly.org/) | Operator consoles, log viewers, topology, status, progressive disclosure and technical density |
| Accessible data-heavy enterprise applications | [Carbon](https://carbondesignsystem.com/) | Data tables, batch actions, structured shells, data visualization and accessibility discipline |

Choose one primary implementation system per application surface. Borrow workflow ideas from other sources, but do not mix multiple component libraries in one surface merely to obtain individual widgets. If the repository already has a coherent component system, map patterns into it instead of replacing it by default.

## Required `UI_CONTRACT.md`

When `interface_scope` is `in-scope`, maintain `.prodloop/UI_CONTRACT.md` as the implementation contract. It must contain evidence or explicit decisions for:

- actors, work setting, device and input assumptions, frequency, urgency, and information density;
- critical task scripts with entry, continuation, completion, return, exception, and recovery;
- information architecture and navigation, including object ownership and cross-object relationships;
- page-pattern choices for list, search, filter, saved views, detail, create/edit, bulk action, approval, dashboard, settings, and audit history as applicable;
- loading, empty, partial, success, validation, conflict, offline, expired, permission-denied, destructive, undo, and recovery states as applicable;
- table behavior: column priority, width, wrapping, fixed areas, sort/filter, pagination or virtualization, selection, batch action, long values, and export;
- form behavior: grouping, defaults, dependencies, validation timing, drafts, preserved input, cancellation, submission, retry, and duplicate prevention;
- role and permission differences without exposing unauthorized actions or data;
- responsive reflow based on task priority, not simple shrinkage; define what moves, collapses, becomes a drawer, or is intentionally desktop-only;
- keyboard order, visible focus, semantic labels, contrast, touch targets, text fit, localization, and reduced motion where relevant;
- the single primary implementation system, reuse boundary, tokens, icon source, and approved exceptions;
- visual direction, source principles, project-specific adaptations, and explicit anti-copy/brand constraints;
- fixture matrix for realistic volume, long text, empty data, failures, roles, and edge conditions;
- browser and task-based verification plan with viewports and evidence locations.

Mark `Status: complete` only when implementers no longer need to invent consequential product behavior or visual rules. Unknown business meaning blocks the responsible product gate; an aesthetic preference may use a reversible default if the autonomy contract permits it.

## Business UI Guardrails

- Optimize common repeated work for scanning and action count; reserve spacious editorial composition for reading or marketing surfaces.
- Use dashboards to support a decision and provide a path to the underlying records. Do not fill the first screen with decorative KPI cards.
- Prefer tables for comparison, timelines for event history, trees for hierarchy, step flows for ordered completion, and detail workspaces for one business object.
- Keep primary actions stable and contextual. Do not hide frequent commands behind ornamental cards or ambiguous icon-only controls.
- Preserve user input across validation, dependency failure, navigation mistakes, and retry whenever safe.
- Make status, ownership, freshness, permission, and next action visible where decisions are made.
- Use realistic domain content during design and verification. Lorem ipsum and uniformly short mock records conceal layout and workflow defects.
- Avoid nested cards, excessive rounding, low-contrast gray text, decorative gradients, giant headings in work surfaces, and one-card-per-field layouts unless the domain requires them.

## G3 And G6

G3 passes for an in-scope interface only when `UI_CONTRACT.md` is complete, critical task scripts map to the product contract, the primary implementation system is selected or an evidence-backed custom system is specified, and the verification fixtures and viewports are frozen.

At S6 the checker uses the frozen contract and completes `UI_VERIFICATION.md`. Test real tasks in a real browser with representative data and roles. Screenshots support visual judgment but do not replace interaction. Any blocker in task completion, data comprehension, permission safety, recovery, text fit, responsive behavior, keyboard use, or visual hierarchy routes to the responsible stage.
