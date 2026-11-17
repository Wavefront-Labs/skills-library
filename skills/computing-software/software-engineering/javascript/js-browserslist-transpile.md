---
id: computing-software.software-engineering.javascript.js-browserslist-transpile
name: js-browserslist-transpile
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, browserslist, js-compat]
level: practitioner
status: draft
description: "Define supported browsers once and let Babel, PostCSS and esbuild follow."
sources: ["https://browsersl.ist/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browserslist and transpilation targets

- Declare in `package.json` `"browserslist": ["defaults", "not dead", ">0.5%"]` or `.browserslistrc`; preview with `npx browserslist`.
- Update the data regularly: `npx update-browserslist-db@latest`.
- Babel `@babel/preset-env` reads it and transpiles syntax; polyfills are separate (`core-js` with `useBuiltIns: "usage"`).
- esbuild/Vite use `target` (e.g. `es2020`); keep it consistent with Browserslist (`browserslist-to-esbuild`).
- Check support: MDN compat tables, caniuse, `eslint-plugin-compat`.
- Decide support by analytics, not guesses.

Self-check: `npx browserslist` output matches the list in your support policy.
