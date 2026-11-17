---
id: computing-software.web-development.frontend-development.javascript-this-binding
name: javascript-this-binding
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-classes, this-binding, arrow-functions, bind, javascript]
level: practitioner
status: docs-checked
description: "Predicting `this` in JavaScript: the four binding rules, arrow functions, losing this in callbacks and event handlers, and fixing it with bind, arrows or class fields."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `this` binding rules

`this` is decided by **how a function is called**, not where it is defined (except arrows).

## 1. Rules in precedence order
1. `new Fn()` - `this` is the new object.
2. `fn.call(obj)` / `fn.apply(obj)` / `fn.bind(obj)` - explicit. A bound function ignores later `call`/`bind`.
3. `obj.fn()` - `this` is `obj` (the thing left of the dot at call time).
4. Plain `fn()` - `undefined` in strict mode and modules/classes; `globalThis` in sloppy scripts.

Arrow functions have no own `this`; they capture it from the enclosing scope at creation and ignore call/bind/new.

## 2. The classic loss
```js
class Clock {
  ticks = 0;
  tick() { this.ticks++; }
  start() { setInterval(this.tick, 1000); }   // TypeError: this is undefined when the timer calls tick
}
```
Fixes:
```js
start() { setInterval(() => this.tick(), 1000); }   // arrow wrapper
constructor() { this.tick = this.tick.bind(this); }  // bind once
tick = () => { this.ticks++; };                      // arrow class field (per-instance copy)
```
Same with `button.addEventListener("click", this.onClick)` and with destructuring `const { tick } = clock`.

## 3. DOM handlers
In a non-arrow listener, `this === event.currentTarget`. In an arrow, it is the outer `this`. Prefer `event.currentTarget` explicitly - clearer and arrow-safe.

## 4. Pitfalls
- Arrows as object methods: `const o = { n: 1, get: () => this.n }` - `this` is the module's `undefined`.
- `removeEventListener(this.onClick.bind(this))` never removes - each bind returns a new function. Store the bound reference or use an `AbortController` signal.
- Callbacks with a `thisArg` parameter (`arr.map(fn, thisArg)`) are ignored for arrows.
- Methods passed to libraries (`promise.then(obj.method)`) lose `this` too.

## Verify
Run in a module: `const f = obj.method; f()` throws rather than silently using `window` - write a test that calls handlers detached.

## Checked

2026-10-26. MDN `this` (value depends on how the function is invoked; strict mode; listener `this` equals `event.currentTarget`), arrow functions (no own `this`, `thisArg` ignored for call/apply/bind, arrow class fields close over the instance) and `Function.prototype.bind`. Reworded the error message in the example, which varies by engine.

Method: documentation only; no commands were run.
