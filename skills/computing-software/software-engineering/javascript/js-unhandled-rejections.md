---
id: computing-software.software-engineering.javascript.js-unhandled-rejections
name: js-unhandled-rejections
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, unhandled-rejection, js-promises]
level: practitioner
status: docs-checked
description: "Find and prevent unhandled promise rejections in browsers and Node; use the unhandledRejection and rejectionHandled events."
sources: ["https://nodejs.org/api/process.html", "https://developer.mozilla.org/en-US/docs/Web/API/Window/unhandledrejection_event"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unhandled rejections and async error flow

- Browser: `window.addEventListener("unhandledrejection", (event) => { report(event.reason); event.preventDefault(); })`. The event is cancelable; `preventDefault()` stops the default console error. Rejections from cross-origin scripts do not fire it.
- Node: `process.on("unhandledRejection", (reason, promise) => ...)` fires when a promise is rejected and no handler is attached within a turn of the event loop. If the event is emitted but not handled, it is raised as an uncaught exception, which exits with code 1 by default. The `--unhandled-rejections` flag changes this; per the page, the default mode is `throw`.
- A rejection can be handled later than the event loop turn in which `unhandledRejection` fired; Node then emits `rejectionHandled`. Track both events (for example in a `Map`) and log periodically for long-running apps or at exit for scripts.
- A promise created already rejected (for example `this.loaded = Promise.reject(...)` in a constructor) triggers the event unless a handler, even `.catch(() => {})`, is attached within a turn.
- Typical cause named in the docs: a `.then` chain with no `.catch`, where an error in the callback (such as a typo) rejects the promise unhandled.
- `uncaughtException` receives an `origin` argument; it is `"unhandledRejection"` when the exception came from an unhandled rejection under the `strict` or `throw` modes.

Self-check: run `Promise.reject(new Error("x"))` in Node without a handler and confirm the process exits with a non-zero code.

## Checked

2026-11-08. Confirmed on the Node.js process page (`unhandledRejection`, `rejectionHandled`, `uncaughtException` origin, default mode `throw`, exit code 1) and MDN unhandledrejection event. Removed the "since Node 15" version claim, the list of other flag modes, the causes list (`forEach` with async callbacks, `return await`), and the ESLint rules, which the cited pages do not state.

Method: docs-only read of cited pages, 2026-11-08
