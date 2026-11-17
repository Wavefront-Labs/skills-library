---
id: computing-software.web-development.web-performance.differential-serving-and-legacy-polyfills
name: differential-serving-and-legacy-polyfills
category: computing-software
field: web-development
product: web-performance
tags: [differential-serving, legacy-polyfills, browserslist, baseline, javascript-performance]
level: practitioner
status: docs-checked
description: "Shipping less JavaScript to modern browsers: auditing legacy polyfills, modern browserslist targets, module/nomodule history, and when a legacy bundle pays off."
sources:
  - https://web.dev/articles/publish-modern-javascript
  - https://developer.chrome.com/docs/lighthouse/performance/legacy-javascript-insight
  - https://web-platform-dx.github.io/web-features/
  - https://github.com/vitejs/vite/tree/main/packages/plugin-legacy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differential serving and dropping legacy polyfills

Transpiling to ES5 and bundling core-js polyfills adds JS weight to every user to support a shrinking minority.

## 1. Audit what you ship
- Lighthouse's "Legacy JavaScript" insight flags polyfills and transforms that modern browsers don't need.
- Bundle analyser: search for `core-js` and `regenerator-runtime`.
- Third-party dependencies often ship pre-transpiled ES5; prefer packages with ESM/modern builds.

## 2. Set modern targets
```
# .browserslistrc - explicit modern targets (example versions; choose from your analytics)
chrome >= 111, edge >= 111, firefox >= 114, safari >= 16.4
```
- In Vite, set `build.target`; for `@vitejs/plugin-legacy`, `modernTargets` controls the modern chunk's polyfills.
- Check analytics for actual browser share before deciding (CrUX, your RUM).

## 3. Differential serving (if you must support old browsers)
- Historical pattern: `<script type="module" src="modern.js">` + `<script nomodule src="legacy.js">` - modern browsers ignore `nomodule`.
- `@vitejs/plugin-legacy` generates a legacy chunk for every chunk plus a polyfill chunk with the SystemJS runtime, and injects `<script nomodule>` tags so they load only in browsers without the needed features; `renderModernChunks` and `modernPolyfills` control the modern side.
- Don't do UA-sniffing to pick bundles; caches and spoofed UAs make it fragile.

## 4. Feature-detect instead of polyfill-everything
Load a polyfill only when needed:
```js
if (!("groupBy" in Object)) await import("core-js/actual/object/group-by");
```

## Verify
- [ ] Legacy JavaScript insight shows no significant savings; core-js footprint in the modern bundle near zero; browser-support policy documented and matches analytics.

## Checked

2026-10-28. Confirmed from the `@vitejs/plugin-legacy` README (legacy chunks, SystemJS runtime, `nomodule` tags, `modernTargets`, `renderModernChunks`, `modernPolyfills`, core-js and regenerator-runtime). Removed (not found): the 20-40% figure, whatwg-fetch and es6-promise, the 30-month Baseline definition, the Browserslist and Vite Baseline defaults, Babel `useBuiltIns` advice and the IE11/Safari version claims. The browserslist versions are labelled as an example.

Method: documentation only; no commands were run.
