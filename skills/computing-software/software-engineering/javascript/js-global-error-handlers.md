---
id: computing-software.software-engineering.javascript.js-global-error-handlers
name: js-global-error-handlers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, window-onerror, js-error-handling]
level: practitioner
status: docs-checked
description: "Capture uncaught errors with the window error event, unhandledrejection and Node uncaughtException; know finally and catch rules."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch", "https://developer.mozilla.org/en-US/docs/Web/API/Window/error_event", "https://developer.mozilla.org/en-US/docs/Web/API/Window/unhandledrejection_event", "https://nodejs.org/api/process.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global error handlers and finally semantics

- Browser: `window.addEventListener("error", (event) => ...)`. The `error` event fires on `Window` when a resource failed to load or could not be used, for example a script execution error. It is generated only for script errors thrown synchronously (initial load, event handlers). A rejected promise with no handler fires `unhandledrejection` instead.
- `window.onerror` is special: it receives five arguments (`message, source, lineno, colno, error`), unlike `addEventListener`, which receives one `ErrorEvent`. To cancel the default behaviour (console output) an `onerror` handler must return `true`, not `false`; the current script still stops.
- `unhandledrejection` is sent to the global scope (window or a Worker) when a promise with no rejection handler is rejected. It is a `PromiseRejectionEvent` and is cancelable: `event.preventDefault()` suppresses the default console message. Rejections originating from a cross-origin script do not fire it.
- Node: `process.on("uncaughtException", (err, origin) => ...)` is a last resort. Without a handler Node prints the stack to stderr and exits with code 1; with one, the process continues (exit code 0 unless `process.exitCode` is changed). Node says it is not safe to resume normal operation afterwards: use it for synchronous cleanup before shutting down, and restart the app with an external monitor process. `uncaughtExceptionMonitor` observes without overriding the crash. Exceptions thrown inside the handler exit the process non-zero.
- `finally` always runs before control leaves the construct. A `return`, `throw`, `break` or `continue` in `try`/`catch` is deferred until `finally` ends, but a control-flow statement as the last statement in `finally` overrides it, so avoid them there.
- Catch binding is optional: `catch { ... }`. The binding can be a destructuring pattern, is writable, and may hold a non-`Error` value, so normalise with `instanceof Error`.
- Rethrow errors you do not expect: `else { throw e; }`.

Self-check: throw in an event handler and confirm your `error` listener receives it; reject a promise without a handler and confirm `unhandledrejection` fires.

## Checked

2026-11-08. Confirmed on MDN try...catch, Window error event, Window unhandledrejection event, and the Node.js process page (`uncaughtException`, `uncaughtExceptionMonitor`). Removed the "Script error." cross-origin CORS note, the ESLint rule `no-unsafe-finally`, and the `navigator.sendBeacon` advice, none of which those pages state.

Method: docs-only read of cited pages, 2026-11-08
