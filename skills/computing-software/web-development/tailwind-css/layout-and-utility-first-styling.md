---
id: computing-software.web-development.tailwind-css.layout-and-utility-first-styling
name: layout-and-utility-first-styling
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwindcss, tailwind-v4, tailwind-v3, css, utility-first, flexbox, css-grid, layout, responsive, mobile-first, breakpoints, theme, design-tokens, css-variables, tailwind-config, dynamic-classes, purge, safelist, apply, container-queries, dark-mode, prefers-color-scheme, custom-variant, clsx, tailwind-merge, cva, web-development]
level: practitioner
status: docs-checked
description: "Tailwind and modern CSS layout: flex and grid, mobile-first prefixes, v4 @theme vs v3 config, design tokens, dynamic class purge gotcha, @apply, container queries, dark mode."
sources:
  - https://tailwindcss.com/docs/upgrade-guide
  - https://tailwindcss.com/docs/theme
  - https://tailwindcss.com/docs/responsive-design
  - https://tailwindcss.com/docs/dark-mode
  - https://tailwindcss.com/docs/detecting-classes-in-source-files
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layout and utility-first styling with Tailwind — tokens in one place, classes in markup

**Goal:** build layouts with flex/grid utilities, keep design decisions in theme tokens,
and avoid the handful of Tailwind gotchas that make styles silently disappear.

## 1. Know your major version
Run `npm ls tailwindcss`. **v4** is CSS-first: no
`tailwind.config.js` by default and automatic source detection (JS config files still work
but are no longer detected automatically; load one with `@config`).
**v3** uses `tailwind.config.js`. Tutorials mix the two; the
upgrade guide lists renamed utilities (e.g. `shadow-sm` → `shadow-xs`,
`outline-none` → `outline-hidden`). Run `npx @tailwindcss/upgrade` to migrate.

```css
/* v4: app.css */
@import "tailwindcss";
@theme {
  --color-brand-500: oklch(0.62 0.19 255);
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 112rem;
}
```
Each `@theme` variable creates utilities (`bg-brand-500`, `font-display`, `3xl:`) **and** a
real CSS variable you can use anywhere: `var(--color-brand-500)`.


## 2. Layout recipes
```html
<!-- Header: logo left, nav right, vertically centred -->
<header class="flex items-center justify-between gap-4 px-4 py-3">…</header>

<!-- Card grid: 1 col on phones, auto-fill at ≥ 16rem per card -->
<ul class="grid grid-cols-1 gap-6 sm:grid-cols-[repeat(auto-fill,minmax(16rem,1fr))]">…</ul>

<!-- Sidebar layout -->
<div class="grid min-h-dvh grid-cols-1 md:grid-cols-[16rem_1fr]">…</div>

<!-- Prevent flex child overflow with long text -->
<div class="flex"><p class="min-w-0 flex-1 truncate">…</p></div>
```
Use `gap-*` instead of margins between children; add `min-w-0` when text refuses to shrink.

## 3. Responsive is mobile-first
Unprefixed = all sizes; `md:` = **min-width** 48rem (768px) and up. `md:` does not mean "on
tablets only". Default breakpoints: `sm` 40rem, `md` 48rem, `lg` 64rem, `xl` 80rem, `2xl`
96rem. Range: `md:max-lg:hidden`. Write the phone layout first, then add larger prefixes.

## 4. The dynamic class name gotcha
Tailwind scans source files as plain text for complete class names. It never runs your code.
```jsx
<div className={`bg-${color}-500`} />            // ✘ never generated
const bg = { red: 'bg-red-500', green: 'bg-green-500' };
<div className={bg[color]} />                     // ✔ full strings appear in source
```
Classes from a CMS or database need safelisting: v4 has no `safelist` option, so use
`@source inline("bg-red-500 bg-green-500")` or point `@source` at the files that contain them. Files outside detected sources (e.g. a UI package in
`node_modules`, which is ignored) need `@source "../node_modules/my-ui";`.

## 5. Components, not @apply
Reuse via components/partials (`<Button>`), not by moving utilities into CSS. `@apply` is fine
for third-party markup you don't control or tiny base styles. In v4, CSS modules and
component `<style>` blocks need `@reference "../app.css";` before `@apply` can see your theme.
For variant-heavy components, `cva` plus `tailwind-merge` (`twMerge`) is a common way to resolve conflicting
classes such as `p-2` vs `p-4` (third-party libraries; not covered by the Tailwind docs).

## 6. Container queries
Style a component by its container's width, not the viewport:
```html
<div class="@container">
  <article class="flex flex-col @md:flex-row">…</article>
</div>
```
Built into v4. Container sizes follow the `--container-*` theme variables (`--container-md` is 28rem); name containers with `@container/name` and target them with `@md/name`.

## 7. Dark mode
Default `dark:` follows `prefers-color-scheme`. For a user toggle with a `.dark` class:
- v4: `@custom-variant dark (&:where(.dark, .dark *));`

Better still, define semantic tokens (`--color-surface`, `--color-text`) and swap their values
under `.dark`, so components use `bg-surface` and never need `dark:` on every element. Set
the class before first paint (inline script in `<head>`) to avoid a light flash.

## Checked

2026-11-01. Confirmed against the Tailwind docs source (tailwindcss.com repo): renamed utilities and the upgrade tool (upgrade guide), `@theme` breakpoints and `--container-md` (theme), default breakpoints and `md:max-lg:` ranges (responsive design), `@custom-variant dark` and `prefers-color-scheme` default (dark mode), `@source`, `@source inline()` and `node_modules` ignored (detecting classes), `@reference`. Removed: release date, v4.1 claim, v3 config and dark-mode/container-plugin details, engine speed, flex min-width explanation, twMerge ordering claim.

Method: documentation only; no commands were run.

## Verify
- [ ] You know which Tailwind major the project uses and the config matches it.
- [ ] Production build contains every class used (search the built CSS for one dynamic class).
- [ ] No string-built class names; variant maps hold full class strings.
- [ ] Layout checked at 320px, each breakpoint and very wide screens; no horizontal scroll.
- [ ] Colours/spacing come from theme tokens, not arbitrary values like `bg-[#3a7]` scattered around.
- [ ] Dark mode has no flash on reload and meets contrast in both themes.
