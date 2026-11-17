---
id: computing-software.web-development.tailwind-css.theming-dark-mode-and-design-tokens
name: theming-dark-mode-and-design-tokens
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, dark-mode, css-variables, design-tokens, theming, tailwind-config, prefers-color-scheme, web-development]
level: advanced
status: verified
description: "Tailwind theming with CSS variables as design tokens, dark-mode strategy (class vs media), and avoiding a brittle multi-theme utility explosion."
sources:
  - https://tailwindcss.com/docs/dark-mode
  - https://tailwindcss.com/docs/theme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailwind theming, dark mode, and design tokens

**Goal:** a theme that supports dark mode (and ideally other themes) without
doubling every colour utility in every component, and tokens that stay in sync
between design and code.

## 1. Dark mode strategy — `class` vs `media`
(The config snippets here target Tailwind v3 and were run on 3.4.19; the v4 CSS-first equivalents are `@custom-variant dark` and `@theme`, see dark-mode-strategies-v4. In v3.4.1+ `darkMode: 'selector'` is the documented form that replaced `'class'`; `'class'` still compiled.)
```js
// tailwind.config.js
module.exports = { darkMode: 'class' }; // toggle by adding .dark to <html>, user-controlled
// vs
module.exports = { darkMode: 'media' }; // follows OS prefers-color-scheme, no manual toggle
```
`media` is zero-JS but gives the user no in-app override. `class` requires a
toggle (usually a small script that sets `document.documentElement.classList`
and persists the choice to `localStorage`) but lets users choose independent
of OS setting — the common production choice. To avoid a flash of the wrong
theme on load, set the class synchronously in an inline `<script>` in `<head>`
*before* the stylesheet paints, not in a framework's mounted lifecycle (which
runs after first paint).

## 2. CSS variables as the actual source of truth, Tailwind utilities as the API
```css
:root { --color-bg: 255 255 255; --color-text: 15 23 42; }
.dark { --color-bg: 15 23 42; --color-text: 241 245 249; }
```
```js
// tailwind.config.js
theme: { extend: { colors: { bg: 'rgb(var(--color-bg) / <alpha-value>)', text: 'rgb(var(--color-text) / <alpha-value>)' } } }
```
Now `bg-bg text-text` resolves to whichever value the active `.dark` class (or
any other theme class) defines — one utility class works across every theme,
instead of writing `bg-white dark:bg-slate-900` on every single element. This
scales to more than two themes (a client white-label, a high-contrast mode)
without touching component markup at all — only the root variable block
changes.

## 3. When `dark:` prefix utilities are still the right call
For one-off overrides that aren't a themeable token (a specific illustration
that needs a different image in dark mode, a border that should disappear
rather than recolor) `dark:hidden`/`dark:block`/`dark:border-none` are fine and
simpler than inventing a token for a one-time case. Reach for the CSS-variable
token approach once you're writing `dark:` on the same handful of colour
classes across dozens of components — that repetition is the signal to
centralize.

## 4. Design tokens beyond color — spacing, radius, type scale
Extend `theme.extend` (never fully override `theme.colors`/`theme.spacing`
unless intentionally dropping Tailwind's defaults) with named tokens that match
the design file: `borderRadius: { card: '12px' }`, `fontSize: { 'display-lg':
['3rem', { lineHeight: '1.1' }] }`. This keeps `rounded-card` and
`text-display-lg` meaningful across the codebase instead of every component
picking its own nearby arbitrary value (`rounded-[13px]` creeping in because
nobody remembers the agreed token).

## 5. Extracting components without losing utility-first benefits
Don't reach for `@apply` to bundle utilities into a new custom class as the
default pattern — it reintroduces the specificity/cascade problems utility-first
CSS exists to avoid, and the resulting class can't be overridden per-instance
with a plain utility the way composed classes can. Prefer a framework
component (`<Button>`) that accepts a `className`/`class` prop merged in
(e.g. via `clsx`/`tailwind-merge` to handle conflicting utilities correctly)
over a Tailwind-level `@apply` abstraction — the logic lives in the component
layer, not the CSS layer.

## Verify
- [ ] Theme class is set synchronously before first paint, no flash of the wrong theme.
- [ ] Repeated `dark:` color pairs are migrated to a CSS-variable-backed token instead of per-component overrides.
- [ ] `theme.extend` is used for custom tokens rather than silently dropping Tailwind's default scale.
- [ ] `tailwind-merge`/`clsx` resolves conflicting utility classes when a component accepts an external `className`.
- [ ] A second theme (if ever added) requires only a new root variable block, not component changes.
