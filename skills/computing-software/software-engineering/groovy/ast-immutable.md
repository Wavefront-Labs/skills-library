---
id: computing-software.software-engineering.groovy.ast-immutable
name: ast-immutable
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, ast-immutable]
level: practitioner
status: docs-checked
description: "@Immutable (and records in Groovy 4+) for final classes with defensive copies, and its limits."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://docs.groovy-lang.org/latest/html/gapi/
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_records.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable value objects
```groovy
import groovy.transform.Immutable
@Immutable class Pt { int x; int y }
def p = new Pt(1, 2)
try { p.x = 5 } catch (ReadOnlyPropertyException e) { println 'immutable' }
```
- Results are similar to `@Canonical` plus immutability: the class is made final and each property's backing field is final, so assignment throws `ReadOnlyPropertyException`.
- Property types must come from a predefined list of known immutable classes (for example `java.lang.String`) or compilation fails; extend the list with `knownImmutables` or `knownImmutableClasses` of `@ImmutableOptions`.
- Groovy also has record classes (documented as incubating) for plain data aggregates; see the Records chapter.

## Gotchas
- A property type outside the known-immutable list fails compilation unless you declare it in `@ImmutableOptions`.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (`@Immutable`, `@ImmutableBase`, `@ImmutableOptions`) and the Records chapter intro. Removed: collection copy, Date cloning, reflection and per-version record claims.

Method: documentation only; no commands were run.

## Self-check
Run the snippet and confirm the exception.
