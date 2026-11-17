---
id: creative-arts.design-for-form-and-experience.design-systems.specifying-component-anatomy
name: specifying-component-anatomy
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [component-anatomy, anatomy-diagram, component-parts, component-spec, component-documentation, design-system-anatomy]
level: practitioner
status: draft
description: "Specify component anatomy: label and number every part, mark optional parts, list dimensions, tokens and states per part, and link anatomy to props and code."
sources:
  - "Nathan Curtis, EightShapes articles on component documentation (medium.com/eightshapes-llc)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Component anatomy spec

An anatomy diagram names every part of a component so designers, developers and writers share a vocabulary.

## Steps
1. **Draw the component** large with numbered callouts for each part (container, leading icon, label, helper text, trailing action, indicator, focus ring).
2. **Table the parts:** number, name, optional or required, what it is (text, icon, shape), and the prop or slot that controls it.
3. **Per part, list the properties:** size, spacing and padding, typography token, colour tokens by state, border and radius tokens, and min and max sizes.
4. **States and variants:** default, hover, focus, pressed, disabled, error, loading, selected; which parts change.
5. **Behaviour notes:** truncation, wrapping, overflow, what happens when optional parts are absent, minimum touch target (see `...interaction-design.sizing-touch-targets`).
6. **Accessibility notes:** role, accessible name source, keyboard keys, focus order (see `...interaction-design.annotating-designs-for-accessibility`).
7. **Link** to the code component and its props (see `...design-systems.designing-a-component-api-and-props`).
8. **Keep one source:** in the design file's component documentation page and in the docs site (see `...design-systems.documenting-components-in-storybook-and-a-docs-site`).

## Verify
- [ ] Every visible part has a number, a name and a token.
- [ ] Optional parts are marked.
- [ ] The anatomy matches the built component.
