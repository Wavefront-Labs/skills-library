---
id: computing-software.software-engineering.groovy.closure-basics
name: closure-basics
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, closure-basics, groovy-closures]
level: intro
status: docs-checked
description: "Define and call closures: implicit it, explicit parameters, defaults, call(), return values and passing as the last argument."
sources:
  - https://groovy-lang.org/closures.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-closures.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closure syntax, parameters and calling
```groovy
def sq = { int x -> x * x }
def hi = { it.toUpperCase() }            // implicit single param 'it'
def none = { -> 42 }                      // zero params
assert sq(4) == 16 && sq.call(4) == 16 && hi('a') == 'A'
list.each { println it }                  // closure as last argument, outside parens
```
- `{ a, b = 2 -> ... }`: each parameter has an optional type, a name and an optional default value.
- A closure with no explicit `->` parameter list always has an implicit `it` parameter.
- Closure return is its last expression.

## Gotchas
- `{ -> }` has zero params; `{ }` accepts one optional `it`.

## Self-check
Run the snippet; `assert none() == 42`.

## Checked

2026-11-02. Confirmed against the Closures chapter (parameters, implicit parameter, return value). Removed: the maximumNumberOfParameters/parameterTypes claim and the return-inside-closure gotcha.

Method: documentation only; no commands were run.
