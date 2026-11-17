---
id: computing-software.software-engineering.javascript.js-iterator-helpers
name: js-iterator-helpers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, iterator-helpers, js-iteration]
level: advanced
status: docs-checked
description: "Use Iterator helper methods (map, filter, take, drop, reduce, toArray) and Iterator.from on built-in and custom iterators."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterator helpers

- Helper methods live on `Iterator.prototype`: `map`, `filter`, `flatMap`, `drop`, `take` return a new iterator helper object (chainable); `reduce`, `toArray`, `some`, `every`, `find`, `forEach`, `includes`, `join` consume the iterator.
- They avoid intermediate arrays and iterate only as far as needed, so they work on infinite iterators: `fibonacci().find((n) => n >= 100)` stops at the first match. Use `take(n)` before `toArray()` on an infinite sequence.
- `Iterator.from(x)` creates an `Iterator` from an iterator or iterable; a "proper" iterator both has `next()` and inherits from `Iterator`, which is what provides the helpers.
- A helper shares its data source with the underlying iterator and cannot be forked: iterating one advances the other. A helper's `return()` calls the underlying iterator's `return()`.
- Helpers are newer than the iteration protocol: check browser and runtime compatibility, or fall back to generator functions or `[...it]`.

Self-check: `Iterator.from` a counter generator, `.take(3).toArray()` returns three values and does not hang.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Iterator: helper method list and descriptions, chainable helper objects, infinite-iterator `find` example, Iterator.from, proper iterators, shared data source, return() behaviour. Removed as not stated there: the "ES2025" label, the Node 22 support claim, and the arbitrary filter/take example.

Method: documentation only; no commands were run.
