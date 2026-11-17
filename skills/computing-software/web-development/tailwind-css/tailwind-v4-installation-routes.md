---
id: computing-software.web-development.tailwind-css.tailwind-v4-installation-routes
name: tailwind-v4-installation-routes
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind-vite-plugin, tailwind-cli, tailwind-postcss, tailwind-play-cdn, tailwind-v4, tailwind]
level: practitioner
status: verified
description: "Installing Tailwind CSS v4 the right way per stack: Vite plugin, PostCSS plugin, standalone CLI and Play CDN, browser support limits, and loading a legacy JS config."
sources:
  - https://tailwindcss.com/docs/installation/using-vite
  - https://tailwindcss.com/docs/installation/using-postcss
  - https://tailwindcss.com/docs/compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailwind v4 installation routes

All routes end with one CSS entry: `@import "tailwindcss";`. No `tailwind.config.js` is needed; configuration lives in CSS (`@theme`, `@source`, `@utility`).

## 1. Vite (fastest for Vite-based apps; the Tailwind guides on this route cover Laravel, SvelteKit, React Router, Nuxt and SolidJS)
```bash
npm i tailwindcss @tailwindcss/vite
```
```js
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({ plugins: [tailwindcss()] });
```

## 2. PostCSS (Next.js, webpack, other PostCSS pipelines)
```bash
npm i tailwindcss @tailwindcss/postcss postcss
```
```js
// postcss.config.mjs
export default { plugins: { "@tailwindcss/postcss": {} } };
```
Remove `autoprefixer` and `postcss-import`: v4 handles prefixes and imports itself (via Lightning CSS).

## 3. Standalone CLI (no bundler: Django, Rails, Go, static sites)
```bash
npx @tailwindcss/cli -i ./src/input.css -o ./static/app.css --watch
npx @tailwindcss/cli -i ./src/input.css -o ./static/app.css --minify     # production
```
Other flags (`--help` on 4.3.3): `-m` for `--minify`, `--optimize` (optimise without minifying), `--map`, `--poll`. A standalone executable (no Node) is published on GitHub releases. `tailwindcss-rails` (via the `tailwindcss-ruby` gem), `pytailwindcss` (pip) and `django-tailwind-cli` wrap it; `django-tailwind` offers a standalone-binary mode or an npm mode.

## 4. Play CDN (prototypes only)
```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<style type="text/tailwindcss">@theme { --color-brand: oklch(55% .2 270); }</style>
```
Generates CSS at runtime in the browser; never use in production.

## 5. Browser support and legacy config
- v4 targets Safari 16.4+, Chrome 111+, Firefox 128+ (the v4 announcement says it is built on cascade layers, `@property` and `color-mix()`). Need older browsers: stay on v3.4.
- Migrating projects can keep a JS config temporarily with `@config "../tailwind.config.js";` in the CSS entry (run on 4.3.3: a `theme.extend.colors.legacy` entry compiled to `bg-legacy`); `npx @tailwindcss/upgrade` automates most of v3 -> v4.

## Verify
- [ ] Build output contains only used utilities; a class added in a template appears after save in dev.
