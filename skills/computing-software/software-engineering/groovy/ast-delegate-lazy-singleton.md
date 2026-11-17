---
id: computing-software.software-engineering.groovy.ast-delegate-lazy-singleton
name: ast-delegate-lazy-singleton
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, ast-delegate-lazy-singleton]
level: practitioner
status: docs-checked
description: "@Delegate for composition, @Lazy fields, @Singleton instances and @Memoized methods."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://docs.groovy-lang.org/latest/html/gapi/
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegate, Lazy, Singleton and Memoized
- `@Delegate private Foo foo` makes the class delegate calls of Foo's methods to the property (compose rather than inherit).
- `@Lazy List data = expensive()` initialises on first access; a `volatile` field uses double-checked locking, and `@Lazy(soft = true)` holds the value in a `SoftReference` (a simple cache).
- `@Singleton class Reg {}` gives `Reg.instance`, created eagerly by default; `lazy = true` defers creation (double-checked locking); `property` renames the instance property.
- `@Memoized` caches method results by arguments; `maxCacheSize` limits the cache and `protectedCacheSize` protects results from garbage collection.
- `@Synchronized`, `@WithReadLock`, `@WithWriteLock` for simple locking.

## Gotchas
- `@Singleton` is strict by default; set `strict = false` to define your own constructor.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (`@Delegate`, `@Lazy`, `@Singleton`, `@Memoized`, `@Synchronized`, `@WithReadLock`/`@WithWriteLock`). Removed: the "cannot have a public constructor" and delegate-recompile claims; corrected the `volatile` and `soft` description of `@Lazy`.

Method: documentation only; no commands were run.

## Self-check
`@Singleton class S {}; assert S.instance.is(S.instance)`.
