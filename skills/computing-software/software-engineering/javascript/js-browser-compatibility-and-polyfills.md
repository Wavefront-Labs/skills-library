---
id: computing-software.software-engineering.javascript.js-browser-compatibility-and-polyfills
name: js-browser-compatibility-and-polyfills
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-browser-compat, browserslist, feature-detection, polyfills, caniuse]
level: practitioner
status: draft
description: "Decide what to ship for target browsers using Browserslist, feature detection and polyfills."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser compatibility

- Define targets once in `package.json` `"browserslist"` or `.browserslistrc` (for example `defaults and fully supports es6-module`); Babel/preset-env, SWC, esbuild and autoprefixer read it.
- Check support on MDN compatibility tables and caniuse; the Baseline label summarises cross-browser availability.
- Feature-detect, not user-agent-sniff: `if ("IntersectionObserver" in window)`, `typeof structuredClone === "function"`, `CSS.supports(...)`.
- Syntax is transpiled by build tools; APIs (new methods, `fetch`, `Promise`) need polyfills: load via core-js with `useBuiltIns: "usage"` or a targeted import, and keep bundles small by raising the targets.
- Use `<script type="module">` with `nomodule` fallback only if you still support browsers that lack modules.
- Test on real engines (Chromium, Firefox, WebKit) with Playwright; Safari/WebKit lag is the usual surprise.
