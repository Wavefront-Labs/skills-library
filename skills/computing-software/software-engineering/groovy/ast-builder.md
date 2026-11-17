---
id: computing-software.software-engineering.groovy.ast-builder
name: ast-builder
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, ast-builder]
level: practitioner
status: docs-checked
description: "Generate builders with @Builder: default, simple, external, initializer and derived strategies."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://docs.groovy-lang.org/latest/html/gapi/
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @Builder strategies
```groovy
import groovy.transform.builder.*
@Builder class Person { String name; int age }
def p = Person.builder().name('a').age(3).build()
```
- Strategies: `DefaultStrategy` (nested helper class, named `<TypeName>Builder` by default), `SimpleStrategy` (chained setters), `ExternalStrategy` (explicit builder class, target class untouched, named with `forClass`), `InitializerStrategy` (single public constructor taking a fully set initializer).
- `SimpleStrategy` setter prefix defaults to `set`; the `prefix` attribute changes it.
- Annotate constructors or static factory methods too.

## Gotchas
- With `InitializerStrategy`, leaving a property unset is a compile error only under `@CompileStatic`; without it the strictness is not enforced.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (`@Builder` strategy table and the four strategy sections). Removed: the claim that builders do not validate.

Method: documentation only; no commands were run.

## Self-check
Run the snippet and assert `p.age == 3`.
