---
id: computing-software.software-engineering.groovy.closure-to-sam
name: closure-to-sam
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, closure-to-sam]
level: practitioner
status: docs-checked
description: "Passing closures where Java expects a functional interface or abstract class (SAM coercion) and as Comparator/Runnable."
sources:
  - https://groovy-lang.org/semantics.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closure coercion to interfaces and SAM types
- A closure converts to a SAM type with `as`; since Groovy 2.2.0 the `as Type` is optional, in assignments and in calls to methods that take a SAM type.
- Explicit: `{ ... } as Runnable`. A closure can also be coerced to any interface or class with `as`, and every method is then implemented by the closure. For several methods coerce a Map: keys are method names, values the implementations (`[run: { }, close: { }] as MyIface`).
- Lambda expressions such as `(Integer x, Integer y) -> x + y` are supported as expressions.

## Gotchas
- A Map coerced to an interface only needs the methods that are called; calling a missing one throws `MissingMethodException` (arguments do not match) or `UnsupportedOperationException` (arguments match an overload).

## Self-check
`Runnable r = { println 'ok' }; r.run()`.

## Checked

2026-11-02. Confirmed against the Semantics chapter (Assigning a closure to a SAM type, closure to arbitrary type, Map to type coercion, expressions table). Removed: the Java 8 stream example, the @CompileStatic gotcha and the unconditional UnsupportedOperationException claim.

Method: documentation only; no commands were run.
