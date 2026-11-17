---
id: creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale
name: design-tokens-and-a-modular-type-scale
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [design-systems, design-system, design-tokens, tokens, primitive-tokens, semantic-tokens, component-tokens, alias-tokens, colour-palette, color-tokens, dark-mode, theming, type-scale, modular-scale, typography, line-height, spacing-scale, 4pt-grid, 8pt-grid, figma-variables, style-dictionary, w3c-design-tokens, dtcg, css-custom-properties, naming-conventions, governance, versioning, component-library]
level: practitioner
status: draft
description: "Set up a design system's foundations: three tiers of tokens (primitive, semantic, component), sensible naming, a modular type scale and spacing scale, and theming like dark mode via semantic aliases."
sources:
  - "W3C Design Tokens Community Group (DTCG), Design Tokens Format Module (draft specification)"
  - "Kholmatova, Design Systems (Smashing Magazine)"
  - "Figma documentation on variables and modes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design tokens and a modular type scale

**Goal:** give a product a visual language that stays consistent as it grows: every
colour, size and space comes from a small named set of **tokens**, so design files and
code share one source of truth and a theme change (dark mode, a sub-brand) is a remap,
not a redesign.

> **Status: draft.** The three-tier model is the prevailing convention (Material,
> Salesforce Lightning, Adobe Spectrum, and the W3C DTCG draft). The DTCG format was still a
> draft specification at time of writing — check its current status before committing to it.

## 1. Three tiers of tokens
1. **Primitive (global) tokens** — raw values with descriptive names, no meaning:
   `color.blue.500 = #2563EB`, `space.4 = 16px`, `font.size.300 = 20px`.
2. **Semantic (alias) tokens** — what a value is **for**, pointing at primitives:
   `color.text.default → color.grey.900`, `color.bg.surface → color.white`,
   `color.action.primary → color.blue.600`, `color.feedback.error → color.red.600`.
3. **Component tokens** (optional, for large systems): `button.primary.bg →
   color.action.primary`.

**Components use only semantic or component tokens, never primitives.** That's what makes
theming work: dark mode remaps `color.bg.surface → color.grey.950` and every component follows.

## 2. Naming
Pick a pattern and enforce it: `category.property.variant.state`, e.g.
`color.text.subtle`, `color.border.focus`, `color.action.primary.hover`.
- Names describe purpose, not appearance (`color.feedback.error`, not `color.red-text`).
- Avoid names tied to one component in the semantic tier.
- Keep the set small: dozens of semantic colours, not hundreds.

## 3. Colour palette
- Build each hue as a ramp (e.g. 50–950), checking that key pairs pass contrast:
  body text on surface ≥4.5:1; UI boundaries ≥3:1.
- Define semantic roles: text (default, subtle, inverse), backgrounds (surface, raised,
  sunken), border, action (primary, secondary), feedback (info, success, warning, error),
  focus.
- For dark mode, don't simply invert: reduce saturation of bright colours, use lighter
  surfaces to show elevation, re-check every contrast pair.

## 4. A modular type scale
- Choose a **base size** (16 px for body on web is the common default) and a **ratio**:
  1.125 (major second, tight, dense UIs), 1.2 (minor third), 1.25 (major third), 1.333
  (perfect fourth, expressive marketing).
- Generate steps: base × ratio^n. With 16 px and 1.25: 12.8, **16**, 20, 25, 31.25, 39 →
  round to 13, 16, 20, 25, 31, 39.
- Name them as tokens (`font.size.100`… or `text.body`, `text.heading.lg`) and pair each
  with a **line height** (body ~1.4–1.6; large headings ~1.1–1.25) and letter-spacing.
- Limit to ~6–8 sizes. More means nobody knows which to use.
- Consider fluid type (CSS `clamp()`) for headings across breakpoints.

## 5. Spacing scale
A 4 px base with an 8-ish rhythm: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64. Tokens like
`space.100 = 4px`, `space.200 = 8px`. Use them for padding, gaps and layout margins; avoid
one-off values.

## 6. Tooling and governance
- **Figma variables** with **modes** (light/dark, brand A/B) for primitives and semantics.
- Export to code via a token pipeline (e.g. Style Dictionary or similar) producing CSS
  custom properties, iOS/Android resources.
- One owner; changes through a request process; **version** the token package and write a
  changelog. Deprecate tokens before deleting.

## Gotchas
- Components referencing primitives → dark mode needs every component edited.
- Too many semantic tokens nobody can choose between.
- Type scale chosen in Figma but not mapped to code → drift within weeks.
- Contrast checked in light mode only.

## Verify
- [ ] Primitive, semantic (and optionally component) tiers exist; components use semantic only.
- [ ] Naming convention documented and applied.
- [ ] Key colour pairs pass contrast in all themes.
- [ ] Type scale has base, ratio, 6–8 steps with line heights.
- [ ] Spacing scale defined; tokens exported to code from one source and versioned.
