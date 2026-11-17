---
id: creative-arts.design-for-form-and-experience.design-systems.theming-multi-brand-and-multi-mode-tokens
name: theming-multi-brand-and-multi-mode-tokens
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [multi-brand-theming, multi-theme-tokens, theming-tokens, token-modes, dark-mode-tokens, white-label-design-system]
level: advanced
status: draft
description: "Support multiple brands and modes with tokens: separate primitives from semantics, swap semantic mappings per theme, ship CSS variables and Figma modes, and test each combination."
sources:
  - "W3C Design Tokens Community Group (w3.org/community/design-tokens)"
  - "Nathan Curtis, EightShapes articles on design system themes (medium.com/eightshapes-llc)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Multi-brand and multi-theme tokens

Goal: one component library, many looks: light and dark, density, and several brands.

## Architecture
1. **Primitives per brand,** semantics shared: each brand supplies its palette, type and radius primitives; the semantic layer (`color.action.primary.bg`) has the same names in every theme (see `...design-systems.tokens-tiers-primitive-semantic-component`).
2. **Theme = a mapping** from semantic names to primitives. Light, dark and each brand are separate theme files with identical key sets.
3. **Axes:** keep brand, colour mode and density as independent axes where possible so combinations compose rather than multiply files.

## Delivery on the web
- Output each theme as CSS custom properties scoped to a selector (`:root`, `[data-theme="dark"]`, `[data-brand="b"]`) and have components use only `var(--semantic-token)`.
- Respect `prefers-color-scheme` as a default for mode; allow a user override.
- Style Dictionary can build one output per theme from the same sources (see `...design-systems.building-tokens-with-style-dictionary`).

## Delivery in Figma
Use variable collections with modes: one collection per axis, or a collection with brand modes (see `...figma.collections-and-modes-in-figma-variables`). Frames can be set to a mode, so you can preview each theme in one file.

## Test
- Check each theme against contrast targets (see `...interaction-design.checking-colour-contrast`).
- Run visual regression across theme combinations (see `...design-systems.visual-regression-testing-for-components`).
- Fail the build when a theme lacks a semantic token that another theme defines.

## Verify
- [ ] Every theme defines the same semantic keys.
- [ ] Components contain no hard-coded colours.
- [ ] Contrast was verified per theme.
