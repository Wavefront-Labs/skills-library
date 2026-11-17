---
id: computing-software.web-development.vite.preload-error-handling
name: preload-error-handling
category: computing-software
field: web-development
product: vite
tags: [vite-preload-error, stale-chunks, dynamic-import-failure]
level: practitioner
status: docs-checked
description: "Handle failed dynamic imports after a deploy with the vite:preloadError event, preventDefault, and no-cache on the HTML file."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite emits `vite:preloadError` when a dynamic import fails to load. `event.payload` holds the original import error; calling `event.preventDefault()` stops the error being thrown.

```js
window.addEventListener('vite:preloadError', (event) => {
  window.location.reload() // for example, refresh the page
})
```

Why it matters: after a new deployment the host may delete the previous assets. A user who loaded the site earlier then tries to import an old chunk that no longer exists. Set `Cache-Control: no-cache` on the HTML file, or old assets stay referenced.

Browsers with retriable module loading let an app retry the original dynamic import after a transient network or HTTP error. Older browsers cache the failure in the module map and need a page reload.

## Checked

Date: 2026-11-07

Read build.md in full (Load Error Handling). Confirmed vite:preloadError, event.payload, preventDefault, the reload example, retriable module loading and Cache-Control no-cache on HTML. Nothing removed.

Method: documentation only; no commands were run.
