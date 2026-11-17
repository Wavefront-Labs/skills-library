---
id: creative-arts.graphic-design.brand-identity.brand-libraries-and-design-tokens
name: brand-libraries-and-design-tokens
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, brand-assets, brand-library, design-tokens, figma-library, figma-variables, style-dictionary, tokens-studio, cc-libraries, design-system]
level: advanced
status: draft
description: "Turn a brand into shared libraries and design tokens: Figma and CC libraries, primitive and semantic tokens for colour, type and spacing, and exporting them to code."
sources:
  - https://www.designtokens.org/tr/drafts/format/
  - https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma
  - https://styledictionary.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared libraries and design tokens for brand

**Goal:** brand decisions (colours, type, spacing, radii, logos) stored once as named tokens and library
assets, consumed by design tools and code, so the brand updates everywhere together.

## Libraries
- **Figma:** a brand foundations file published as a library: colour and typography styles or variables,
  logo components (variants for version and colour), icons, graphic devices. Teams enable the library.
- **Adobe:** CC Libraries for print teams (see cc-libraries-for-brand-assets).
- Keep one source of truth: generate Adobe swatches from the same token values.

## Token layers
1. **Primitive (core):** raw values. `color.red.500 = #D62828`, `space.4 = 16px`, `font.family.sans = "Brand Sans"`.
2. **Semantic (alias):** intent. `color.action.primary = {color.red.500}`, `color.text.default = {color.grey.900}`.
3. **Component:** `button.primary.background = {color.action.primary}`.
- Modes for light/dark or sub-brands swap semantic values, not primitives.

## Format and pipeline
- W3C Design Tokens Community Group format (JSON with `$value`, `$type`):
```json
{ "color": { "red": { "500": { "$value": "#D62828", "$type": "color" } },
  "action": { "primary": { "$value": "{color.red.500}", "$type": "color" } } } }
```
- Manage in Figma variables, or Tokens Studio (syncs JSON with Git), then build with **Style Dictionary** to CSS
  custom properties, SCSS, iOS (Swift), Android (XML/Compose).
- Version tokens like code (semver); publish changes with release notes.

## Gotchas
- Naming by colour value (`red`) in semantic tokens breaks when the brand colour changes; name by role.
- Print colours (Pantone, CMYK) do not belong in screen tokens; store them as separate metadata.
- Library updates are opt-in per Figma file; communicate releases.

## Verify
- [ ] One token change flows to Figma and to built CSS output.
- [ ] Semantic tokens cover every UI use; components never reference primitives directly.
