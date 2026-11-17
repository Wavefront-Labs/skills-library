---
id: computing-software.software-engineering.groovy.groovy-vs-java
name: groovy-vs-java
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovy-vs-java, groovy-java-interop]
level: intro
status: docs-checked
description: "The Groovy differences that trip Java developers: default imports, == semantics, visibility, semicolons, arrays, inner classes, and primitive handling."
sources:
  - https://groovy-lang.org/differences.html
  - https://groovy-lang.org/integrating.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-differences-java.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-numbers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differences from Java
- Default imports: `java.io.*`, `java.lang.*`, `java.math.BigDecimal`, `java.math.BigInteger`, `java.net.*`, `java.time.*`, `java.util.*`, `groovy.lang.*`, `groovy.util.*`.
- For non-primitives `==` maps to `.equals()`; use `a.is(b)` for identity.
- `{ ... }` is reserved for closures, so Java's array initializer shorthand does not work; use list notation (`[1, 2] as int[]`). Groovy 3+ also accepts Java's long array initializer syntax.
- `/` gives a `double` if either operand is a `float` or `double`, otherwise a `BigDecimal`; use `intdiv()` for integer division.
- A field without a modifier becomes a property (private field plus getter and setter), not package-private; `@PackageScope` gives package-private.
- Methods are chosen at runtime from argument types (multi-methods).
- Comprehensive list: the Differences with Java chapter.

## Gotchas
- Anonymous inner classes and nested classes follow Java closely but rely on `Closure` implementation details.
- Lambda expressions and the `::` method reference operator are supported.

## Checked

2026-11-02. Confirmed against the Differences with Java chapter (default imports, equality, array initializers, package-private properties, multi-methods, inner classes, lambdas) and the numbers chapter (division operator). Removed: `private`/checked exception, optional-syntax, `**`, `?.`/`?:`, and for-loop claims. Fixed: the default imports list omitted `java.time.*`; integer division was stated without the double case.

Method: documentation only; no commands were run.

## Self-check
Translate a small Java class to Groovy without dots-semicolons-and confirm same output.
