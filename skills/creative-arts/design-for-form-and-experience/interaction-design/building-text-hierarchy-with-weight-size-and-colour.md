---
id: creative-arts.design-for-form-and-experience.interaction-design.building-text-hierarchy-with-weight-size-and-colour
name: building-text-hierarchy-with-weight-size-and-colour
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [text-hierarchy, type-hierarchy, ui-typography, font-weight, typographic-scale, visual-hierarchy]
level: practitioner
status: draft
description: "Build UI text hierarchy using size, weight, colour and spacing: limited levels, mapped to roles, with enough contrast between steps and semantic colour for secondary text."
sources:
  - "Material Design 3 - Typography: type scale tokens (m3.material.io/styles/typography)"
  - "Apple Human Interface Guidelines - Typography (developer.apple.com/design/human-interface-guidelines/typography)"
  - "Refactoring UI, Wathan and Schoger (2018), hierarchy chapter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text hierarchy

**Goal:** readers instantly know what to read first, second and last.

## Levers (use two at a time, not all)
- **Size:** the most obvious step; use a type scale (1.125-1.25 ratio) rather than ad-hoc sizes.
- **Weight:** 400 body, 500-600 labels and subheads, 700 for headings and emphasis; avoid more than 3 weights.
- **Colour/contrast:** primary text near-black (for example #1A1A1A on white), secondary a lighter grey that still passes 4.5:1, tertiary only for non-essential metadata. Do not use low-contrast grey for needed text.
- **Spacing:** space above a heading larger than space below, tying it to its content.
- **Case and tracking:** uppercase small labels with extra letter spacing (0.05-0.1 em) as a minor tier.

## Roles
Define 6-8 roles (Display, Headline, Title, Body, Label, Caption), each with size, weight, line height and letter spacing as tokens (Material 3 names: display, headline, title, body, label x large/medium/small). Map them to HTML semantics (h1-h6, p) and to component slots.

## Procedure
1. Squint test the screen: the order of weight should match the order of importance.
2. Limit to 3 text levels per component (title, body, meta).
3. De-emphasise secondary text with colour and size instead of making everything bold.
4. Keep hierarchy consistent: the same role always looks the same (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`).
5. Check dynamic type or browser text scaling: hierarchy should survive 200 percent.

## Verify
- [ ] No more than 3 levels in a component; no more than 8 text roles in the system.
- [ ] Secondary text passes contrast.
- [ ] Hierarchy intact when blurred and at large text sizes.
