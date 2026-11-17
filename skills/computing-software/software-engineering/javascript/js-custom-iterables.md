---
id: computing-software.software-engineering.javascript.js-custom-iterables
name: js-custom-iterables
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, custom-iterable, js-iteration]
level: practitioner
status: docs-checked
description: "Build proper iterators: next() protocol, extending Iterator or using Iterator.from, helper methods, single-use iteration and return()."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing custom iterators and iterables

- An object conforms to the iterator protocol when it has a `next()` method returning an iterator result object. An object is iterable when it has a `[Symbol.iterator]()` method. Generator functions return Generator objects, which are built-in iterators.
- There are two kinds of "iterator": protocol-conforming objects (only `next()` required) and objects inheriting from `Iterator`, which get the helper methods. They do not imply each other: extending `Iterator` does not add `next()`. A proper iterator does both, and MDN says most code expects iterables to return proper iterators.
- To make a proper iterator, define `class MyIterator extends Iterator { next() { ... } }` or wrap a plain object with `Iterator.from({ next() { ... } })`. `Iterator()` cannot be constructed by itself.
- `Iterator.prototype[Symbol.iterator]()` returns the iterator itself, so an iterator is also iterable and works in `for...of`.
- Helper methods analogous to array methods: `every`, `filter`, `find`, `flatMap`, `forEach`, `includes`, `join`, `map`, `reduce`, `some`, plus `drop`, `take` and `toArray`. `filter`, `flatMap`, `map`, `drop` and `take` return a chainable iterator helper object. They are needed for infinite iterators, where converting to an array is impossible: `fibonacci().find((n) => n >= 100)` only iterates as far as necessary.
- An iterator helper shares the data source of the underlying iterator and there is no way to fork an iterator to iterate it multiple times: consumption through one is visible through the other. Its `return()` calls the underlying iterator's `return()`.

Self-check: `fibonacci().take(3).toArray()` on an infinite generator terminates, and `for (const v of [1, 2, 3].values())` works because built-in iterators are iterable.

## Checked

Confirmed on the MDN Iterator page: protocol definition, proper iterators, `Iterator.from`, self-returning `[Symbol.iterator]()`, helper method list, infinite-iterator rationale, shared-source and no-fork behaviour, helper `return()`. Removed: `return()` running on `break` or `throw`, `yield*` return values, `gen.next(v)`/`gen.throw`, the list of consumers (`Promise.all`, `Map`, `Set`) and the `*[Symbol.iterator]() { yield* ... }` shortcut, none of which this page states.

Method: docs-only read of cited pages, 2026-11-08
