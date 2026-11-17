---
id: computing-software.software-engineering.groovy.operator-equality-identity
name: operator-equality-identity
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, operator-equality-identity]
level: practitioner
status: docs-checked
description: "== is equals/compareTo, .is() is identity, as for coercion, in for isCase, and null-safe equality semantics."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-differences-java.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality, identity and coercion
- `a == b` is null-safe `equals` (or `compareTo` when Comparable); `a.is(b)` tests identity.
- `a != b` negates `==`; `===` and `!==` are identity operators, same as `is()` and its negation (since Groovy 3.0.0).
- `x as Type` calls `asType`; custom conversion rules are implemented by `asType`.
- `x instanceof T`, `x in list` uses `isCase`.

## Gotchas
- `==` compares the text of a `GString` and a `String`, but their hashCodes differ, so a `GString` Map key is not found by a `String` lookup.

## Self-check
`assert !(new Object().is(new Object()))`.

## Checked

2026-11-02. Confirmed against the Operators chapter (identity operators, membership, asType) and Differences from Java (== behaviour), Syntax (GString hashCodes). Removed: the [1] == [1L] claim, the 1 == 1L self-check and the Set/int coercion examples.

Method: documentation only; no commands were run.
