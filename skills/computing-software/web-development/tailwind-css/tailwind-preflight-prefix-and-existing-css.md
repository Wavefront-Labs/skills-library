---
id: computing-software.web-development.tailwind-css.tailwind-preflight-prefix-and-existing-css
name: tailwind-preflight-prefix-and-existing-css
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-preflight, tailwind-prefix, important-modifier, cascade-layers, legacy-css, integration, web-development]
level: practitioner
status: verified
description: "Adding Tailwind to an app that already has CSS or a component library: prefixing, disabling or scoping Preflight, important strategy and layer ordering."
sources:
  - https://tailwindcss.com/docs/preflight
  - https://tailwindcss.com/docs/styling-with-utility-classes#using-the-important-modifier
  - https://tailwindcss.com/docs/installation/framework-guides
  - https://tailwindcss.com/docs/upgrade-guide#using-a-prefix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailwind alongside existing CSS: Preflight, prefix and precedence

**Goal:** introduce Tailwind incrementally into a codebase with Bootstrap/legacy CSS/a component library without breaking existing screens.

## 1. Decide about Preflight
Preflight resets margins, makes images `display: block`, strips list styles and heading sizes. On a legacy page that is a site-wide visual change.

v4 - import the layers without Preflight:
```css
@layer theme, base, components, utilities;
@import "tailwindcss/theme.css" layer(theme);
/* @import "tailwindcss/preflight.css" layer(base);   <- omitted */
@import "tailwindcss/utilities.css" layer(utilities);
```
v3: `corePlugins: { preflight: false }` (run on 3.4.19: no `box-sizing` reset in the output). Omitting the preflight import in v4 likewise left the reset out (run).

Middle ground: keep Preflight but scope new UI inside a container and leave old pages on a separate stylesheet entry.

## 2. Prefix to avoid class collisions
Collisions are real: Bootstrap 5.3.8 and Tailwind 4.3.3 both define `.container`, `.collapse`, `.visible`, `.invisible`, `.shadow`, `.border` and `.rounded` (checked in both stylesheets); Bootstrap 5 has no `.hidden`.
```css
@import "tailwindcss" prefix(tw);   /* v4: classes become tw:flex, tw:hover:bg-red-500 */
```
v4 prefixes look like a variant and come first. v3: `prefix: 'tw-'` → `tw-flex`, `hover:tw-bg-red-500`. v4 prefixes the theme variables too: the generated CSS uses `--tw-color-red-500` (docs and run on 4.3.3). With prefix `tw` on 4.3.3, `tw:bg-red-500!` is the important form.

## 3. Winning against existing CSS
Tailwind v4 puts utilities in `@layer utilities`. Unlayered legacy CSS beats **any** layered CSS regardless of specificity. Options:
- Wrap legacy CSS in a layer declared before utilities: `@import "legacy.css" layer(legacy);` with `@layer theme, base, legacy, components, utilities;`.
- Or mark all utilities important: `@import "tailwindcss" important;` (v4) / `important: true` or `important: '#app'` (v3, selector strategy keeps specificity scoped).
- One-off: `bg-red-500!` (v4) / `!bg-red-500` (v3).

## 4. Framework wiring
- Vite: `@tailwindcss/vite`; Next.js/others: `@tailwindcss/postcss` in `postcss.config.mjs`.
- Make sure only one entry imports `tailwindcss`; double imports duplicate the whole utility layer.
- Component libraries with their own styles (MUI, Ant): load their CSS in a lower layer or use the important strategy.

## Verify
- [ ] Screenshots of legacy pages unchanged after adding Tailwind.
- [ ] No class-name collisions: grep compiled CSS for `.container`/`.collapse` defined twice.
- [ ] A utility applied over a legacy class actually wins (inspect computed style).
