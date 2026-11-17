---
id: creative-arts.design-for-form-and-experience.design-systems.tokens-tiers-primitive-semantic-component
name: tokens-tiers-primitive-semantic-component
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [token-tiers, design-token-tiers, primitive-tokens, semantic-tokens, component-tokens, alias-tokens]
level: practitioner
status: draft
description: "Structure design tokens in tiers: primitive values, semantic aliases that carry meaning, and optional component tokens, with rules for what may reference what."
sources:
  - "W3C Design Tokens Community Group (w3.org/community/design-tokens)"
  - "Nathan Curtis, Naming Tokens in Design Systems, EightShapes (medium.com/eightshapes-llc)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Token tiers: primitive, semantic, component

Tiering lets you change a brand colour or theme in one place without rewriting every component.

## Tiers
1. **Primitive (also called global, base or reference) tokens:** raw values with no meaning attached, such as `color.blue.500 = #1D4ED8`, `space.4 = 16px`, `radius.2 = 8px`. They form the palette and scales.
2. **Semantic (alias, system) tokens:** named for purpose and pointing at primitives, such as `color.text.primary -> color.neutral.900`, `color.action.primary.bg -> color.blue.500`, `space.layout.gutter -> space.6`. Themes (light, dark, brand) change what semantic tokens point to.
3. **Component tokens (optional):** specific to one component, pointing at semantic tokens, such as `button.primary.bg -> color.action.primary.bg`. Add them only where components need independent overrides; they multiply quickly.

## Rules
- **Reference downwards only:** component to semantic to primitive. Components never use primitives directly, or themes break.
- **Semantic tokens carry intent** (what it is for), not appearance ("text.danger", not "text.red").
- **Keep primitives out of the designer's picker** where possible: in Figma, hide primitive variables from publishing and scope semantic ones (see `...figma.scoping-variables-and-setting-code-syntax`).
- **Document** each semantic token: purpose, allowed usage, contrast pairing.
- **Resist token sprawl:** create a component token only after the second need.

## Example mapping (light and dark)
`color.surface.default`: light -> `color.neutral.0`; dark -> `color.neutral.900`.

## Verify
- [ ] No component references a primitive directly.
- [ ] Changing a primitive updates every dependent token as expected.
- [ ] Each semantic token has a stated purpose.
