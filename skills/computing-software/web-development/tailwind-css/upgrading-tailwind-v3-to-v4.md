---
id: computing-software.web-development.tailwind-css.upgrading-tailwind-v3-to-v4
name: upgrading-tailwind-v3-to-v4
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-upgrade, tailwind-v4, tailwind-v3, migration, tailwindcss-upgrade-tool, web-development]
level: practitioner
status: verified
description: "Upgrading a project from Tailwind CSS v3 to v4: the upgrade tool, new build plugins, renamed utilities, changed defaults and a visual-regression plan."
sources:
  - https://tailwindcss.com/docs/upgrade-guide
  - https://tailwindcss.com/blog/tailwindcss-v4
  - https://tailwindcss.com/docs/compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Tailwind CSS v3 to v4

**Goal:** move a v3 codebase to v4 without silent visual regressions.

## 1. Check the floor first
- v4 targets Safari 16.4+, Chrome 111+, Firefox 128+ (it relies on `@property`, `color-mix()`, cascade layers). If you must support older browsers, stay on v3.4.
- The upgrade tool needs Node 20+.
- Sass/Less/Stylus are not supported as pre-processors for Tailwind v4 files; Tailwind is the pre-processor.

## 2. Run the tool on a clean branch
```bash
git switch -c tailwind-v4
npx @tailwindcss/upgrade        # rewrites deps, config, CSS entry and class names in templates
git diff --stat                 # review every file it touched
```
Run on a v3.4.19 sample with the 4.3.3 tool: it rewrote class names in the HTML (`shadow-sm`->`shadow-xs`, `shadow`->`shadow-sm`, `rounded`->`rounded-sm`, `blur`->`blur-sm`, `outline-none`->`outline-hidden`, `ring`->`ring-3`, `!bg-red-500`->`bg-red-500!`, `bg-[--brand]`->`bg-(--brand)`, `first:*:pt-0`->`*:first:pt-0`, `flex-shrink-0`->`shrink-0`, `flex-grow`->`grow`, `overflow-ellipsis`->`text-ellipsis`), moved `theme.extend.colors` into `@theme` and deleted `tailwind.config.js`, added a base-layer rule restoring the `gray-200` border colour, switched the PostCSS plugin to `@tailwindcss/postcss` but left `autoprefixer` in the config, and left `bg-opacity-50` untouched, so grep for leftovers.
It migrates `tailwind.config.js` into CSS `@theme` where it can. If it can't, keep the JS config and load it explicitly:
```css
@import "tailwindcss";
@config "../tailwind.config.js";
```
`corePlugins`, `safelist` and `separator` from JS config are not supported in v4 — use `@source inline(...)` for safelisting.

## 3. Build pipeline changes
| v3 | v4 |
|---|---|
| `@tailwind base; @tailwind components; @tailwind utilities;` | `@import "tailwindcss";` |
| `tailwindcss` PostCSS plugin + `autoprefixer` | `@tailwindcss/postcss` (prefixing and imports built in) |
| `npx tailwindcss -i ...` | `npx @tailwindcss/cli -i ...` |
| Vite via PostCSS | `@tailwindcss/vite` plugin (fastest) |

## 4. Renamed and changed utilities (the tool rewrites most; grep for leftovers)
- Scale shift: `shadow-sm`→`shadow-xs`, `shadow`→`shadow-sm`; same for `blur`, `rounded`, `drop-shadow`, `backdrop-blur` (`rounded`→`rounded-sm`, `rounded-sm`→`rounded-xs`). The bare names still compile (`.shadow` is the old `shadow` value), but an unrenamed `-sm` now looks different.
- `outline-none` → `outline-hidden` (v4 `outline-none` really sets `outline-style: none`).
- `ring` is now 1px (was 3px) and `currentColor`; use `ring-3 ring-blue-500` for the old look.
- The upgrade guide lists `bg-opacity-*` (and the other `*-opacity-*` utilities) as removed → `bg-black/50`; also `flex-shrink-*`→`shrink-*`, `flex-grow-*`→`grow-*`, `overflow-ellipsis`→`text-ellipsis`, `decoration-slice/clone`→`box-decoration-slice/clone`. Run on 4.3.3: `bg-opacity-50` generates no CSS, but `flex-shrink-0`, `flex-grow` and `overflow-ellipsis` still compile, so a build will not flag them.
- Default border colour is `currentColor` (was gray-200): bare `border` now looks darker. Add a base rule or explicit colours.
- `!` important modifier moves to the end: `bg-red-500!`.
- Variants stack left to right: `*:first:pt-0` order matters differently than v3.
- CSS-variable shorthand: `bg-[--brand]` → `bg-(--brand)`.
- `space-y-*`/`space-x-*` selector changed (margin-bottom on `:not(:last-child)`); prefer `flex flex-col gap-*`.
- `hover:` only applies on devices with `@media (hover: hover)`.
- Buttons get `cursor: default`; placeholder text is current colour at 50%.
- `theme()` in CSS → use variables: `var(--color-gray-500)`.

## 5. Component-scoped CSS
Vue/Svelte `<style>` blocks and CSS modules are processed separately, so `@apply` there fails with unknown utilities. Add:
```css
@reference "../../app.css";
.btn { @apply px-4 py-2; }
```

## Verify
- [ ] `grep -rE "bg-opacity|flex-shrink|overflow-ellipsis|outline-none|@tailwind " src` returns nothing unintended.
- [ ] Visual regression (Playwright screenshots / Chromatic) run on key pages before and after; borders, rings and shadows reviewed.
- [ ] Production CSS builds and the bundle contains classes used in templates (spot-check a dynamic one).
