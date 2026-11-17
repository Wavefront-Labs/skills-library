---
id: computing-software.software-engineering.groovy.typechecked
name: typechecked
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, typechecked, groovy-static]
level: practitioner
status: docs-checked
description: "Compile-time type checking in Groovy with @TypeChecked, flow typing, and what still runs dynamically."
sources:
  - https://groovy-lang.org/semantics.html
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @TypeChecked
- `@TypeChecked` on a class or method checks types at compile time while the code still dispatches dynamically.
- Flow typing: with `@TypeChecked`, methods are selected from the inferred types of arguments, not declared types, to stay close to dynamic Groovy semantics. An `instanceof` check narrows the type, so the cast is optional.
- A method taking a `Closure` needs `@ClosureParams` (and `@DelegatesTo`) to give the checker closure parameter types; omitting `@ClosureParams` does not fail compilation.

## Gotchas
- Categories (`use`) cannot be used under `@TypeChecked`; metaprogramming that the checker cannot see needs a type checking extension.

## Checked

2026-11-02. Confirmed against the Semantics chapter (static type checking, flow typing, instanceof inference, `@ClosureParams`) and the Metaprogramming chapter (categories note). Removed: the compiler customizer recipe, `def x` reassignment rule and error-message claim.

Method: documentation only; no commands were run.

## Self-check
Add `@TypeChecked` to a method with a typo'd method call and confirm groovyc rejects it.
