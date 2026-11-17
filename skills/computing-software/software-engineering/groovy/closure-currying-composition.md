---
id: computing-software.software-engineering.groovy.closure-currying-composition
name: closure-currying-composition
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, closure-currying-composition]
level: advanced
status: docs-checked
description: "curry, rcurry, ncurry, closure composition with << and >>, memoize and trampoline for Groovy closures."
sources:
  - https://groovy-lang.org/closures.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-closures.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Currying, composition and memoization
```groovy
def add = { a, b -> a + b }
def inc = add.curry(1)                   // fixes first arg
assert inc(5) == 6 && add.rcurry(1)(5) == 6
def twice = { it * 2 }
assert (inc >> twice)(3) == 8             // inc then twice
assert (inc << twice)(3) == 7             // twice then inc
def slow = { n -> n * n }.memoize()       // also memoizeAtMost(n)
def fact; fact = { n, acc = 1G -> n <= 1 ? acc : fact.trampoline(n - 1, acc * n) }.trampoline()
```
- `trampoline()` avoids stack overflow for tail recursion.

## Gotchas
- `memoize` variants use an LRU cache (`memoizeAtMost`, `memoizeAtLeast`, `memoizeBetween`); do not memoize impure closures.

## Self-check
Run the asserts.

## Checked

2026-11-02. Confirmed against the Closures chapter (left, right and index-based currying, memoize variants, trampoline) and the ClosuresSpecTest composition example (`<<`, `>>`). Removed: the default-argument curry gotcha and the equals-based cache claim.

Method: documentation only; no commands were run.
