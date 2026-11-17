---
id: computing-software.web-development.htmx.htmx-migrate-1-to-2
name: htmx-migrate-1-to-2
category: computing-software
field: web-development
product: htmx
tags: [htmx, migration, htmx-2, htmx-1-compat, hx-on, config, extensions]
level: practitioner
status: docs-checked
description: "Upgrade htmx 1.x to 2.x: module files, extensions split out, config reverts (smooth scroll, DELETE params, cross-domain), hx-on: syntax, htmx-1-compat."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/migration-guide-htmx-1.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/htmx-1-compat.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a site from htmx 1.x to 2.x with the least breakage.

Checklist
1. Modules: 2.x ships `/dist/htmx.esm.js`, `/dist/htmx.amd.js` and `/dist/htmx.cjs.js`; `/dist/htmx.js` is still browser-loadable.
2. Extensions are no longer in core; each is distributed separately. Many 1.x extensions still work, but the SSE extension must be upgraded to its 2.x version, and upgrading all of them is recommended.
3. Replace the legacy `hx-ws` and `hx-sse` attributes with the WS and SSE extensions (see htmx-ext-websockets and htmx-ext-sse).
4. Defaults changed. To restore the 1.x behaviour:
   - smooth scrolling: `htmx.config.scrollBehavior = 'smooth'`
   - form-encoded `DELETE` body: `htmx.config.methodsThatUseUrlParams = ["get"]` (in 2.x, `DELETE` uses URL parameters like `GET`, per the HTTP spec)
   - cross-domain requests: `htmx.config.selfRequestsOnly = false`
5. Convert `hx-on` to `hx-on:`, using the kebab-case event name because HTML attributes are case-insensitive:

```html
<!-- 1.x -->
<button hx-get="/info" hx-on="htmx:beforeRequest: alert('Making a request!')
                              htmx:afterRequest: alert('Done making a request!')">Get Info!</button>
<!-- 2.x -->
<button hx-get="/info" hx-on:htmx:before-request="alert('Making a request!')"
                       hx-on:htmx:after-request="alert('Done making a request!')">Get Info!</button>
```
6. `htmx.makeFragment()` now always returns a `DocumentFragment`.
7. Extension authors: internal `selectAndSwap` is removed; use `swap`, available in both the internal and public API:

```js
let content = "<div>Hello world</div>";
let target = api.getTarget(child);
let swapSpec = api.getSwapSpecification(child);
api.swap(target, content, swapSpec);
```
8. IE is no longer supported; htmx 1.x continues to support it.

Shortcut: the `htmx-1-compat` extension restores most of the breaking changes. Load it after core htmx (CDN example `https://cdn.jsdelivr.net/npm/htmx-ext-htmx-1-compat@2.0.2`, npm `htmx-ext-htmx-1-compat`) and set `<body hx-ext="htmx-1-compat">`. It restores:
- the `hx-ws`, `hx-sse` and old `hx-on` attributes;
- `scrollBehavior` of `'smooth'`, form-encoded `DELETE` bodies, and cross-domain requests allowed by default.

It cannot restore IE11 support, nor the extension API change (the new swap method): custom or community extensions must be updated to the htmx 2 API.

## Checked

2026-11-07. Confirmed on migration-guide-htmx-1.md (module files, extensions, `hx-ws`/`hx-sse`, the three config reverts, `hx-on` conversion, `makeFragment`, `selectAndSwap` to `swap`, IE) and extensions/htmx-1-compat.md (install, what it restores, what it does not cover).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
