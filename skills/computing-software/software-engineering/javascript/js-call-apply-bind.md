---
id: computing-software.software-engineering.javascript.js-call-apply-bind
name: js-call-apply-bind
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, function-bind, js-closures-this]
level: practitioner
status: docs-checked
description: "Fix a function's this and leading arguments with bind(); how bound functions behave with new, rebinding, extends and static properties."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bind and the this value

- `fn.bind(thisArg, arg1, ...)` returns a new function that calls `fn` with `this` fixed and the given arguments prepended to the call-time arguments. It behaves like `(...rest) => fn.call(thisArg, arg1, ..., ...rest)` when called, but not when constructed.
- Lost `this`: `const retrieveX = module.getX; retrieveX()` has `this` set to the global object in non-strict code and `undefined` in strict code. Fix with `retrieveX.bind(module)`.
- In `setTimeout`, `this` defaults to `globalThis`; use `this.declare.bind(this)` or an arrow function (`() => this.declare()`) to keep the instance.
- If the target is not strict, `null`/`undefined` as `thisArg` become the global object and primitives are boxed.
- A bound function can be bound again, but the new `thisArg` is ignored because the target already has a bound `this`; bound arguments accumulate in order.
- Bound functions work with `new`: `thisArg` is ignored, prepended arguments are kept, `new.target` and `instanceof` behave as if the constructor were unbound. Called without `new`, the bound `this` applies.
- A bound function has no `prototype` property, so it cannot be a base class for `extends`. Binding a class loses its own static properties (inherited statics are still reachable through the prototype chain).
- The bound function's `length` is the target's `length` minus the bound arguments (minimum 0) and its `name` is the target's name with a `"bound "` prefix.
- Partial application: `addArguments.bind(null, 37)` gives a function with the first argument preset.

Self-check: `module.getX.bind(module)()` returns `module.x` while the unbound extract returns `undefined` or the global's value.

## Checked

Confirmed on the MDN Function.prototype.bind page: all points above. Removed: `apply` syntax, arrow functions ignoring `call/apply/bind`, `removeEventListener` identity advice and the "prefer spread over `apply`" advice, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
