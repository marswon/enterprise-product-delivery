# Enterprise Data Visualization

Use this module when the delivery includes charts, analytical dashboards, maps, monitoring views, or generated visual reports. The objective is not to maximize chart variety. It is to let a defined audience reach a correct decision from traceable data.

## Start From The Decision

For each visualization, record:

- the audience, decision or task, and action available after reading it;
- the metric owner, source, definition, grain, filters, denominator, time zone, refresh policy, and permitted roles;
- the intended comparison, trend, distribution, relationship, composition, flow, geography, or exact lookup;
- the underlying records or explanation path needed to investigate the result;
- the freshness, uncertainty, missing-data, and failure signals that must remain visible.

Do not create a chart for a metric whose meaning or source is unresolved. Route business-definition conflicts to S2 and data-contract conflicts to S3.

## Choose The Encoding

Compare at least a table and one plausible visual encoding before freezing a consequential chart. Prefer the simplest representation that preserves the intended judgment.

| Analytical need | Usually appropriate | Reject or justify carefully |
|---|---|---|
| Exact lookup or many fields | table with sort, filter, and clear units | a chart that hides exact values |
| Category comparison or ranking | horizontal or vertical bars; dot plot | area or volume encoding for one-dimensional values |
| Change over ordered time | line; bars for discrete periods | unordered categories connected as a trend |
| Distribution and outliers | histogram, box plot, strip/dot plot | averages without spread or sample size |
| Relationship between measures | scatter plot with meaningful scales | implying causation from correlation |
| Part-to-whole | stacked bars or a small number of labeled parts | many-slice pies or parts with inconsistent totals |
| Stage conversion or conserved flow | funnel only for ordered attrition; flow diagram only when quantities reconcile | decorative funnels or flows with no conservation check |
| Geography | map only when location or spatial pattern matters | maps used merely as colorful category lists |
| Hierarchy | indented table, tree, or treemap when area comparison is acceptable | deep unlabeled nesting |

Avoid dual axes unless a single shared interpretation is defensible and less misleading alternatives fail. Small multiples are usually clearer for differently scaled series.

## Truthful Data Contract

Freeze the following in `DATA_VIS_CONTRACT.md` before implementation:

- metric IDs, plain-language definitions, owners, sources, transformations, joins, aggregation grain, denominators, units, precision, time zone, and refresh expectations;
- access-control and tenant boundaries from source query through aggregates, exports, tooltips, caches, and drill-down records;
- representative queries or reconciliations that can independently reproduce key values;
- chart purpose, chosen encoding, rejected alternative, scale and axis rules, sort order, thresholds, reference lines, labels, annotations, and uncertainty treatment;
- behavior for zero, negative, missing, suppressed, delayed, partial, estimated, and extreme values;
- filters, defaults, URL or saved-view persistence, cross-filter effects, reset behavior, drill-down destination, back-navigation, exports, and audit needs;
- loading, no-result, stale, partial, permission-denied, query-failed, and retry states;
- color meanings, non-color cues, text alternatives, keyboard path, focus behavior, reduced motion, and responsive transformation;
- representative fixtures, expected values, browser/viewports, performance limits, and evidence locations.

One chart should have one primary claim. A dashboard may support several decisions, but each region needs explicit ownership and a route from summary to explanation to authorized records.

## Encoding Guardrails

- Start quantitative bar axes at zero. If a non-zero range is necessary for another encoding, disclose it and ensure it cannot exaggerate the decision.
- Preserve proportional area when area, bubbles, or map symbols encode magnitude. Scale area, not diameter, to the value.
- Keep units, precision, aggregation window, denominator, and comparison period visible where ambiguity would change interpretation.
- Distinguish zero, missing, not applicable, suppressed, delayed, and query failure. Never silently coerce them into one state.
- Show sample size, uncertainty, or estimation status when the decision depends on them.
- Use a stable semantic color mapping across the product. Color must not invent categories or imply good/bad meaning that the domain does not support.
- Use labels, shapes, patterns, or position so meaning is not carried by color alone. Check contrast in the rendered product.
- Prevent clipped labels, unreadable legends, tooltip overflow, overplotting, and hidden series at representative and worst-case volumes.
- Motion may explain a transition, but must not be required to read the result. Honor reduced-motion preferences.
- Do not render controls, hover targets, drill-down affordances, or exports that are not connected to real behavior and authorized records.

## Dashboard Workflow

Design the dashboard as a work surface, not a collage of KPI cards.

1. Show status, scope, time window, freshness, and the few signals that determine attention.
2. Support explanation through comparisons, breakdowns, annotations, and filters.
3. Provide an authorized route to the records or events that require action.
4. Preserve filter context through drill-down and make returning predictable.
5. Make shared filters, local filters, cross-filtering, selection, and reset visibly distinct.

Do not place unrelated metrics together merely because space is available. If no decision or follow-up action exists, use a report, notification, or table instead of a dashboard.

## Implementation And Performance

Use the repository's existing charting system when it can satisfy the frozen contract. Before adopting another library, verify maintenance, license, bundle/runtime cost, accessibility, server-rendering needs, export support, and compatibility with the current framework.

Keep metric computation outside presentation code where practical. Test transformation functions and query contracts independently. Bound query ranges, aggregation cost, point counts, polling, and resize work. Prefer aggregation, sampling with disclosure, virtualization, or progressive loading over freezing the interface.

## G3 And G6

G3 passes for in-scope data visualization only when `DATA_VIS_CONTRACT.md` is marked complete, key metrics are reproducible, chart choices are justified against alternatives, interaction and failure states are frozen, and implementers do not need to invent business meaning.

At S6, an independent checker completes `DATA_VIS_VERIFICATION.md` using representative fixtures and at least one independently calculated reconciliation for every decision-critical metric. Verify rendered output in a real browser or target renderer, including interaction, access control, stale/failed data, keyboard use, reduced motion, responsive behavior, labels, units, legends, and extreme values. Screenshots support visual judgment but do not prove data correctness or interaction.

G6 fails when the display cannot be reconciled to its source, materially distorts scale or magnitude, hides freshness or missing data, leaks unauthorized aggregates or records, offers fake interaction, or blocks the intended decision path.

## External References And License Boundary

External chart galleries and templates may help compare approaches, but they are not automatically licensed implementation assets. Verify the current license before copying code, templates, tokens, catalog text, or distinctive visual assets. Record only project-specific decisions and independently written rules in prodloop artifacts.
