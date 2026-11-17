---
id: computing-software.software-engineering.javascript.js-weakmap-weakref
name: js-weakmap-weakref
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, weakref-finalization, js-collections]
level: advanced
status: docs-checked
description: "Use WeakRef.deref with correct expectations about garbage collection, and know which values can key weak collections."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakRef", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WeakRef and weak collections

- A `WeakRef` holds a weak reference to an object (or a non-registered symbol) without preventing garbage collection. `deref()` returns the target, or `undefined` if it has been reclaimed.
- `WeakMap`, `WeakSet`, `WeakRef` and `FinalizationRegistry` accept objects and non-registered symbols, but not symbols from `Symbol.for()`, which are not garbage collectable.
- MDN says correct use of `WeakRef` takes careful thought and is best avoided where possible. When, how and whether garbage collection occurs is up to the engine; do not depend on timely or predictable cleanup, which may happen much later or not at all.
- A target obtained via `new WeakRef(obj)` or `deref()` is not reclaimed until the end of the current JavaScript job. `deref()` may never return `undefined`.
- The target of a `WeakRef` cannot be changed, and `WeakRef`s with the same target are consistent with each other.
- If the target is also registered in a `FinalizationRegistry`, `deref()` inside the cleanup callback returns `undefined`.

Example: MDN's `Counter` holds a `WeakRef` to a DOM element and stops its timer when `deref()` returns `undefined`.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/WeakRef (semantics, avoid-where-possible warning, notes on jobs and consistency, deref) and Global_Objects/Symbol (which symbols can be weak-collection keys). Removed as not stated in the pages read: WeakMap/WeakSet not iterable and lacking size, DOM-keyed cache use cases, the `wm.has`/`wm.size` self-check, the testing remark.

Method: documentation only; no commands were run.
