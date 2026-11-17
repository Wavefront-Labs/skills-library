---
id: computing-software.web-development.frontend-development.dynamic-import-and-lazy-loading
name: dynamic-import-and-lazy-loading
category: computing-software
field: web-development
product: frontend-development
tags: [es-modules, javascript-modules, dynamic-import, lazy-loading-modules, code-splitting, chunk-load-error, import-on-interaction]
level: practitioner
status: docs-checked
description: "Loading code on demand with dynamic import(): route and interaction-based splitting, preloading, error handling for failed chunks, and bundler hints."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import
  - https://vite.dev/guide/build#load-error-handling
  - https://vite.dev/guide/features#dynamic-import
  - https://vite.dev/guide/features#glob-import
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic import and lazy loading

**Goal:** ship only what the first screen needs and fetch the rest when the user is about to need it.

## 1. Basics
```js
button.addEventListener('click', async () => {
  const { openEditor } = await import('./editor.js');   // separate chunk
  openEditor();
});
```
`import()` returns a promise of the module namespace and works in non-module scripts too. Bundlers such as Vite split a chunk at each `import()`.

## 2. What to split
- Routes/pages (framework routers do this).
- Heavy, interaction-gated features: editors, charts, maps, date pickers, PDF export.
- Polyfills only browsers need (`if (!('IntersectionObserver' in window)) await import(…)`).
Don't split tiny modules: each chunk is a request plus a waterfall step.

## 3. Hide the latency
- Preload on intent: `pointerenter`/`focus` on the trigger calls `import('./editor.js')` (the promise is cached; the click awaits the same one).
- `<link rel="modulepreload" href="/assets/editor.js">` when you know it'll be needed soon.
- Idle prefetch: start `import('./settings.js')` from an idle callback.

## 4. Variables in specifiers
`import(\`./locales/${lang}.js\`)` - Vite supports dynamic import with variables (see its Dynamic Import section for the restrictions). Vite: `import.meta.glob('./locales/*.js')` gives explicit control; matched files are lazy-loaded by default and the arguments must be literals.

## 5. Failed chunk loads
After a deploy, old pages may request deleted chunk files: a failed dynamic import (the exact error text varies by browser and bundler). Mitigate: keep old assets for a few days; catch and offer reload:
```js
try { mod = await import('./editor.js'); }
catch { if (confirm('A new version is available. Reload?')) location.reload(); }
```
Vite emits a `vite:preloadError` event on `window` when it fails to load a dynamic import; calling `event.preventDefault()` stops the error being thrown.

## Verify
- [ ] Network panel: editor chunk loads only after hover/click.
- [ ] Initial JS for the landing page dropped by the expected amount (bundle analyzer).
- [ ] Simulate a 404 on a chunk: user sees a recovery prompt, not a blank screen.

## Checked

2026-10-26. MDN `import()` (loads a module asynchronously into a possibly non-module environment) and the Vite guides read from the vitejs/vite docs (vite:preloadError and preventDefault, dynamic import with variables, import.meta.glob lazy by default with literal arguments). Removed the unconfirmed webpack, ChunkLoadError and bundle-size statements.

Method: documentation only; no commands were run.
