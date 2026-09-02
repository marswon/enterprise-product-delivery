# Product And UX Design

Design complete tasks, not attractive isolated screens.

Cover information architecture/navigation; entry, continuation, completion and return; loading, empty, partial, success, error, offline, expired and permission-denied states as applicable; validation, destructive confirmation, undo, recovery and preserved input; role differences; responsive behavior; keyboard/focus/semantics/contrast/text fit; and consistency with the existing design system and domain.

Inspect real reference products or current behavior where authorized and useful. Do not infer usability from screenshots alone.

Choose evidence proportional to risk: flows/wireframes for structure, interactive prototypes for consequential new behavior, real browser implementation for final acceptance, and task-based observation for judgment-heavy workflows.

When `interface_scope` is `in-scope`, read [business-ui-design.md](business-ui-design.md) and maintain `UI_CONTRACT.md`. Read [visual-design-references.md](visual-design-references.md) only when visual direction is unresolved or the user asks for visual redesign. Preserve an established design system unless its replacement is explicitly in scope.

Define critical task scripts before implementation: starting state, actor, goal, expected path, success signal, and failure/recovery checks.

The UX portion of G3 passes when critical tasks are complete across states, domain objects/actions are clear, accessibility and responsive constraints are designed, and implementers will not need to invent product behavior while coding. For an in-scope interface, `UI_CONTRACT.md` must be marked complete.
