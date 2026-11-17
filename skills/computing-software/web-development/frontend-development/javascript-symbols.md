---
id: computing-software.web-development.frontend-development.javascript-symbols
name: javascript-symbols
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-symbols, well-known-symbols, symbol-iterator, symbol-toprimitive, symbol-dispose, javascript]
level: practitioner
status: docs-checked
description: "Using Symbols for collision-free keys and the well-known symbols (iterator, asyncIterator, toPrimitive, toStringTag, hasInstance, dispose) to hook language behaviour."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/using
  - https://tc39.es/ecma262/#sec-well-known-symbols
  - https://github.com/tc39/proposal-explicit-resource-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symbols and well-known symbols

## 1. Basics
```js
const meta = Symbol("meta");            // unique every call; description is for debugging
obj[meta] = { cachedAt: Date.now() };
Symbol.for("app.meta") === Symbol.for("app.meta");   // true: global registry, shared across realms
```
Symbol keys are skipped by `Object.keys`, `for...in`, `JSON.stringify`; found via `Object.getOwnPropertySymbols` or `Reflect.ownKeys`. Useful for metadata that must not collide with user keys or serialize. Not private: anyone can enumerate them (use `#private` for privacy).

`"x" + sym` throws TypeError; use `String(sym)` or `sym.description`.

## 2. Well-known symbols
```js
class Range {
  constructor(a, b) { this.a = a; this.b = b; }
  *[Symbol.iterator]() { for (let i = this.a; i <= this.b; i++) yield i; }
  [Symbol.toPrimitive](hint) { return hint === "number" ? this.b - this.a : `${this.a}..${this.b}`; }
  get [Symbol.toStringTag]() { return "Range"; }
}
[...new Range(1, 3)];              // [1, 2, 3]
`${new Range(1, 3)}`;              // "1..3"
+new Range(1, 3);                  // 2
Object.prototype.toString.call(new Range(1, 3)); // "[object Range]"
```
| Symbol | Hooks |
|---|---|
| `Symbol.iterator` / `asyncIterator` | `for...of`, spread / `for await` |
| `Symbol.toPrimitive` | coercion; hint `"number"`, `"string"`, `"default"` |
| `Symbol.hasInstance` | `instanceof` |
| `Symbol.species` | constructor used by `map/filter` on subclasses (avoid relying on it) |
| `Symbol.dispose` / `asyncDispose` | `using` / `await using` cleanup (explicit resource management) |

## 3. Explicit resource management
```js
{
  using lock = acquireLock();   // lock[Symbol.dispose]() runs at block exit, even on throw
}
```
Per mdn/browser-compat-data `Symbol.dispose` is in Chrome 125 and Firefox 141, with Safari in preview. Check support before relying on `using` in browsers; the proposal repository lists the spec status.

## Gotchas
- `Symbol()` is not a constructor: `new Symbol()` throws.

## Verify
- [ ] Custom iterables work with spread, `Array.from` and destructuring.

## Checked

2026-10-26. MDN `Symbol` (unique per call, `Symbol.for` registry, `new Symbol()` throws TypeError, well-known symbols are constant across realms), `for...in` and `JSON.stringify`/`Object.keys` string-key behaviour, `Symbol.toPrimitive` hints, `using` declaration and browser-compat-data for `Symbol.dispose`. Removed the unconfirmed structuredClone key claim and the TypeScript 5.2 lib note.

Method: documentation only; no commands were run.
