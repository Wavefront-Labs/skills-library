---
id: computing-software.software-engineering.groovy.spread-operators
name: spread-operators
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, spread-operators]
level: practitioner
status: docs-checked
description: "Spread-dot, spread list/map, and the method pointer (.&) and method reference (::) operators."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spread and method pointer operators
- `list*.name` collects `name` of each element (null-safe on null elements).
- `f(*args)` spreads a list into arguments; `[*a, *b]` merges lists; `[*:m1, *:m2]` merges maps.
- Method pointer: `def p = obj.&method` stores a reference to a method in a variable to call later.
- Method reference (Java style) `String::toUpperCase` works in Groovy 3+ (parrot parser).
- Direct field access `obj.@field` bypasses the getter.

## Gotchas
- `*.` is null-safe for null elements: it returns null for them instead of throwing.

## Self-check
`assert [[n:1],[n:2]]*.n == [1,2] && [*[1,2],3] == [1,2,3]`.

## Checked

2026-11-02. Confirmed against the Operators chapter (spread-dot, spread arguments, list and map spread, method pointer, method reference, direct field access). Removed: the metaClass gotcha, the null-collection claim and the valueOf example.

Method: documentation only; no commands were run.
