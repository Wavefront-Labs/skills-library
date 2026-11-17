---
id: creative-arts.graphic-design.typography.ui-type-ramps-and-type-tokens
name: ui-type-ramps-and-type-tokens
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, screen-typography, type-tokens, design-tokens, type-ramp, type-scale, figma-text-styles, figma-variables, material-type-scale, ui-typography]
level: practitioner
status: draft
description: "Define a UI type ramp and type tokens: named roles (display to label), size, line height, weight and tracking per role, Figma text styles and variables, and CSS output."
sources:
  - https://m3.material.io/styles/typography/type-scale-tokens
  - https://help.figma.com/hc/en-us/articles/360039957034-Create-and-apply-text-styles
  - https://www.designtokens.org/tr/drafts/format/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UI type ramps and type tokens

**Goal:** a small, named set of text styles that designers pick from in Figma and developers use as tokens,
so product typography is consistent and changeable in one place.

## Define roles, not sizes
Name by role and size step, as Material 3 does: `display-lg/md/sm`, `headline-lg/md/sm`, `title-lg/md/sm`,
`body-lg/md/sm`, `label-lg/md/sm`. Material 3 baseline values (sp/px): body-lg 16/24, body-md 14/20,
body-sm 12/16, label-lg 14/20 weight 500, title-lg 22/28, headline-lg 32/40, display-lg 57/64.

## Each style token holds
- font family (via a token like `font.family.brand`), weight, size, line height, letter spacing, and
  optionally case and paragraph spacing.
- Line heights on a 4 px grid (16/24, 14/20) keep vertical rhythm in components.
- Tracking: slightly negative for large sizes (-0.25 px at 57 px), slightly positive for small labels.

## Token layers
1. **Primitive:** `font.size.16`, `font.weight.medium`, `line-height.24`.
2. **Semantic:** `type.body.md` composed of primitives.
3. Components reference semantic tokens only (`button.label` -> `type.label.lg`).
- Store in the W3C Design Tokens format (typography composite token) and transform with Style Dictionary or
  Tokens Studio to CSS, iOS and Android.

## In Figma
- Create **text styles** per role; use **variables** (number and string) for size, line height and family so
  modes (e.g. compact vs comfortable, brand A vs brand B) swap values.
- Publish in a library; detach checks (Figma's "Find detached" plugins or lint plugins) catch ad hoc text.

## CSS output example
```css
:root { --type-body-md-size: 0.875rem; --type-body-md-line: 1.25rem; --type-body-md-weight: 400; }
.body-md { font: var(--type-body-md-weight) var(--type-body-md-size)/var(--type-body-md-line) var(--font-brand); }
```
- Use rem so user font settings scale the whole ramp; combine with fluid clamp for display sizes.

## Gotchas
- Too many styles (30+) defeat the point; 12-15 covers most products.
- Platform differences: iOS Dynamic Type and Android sp scaling resize text; test at the largest settings.
- Naming by size (`text-14`) breaks when the size changes; name by role.

## Verify
- [ ] Every text layer in the product file uses a published style.
- [ ] Changing one token updates Figma and the built CSS in the same way.
