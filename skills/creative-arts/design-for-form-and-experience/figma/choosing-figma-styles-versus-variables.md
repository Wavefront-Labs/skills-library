---
id: creative-arts.design-for-form-and-experience.figma.choosing-figma-styles-versus-variables
name: choosing-figma-styles-versus-variables
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [styles-vs-variables, figma-variables, styles, tokens, theming, modes, figma-design-tokens, figma]
level: practitioner
status: draft
description: "Decide between Figma styles and variables: variables for values, modes and logic; styles for composite typography, effects and gradients; migration and token mapping."
sources:
  - "Figma Help Center - Guide to variables and Variables vs styles (help.figma.com/hc/en-us/articles/15339657135383)"
  - "Figma Config 2023 and 2024 - Variables and Schema talks (config.figma.com)"
  - "Design Tokens Community Group - Format spec (design-tokens.github.io/community-group/format)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Styles versus variables

## What each does best
- **Variables** (collections with modes): **colour, number, string, boolean** values; **modes** (Light/Dark, Brand A/B, Compact/Comfortable, languages); **aliases** (semantic references primitive); bind to fills, strokes, corner radius, spacing (padding, gap), sizes, text content, visibility, and component properties; usable in **prototype logic** (`creative-arts.design-for-form-and-experience.figma.conditional-logic-in-prototypes`); exposed via the **REST API** for sync (`creative-arts.design-for-form-and-experience.figma.figma-rest-api-file-access`).
- **Styles:** composite properties that variables cannot bundle: **text styles** (font family, size, weight, line height together), **effect styles** (shadows, blurs), **gradients and image paints**, **grid styles**. Styles have no modes; theming needs duplicate styles.

## Rule of thumb
1. **Single values** that change by theme or need to be tokenised: **variables** (colour, spacing, radius, breakpoints).
2. **Composite or visual recipes:** **styles** for typography and effects; bind individual text properties to number/string variables where supported for responsive type, but keep the style as the unit applied to layers.
3. **Theming:** variable modes on collections (Light/Dark) switch whole screens by setting the mode on a frame or section; use **semantic variables** in components and **primitive variables** only inside the semantic mapping.

## Migrating from styles to variables
1. Audit colour styles; create a **Primitives** collection (palette) and **Semantic** collection with modes, aliasing primitives.
2. Bind component fills and strokes to semantic variables; remove old colour styles after consumers migrate (deprecation period; `creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging`).
3. Keep text and effect styles; add number variables for spacing, radius, and font sizes if you need modes.
4. Publish the variable collections with the library; document naming and the mode strategy.
5. Map to code through the token pipeline (`creative-arts.design-for-form-and-experience.design-systems.building-a-token-sync-pipeline`).

## Gotchas
- Variables cannot be applied to everything (for example gradient stops use variable colours but the gradient itself is a paint).
- Hard-coded values inside components defeat modes; lint with plugins.

## Verify
- [ ] Single values use variables; composites use styles, with a written rule.
- [ ] Mode switching re-themes components fully.
- [ ] Migration plan includes deprecation and code mapping.
