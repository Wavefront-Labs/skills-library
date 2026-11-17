---
id: computing-software.software-engineering.javascript.js-reflect-api
name: js-reflect-api
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, reflect-ownkeys, js-proxy-reflect]
level: advanced
status: docs-checked
description: "Use Reflect.ownKeys, set, apply, construct and has as the function forms of object operations and Proxy defaults."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reflect API methods

- `Reflect` is a non-constructor namespace of static methods with the same names as the Proxy handler methods; its main use is default forwarding inside Proxy traps.
- `Reflect.ownKeys(o)` returns the object's own (not inherited) property keys.
- `Reflect.defineProperty` is like `Object.defineProperty` but returns a boolean saying whether it succeeded; `Reflect.set` and `Reflect.setPrototypeOf` likewise return a boolean.
- `Reflect.apply(fn, thisArg, args)` calls a function with an argument list.
- `Reflect.construct(Target, args, NewTarget)` is the only way to construct a function with a specific `new.target`.
- `Reflect.get` can run a getter with a custom `this`.
- `Reflect.has(o, k)` works like the `in` operator; `Reflect.deleteProperty` is the `delete` operator as a function.
- Inside a trap, a Reflect call that is itself intercepted by the same trap can recurse infinitely.

Self-check: `Reflect.ownKeys({ name: "Maurice", color: "white" })` returns `["name", "color"]`.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Reflect and Global_Objects/Proxy: method descriptions, boolean returns, construct and new.target, get with custom this, forwarding use and recursion warning. Removed as not stated there: ownKeys including symbols and non-enumerable keys, defineProperty not throwing, "safe form" of apply, getPrototypeOf throwing for non-objects.

Method: documentation only; no commands were run.
