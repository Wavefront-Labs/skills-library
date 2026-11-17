---
id: computing-software.software-engineering.typescript.this-binding-and-closures
name: this-binding-and-closures
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, this-binding, closures, arrow-functions, bind, lexical-scope, stale-closure, memory-leaks, class-fields]
level: practitioner
status: docs-checked
description: "Predict JavaScript this binding (call site, arrow, bind, class methods as callbacks) and use closures without stale-value bugs or memory leaks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures
  - https://www.typescriptlang.org/docs/handbook/2/classes.html#this-at-runtime-in-classes
  - https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
  - https://typescript-eslint.io/rules/unbound-method/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# this binding and closures

**Goal:** stop "cannot read properties of undefined" from detached methods, and stale
values from closures.

## How `this` is decided (non-arrow functions)
| Call | this |
|---|---|
| `obj.method()` | `obj` |
| `const f = obj.method; f()` | `undefined` (strict mode / modules / classes) |
| `f.call(x)`, `f.apply(x)`, `f.bind(x)()` | `x` |
| `new F()` | the new object |
| Arrow function | `this` of the enclosing scope, fixed forever |

## The detached method bug
```ts
class Counter {
  count = 0;
  inc() { this.count++; }
}
button.addEventListener("click", counter.inc);   // this is the button / undefined
```
Fixes:
```ts
button.addEventListener("click", () => counter.inc());   // wrap at call site
class Counter { inc = () => { this.count++; }; }          // arrow class field: bound per instance
this.inc = this.inc.bind(this);                            // in constructor
```
Arrow class fields allocate one function per instance and are not on the prototype
(cannot be overridden via `super.inc()`); fine for UI handlers, wasteful for many objects.
TypeScript can enforce: declare `this: Counter` as a pseudo-parameter
(`inc(this: Counter) {}`) and enable `@typescript-eslint/unbound-method`.

## Closures
A closure captures VARIABLES (bindings), not values.
```js
for (var i = 0; i < 3; i++) setTimeout(() => console.log(i));   // 3 3 3
for (let i = 0; i < 3; i++) setTimeout(() => console.log(i));   // 0 1 2 (new binding per iteration)
```
- Memory: a closure keeps its whole captured scope alive. Long-lived listeners or
  caches that capture large objects leak them; remove listeners (`AbortController`
  signal option on `addEventListener`) and avoid capturing more than needed.

## Verify
- [ ] `@typescript-eslint/unbound-method` enabled, no violations.
- [ ] Heap snapshot after repeated mount/unmount shows no growing detached listeners.

## Checked
Checked 2026-10-25 against the MDN content repository, the TypeScript-Website Classes handbook and the typescript-eslint rule docs. Confirmed: a detached method called without a receiver has `this` undefined in strict mode; `call`, `apply`, `bind` and arrow-function `this`; closures capture variables (let versus var in loops); the `signal` option of addEventListener; the unbound-method rule; `this` parameters. Removed the unconfirmed React stale-closure remark.
Method: documentation only; no commands were run.
