---
id: computing-software.web-development.frontend-development.modulepreload-and-module-loading
name: modulepreload-and-module-loading
category: computing-software
field: web-development
product: frontend-development
tags: [modulepreload, module-scripts, script-type-module, import-waterfall, javascript-modules]
level: practitioner
status: docs-checked
description: "How browsers load module scripts (deferred, CORS, import waterfalls) and using link rel=modulepreload and bundler preload settings to flatten dependency chains."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/modulepreload
  - https://vite.dev/config/build-options#build-modulepreload
  - https://github.com/rails/importmap-rails#preloading-pinned-modules
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# modulepreload and module loading

## 1. How module scripts load
- `<script type="module">` is **deferred by default**: fetched in parallel, executed after parsing, in document order. `async` makes it run as soon as it and its graph are ready.
- Module scripts load in CORS mode, so cross-origin modules need CORS headers; use matching `crossorigin` on the preload.
- Each `import` is discovered only after the parent is fetched and parsed: a 4-deep chain = 4 round trips (the waterfall).

## 2. modulepreload
```html
<link rel="modulepreload" href="/assets/app.js">
<link rel="modulepreload" href="/assets/vendor-react.js">
<script type="module" src="/assets/app.js"></script>
```
It is the module-specific form of preload: list each module on the critical chain you want fetched early. Per browser-compat-data: Chrome 66, Firefox 115, Safari 17.

## 3. Bundlers
- Vite computes the list of chunks to preload for each dynamic import and injects a modulepreload polyfill by default (`build.modulePreload`, disable with `{ polyfill: false }`).
- Unbundled ESM relies on `modulepreload` to avoid waterfalls; importmap-rails emits modulepreload links for pins and `pin "name", preload: false` opts a pin out.

## Gotchas
- Preloading things not used soon wastes bandwidth; preload only the critical path.
- Match the `crossorigin` attribute between the preload and the script so the cached response is reused.
- Loading module scripts from a `file://` page hits CORS errors; serve over http.

## Verify
- [ ] Network waterfall: dependent modules start in parallel, not after their parent finishes.
- [ ] No unused-preload warnings in the browser console.

## Checked

2026-10-26. MDN modulepreload and Modules guide (deferred automatically; CORS on file://), browser-compat-data (Chrome 66, Firefox 115, Safari 17), Vite build.modulePreload docs and the importmap-rails README (modulepreload links; `preload: false`). Removed the unconfirmed rel=preload comparison, double-download, LCP and manifest statements.

Method: documentation only; no commands were run.
