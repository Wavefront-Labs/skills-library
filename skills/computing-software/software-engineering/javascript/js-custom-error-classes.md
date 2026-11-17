---
id: computing-software.software-engineering.javascript.js-custom-error-classes
name: js-custom-error-classes
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, custom-error-class, js-error-handling]
level: practitioner
status: docs-checked
description: "Define Error subclasses that set name, pass options so cause works, and are checked with instanceof; note non-standard stack APIs."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom error classes

- Derive from `Error` to throw `new MyError()` and test with `instanceof MyError`.
- Pass the options argument through to `super(message, options)`: the `Error` constructor reads `options.cause` and defines `cause` on the instance. Without passing `options`, `cause` is not installed.
- Wrap and rethrow with `throw new Error("Failed in some way", { cause: err })` so higher-level handlers keep the original error and stack. In a library, prefer `cause` to discriminate errors rather than making callers parse messages.
- Set `this.name` in the constructor (MDN's example uses `this.name = "CustomError"`); `Error.prototype.name` is `"Error"` by default.
- `Error.captureStackTrace`, `Error.stackTraceLimit` and `Error.prototype.stack` are non-standard; MDN guards the call with `if (Error.captureStackTrace)`.
- `Error` is serializable: it can be cloned with `structuredClone()` or copied between workers with `postMessage()`.
- Subclassing built-ins cannot be reliably transpiled to pre-ES6 code; without extra configuration you may need `Object.setPrototypeOf(this, CustomError.prototype)` at the end of the constructor or the instance is not a `CustomError`.
- Some browsers include the custom constructor in the stack trace when using ES2015 classes.

Self-check: `new HttpError("x", 404) instanceof Error` is true, and `new MyError("test", { cause: new Error("cause") }).cause` is the inner error.

## Checked

Confirmed on the MDN Error page: custom error pattern, cause via options, name default, non-standard stack members, structuredClone and postMessage, transpilation warning. Removed: `JSON.stringify` giving `{}`, `toJSON` advice, cross-realm `instanceof` failure and `no-throw-literal`, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
