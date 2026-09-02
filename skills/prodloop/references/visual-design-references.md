# Visual Design References

Use visual references only after product structure and business interaction patterns are understood. The output is a project-specific visual contract, not an instruction to imitate a recognizable brand.

## Source Priority

1. Existing product design system, tokens, and shipped interface behavior.
2. User-provided brand assets and approved references.
3. Domain-appropriate official design systems from [business-ui-design.md](business-ui-design.md).
4. Curated visual-language references such as [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

Do not replace an established brownfield visual system without explicit scope and migration evidence. Verify a third-party source's current license before copying files or code. A repository license does not grant rights to another company's trademarks, proprietary fonts, illustrations, or distinctive brand identity.

## Using `awesome-design-md`

Treat its `DESIGN.md` files as analyses of public marketing surfaces. Extract reusable principles such as contrast, type hierarchy, spacing rhythm, surface treatment, radius, and restrained accent use. Do not assume they describe the referenced product's real application UI, workflow, accessibility, or failure states.

Choose at most one primary visual direction and, when it resolves a specific gap, one secondary reference. Record:

- what is being borrowed and why it fits the users, domain, density, and brand;
- what is rejected because it is marketing-oriented, inaccessible, impractical, or too recognizable;
- substitutions for unavailable proprietary fonts or assets;
- project-specific semantic colors and interaction states;
- examples of both desired and forbidden treatments.

Never tell an implementer only to "make it look like Linear/Notion/Apple." Convert selected principles into project tokens and component rules inside `UI_CONTRACT.md` or the repository's existing design-system documentation.

## Visual Acceptance

Judge rendered pages at frozen viewports with representative data. Check hierarchy, density, rhythm, alignment, consistency, legibility, contrast, text fit, asset quality, responsive composition, and interaction states. Compare screens from the same workflow together so local polish cannot hide cross-page inconsistency.

Visual review does not pass a task that is incomplete, misleading, inaccessible, or operationally inefficient.
