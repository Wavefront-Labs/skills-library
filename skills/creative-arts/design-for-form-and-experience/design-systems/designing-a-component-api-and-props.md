---
id: creative-arts.design-for-form-and-experience.design-systems.designing-a-component-api-and-props
name: designing-a-component-api-and-props
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [component-api, component-props, props-design, api-design-for-components, component-variants-api, design-system-api]
level: advanced
status: draft
description: "Design a component API: pick props over free styling, model variants as enums, name consistently, support controlled use, accessibility and composition, and document."
sources:
  - "Nathan Curtis, EightShapes articles on component APIs (medium.com/eightshapes-llc)"
  - "W3C WAI-ARIA Authoring Practices Guide (w3.org/WAI/ARIA/apg)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Component API and props

A component API is the set of props (inputs), events (outputs) and slots through which teams use a component. Design and code should agree on it (see `...figma.auto-layout-components-and-variants`).

## Principles
1. **Few, meaningful props.** Expose decisions (variant, size, disabled), not CSS internals; avoid a `style` prop that bypasses the system (offer a controlled escape hatch if needed).
2. **Model mutually exclusive options as an enum,** not several booleans: `variant="primary | secondary | ghost"` instead of `primary`, `secondary`, `ghost` flags that can conflict.
3. **Consistent names across components:** `size`, `variant`, `disabled`, `loading`, `onChange`, `value`, `defaultValue`; the same sizes (`sm | md | lg`) everywhere.
4. **Sensible defaults;** the zero-config version should look right.
5. **Support controlled and uncontrolled use** for stateful inputs (`value` + `onChange` vs `defaultValue`).
6. **Pass-through attributes:** forward `className`, `ref` and `aria-*` / data attributes to the root element.
7. **Accessibility built in:** required props for labels where there is no visible text (an `aria-label` for icon buttons), roles and keyboard handling inside the component.
8. **Composition over configuration:** prefer children and slots to dozens of props (see `...design-systems.composing-components-with-slots`).
9. **Mirror the design variants** in the Figma component properties so the vocabulary is shared.
10. **Document** each prop: type, default, description, example; and deprecate properly (see `...design-systems.versioning-deprecating-and-changelogging`).

## Verify
- [ ] No two props can be set into a contradictory state.
- [ ] Names match across design and code.
- [ ] Icon-only usage requires an accessible name.
