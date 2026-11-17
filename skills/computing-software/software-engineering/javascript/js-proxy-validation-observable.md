---
id: computing-software.software-engineering.javascript.js-proxy-validation-observable
name: js-proxy-validation-observable
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, proxy-traps, js-proxy-reflect]
level: advanced
status: docs-checked
description: "Implement validation, defaults and change tracking with Proxy get and set traps and forward with Reflect."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy traps for validation and observation

- `new Proxy(target, handler)`: the handler's traps (`get(target, prop, receiver)`, `set(obj, prop, value)`, `has`, `deleteProperty`, ...) intercept the matching internal methods.
- Validation: a `set` trap throws `TypeError` or `RangeError` for a bad value, otherwise stores it and returns `true` to indicate success (MDN's `age` validator).
- Defaults: a `get` trap can return a fallback such as `prop in obj ? obj[prop] : 37`.
- Invariants about non-extensible objects and non-configurable properties are checked against the target; a trap that violates them throws `TypeError`.
- A proxy has its own identity and no access to the target's private elements or internal slots: `new Proxy(new Map(), {}).size` throws. Use a "this-recovering" proxy that calls methods with the original target as `this`.
- `Proxy.revocable()` creates a revocable proxy.
- Array methods read and write through internal methods, so `push()` invokes the `get()` and `set()` traps; log in the traps to observe changes.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Proxy: handler and trap signatures, validation and default-value examples, invariants and TypeError, private field and Map internal slot errors with the this-recovering fix, Proxy.revocable, push invoking get and set traps. Removed as not stated there: set-trap falsy return throwing in strict mode, the `revoke()` call form, the slow-traps remark, and the "two set traps for push" count.

Method: documentation only; no commands were run.
