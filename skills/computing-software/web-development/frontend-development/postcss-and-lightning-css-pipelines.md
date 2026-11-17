---
id: computing-software.web-development.frontend-development.postcss-and-lightning-css-pipelines
name: postcss-and-lightning-css-pipelines
category: computing-software
field: web-development
product: frontend-development
tags: [postcss, lightningcss, autoprefixer, postcss-preset-env, css-build-pipeline, browserslist]
level: practitioner
status: verified
description: "CSS build pipelines: PostCSS config and plugin order, Autoprefixer with browserslist, postcss-preset-env, and replacing it with Lightning CSS in Vite for transforms and minify."
sources:
  - https://github.com/postcss/postcss#usage
  - https://lightningcss.dev/docs.html
  - https://vite.dev/guide/features#lightning-css
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostCSS and Lightning CSS pipelines

## 1. PostCSS
```js
// postcss.config.js  (Vite, Next.js, webpack pick it up automatically)
export default {
  plugins: {
    "postcss-import": {},                 // inline @import first
    "postcss-preset-env": { stage: 2, features: { "nesting-rules": true } },
    autoprefixer: {},                     // reads browserslist
    ...(process.env.NODE_ENV === "production" ? { cssnano: { preset: "default" } } : {}),
  },
};
```
Order matters: imports -> syntax lowering -> prefixes -> minify. `postcss-preset-env` already depends on Autoprefixer (its package.json lists it); do not run it twice. In a test, `.a { user-select: none; & .b { color: oklch(...) } }` came out unnested with `-webkit-`/`-moz-` prefixes and an `rgb()` colour.

## 2. Targets
```
# .browserslistrc
> 0.5%, last 2 versions, Firefox ESR, not dead
```
Check with `npx browserslist`. Prefixes and lowering are driven entirely by this list; an over-broad list bloats CSS.

## 3. Lightning CSS (Rust, much faster)
```js
// vite.config.js
import browserslist from "browserslist";
import { browserslistToTargets } from "lightningcss";
export default {
  css: { transformer: "lightningcss", lightningcss: { targets: browserslistToTargets(browserslist(">= 0.25%")) } },
  build: { cssMinify: "lightningcss" },
};
```
Vite already minifies CSS with Lightning CSS by default (Vite docs); `css.transformer: "lightningcss"` (marked experimental) is the opt-in for transforms. In a Vite 8 build it handled nesting, prefixes, `oklch()`/`color-mix()` fallbacks, logical properties, media query ranges and minification in one pass. CLI: `npx lightningcss --minify --targets ">= 0.25%" in.css -o out.css`.
Tailwind v4 uses Lightning CSS internally; with `@tailwindcss/vite` you need neither PostCSS nor Autoprefixer.

## 4. Gotchas
- With `transformer: "lightningcss"` the `postcss.config.js` was not run at all in a test (a marker plugin's output was missing); keep the default transformer if you need PostCSS plugins.
- Lowering cannot polyfill everything: `:has()`, container queries and `@layer` behave natively or not at all.
- Source maps: enable `css.devSourcemap: true` in Vite for debugging.

## Verify
- [ ] Built CSS contains prefixes/fallbacks only for features your targets lack (inspect `dist/*.css`).
