---
id: computing-software.software-engineering.groovy.operator-methods
name: operator-methods
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, operator-methods, groovy-op-overload]
level: advanced
status: docs-checked
description: "Which method name each Groovy operator calls (plus, minus, multiply, getAt, leftShift, compareTo, equals, asType)."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator to method mapping
- `+ plus`, `- minus`, `* multiply`, `/ div`, `% mod`, `** power`, `<< leftShift`, `>> rightShift`, `[] getAt`/`putAt`, `a in b` -> `b.isCase(a)`, `<=>` `compareTo`, `==` `equals` (or `compareTo` if Comparable), `as` `asType`, unary `-a` `negative`, `++` `next`, `--` `previous`.
- Implement the method on your class and the operator works:
```groovy
class V { int x; V plus(V o) { new V(x: x + o.x) } }
assert (new V(x:1) + new V(x:2)).x == 3
```
- Complete table: the Operators chapter, section Operator Overloading.

## Gotchas
- `==` calls `compareTo` for Comparable types, so `equals` may not run.
- The operator method must be public with the right name and number of arguments.

## Self-check
Run the snippet.

## Checked

2026-11-02. Confirmed against the Operators chapter (Operator Overloading table, requirements for the method). Removed: the claim about << on strings and writers.

Method: documentation only; no commands were run.
