---
id: computing-software.software-engineering.groovy.constructors-named-args
name: constructors-named-args
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, constructors-named-args]
level: intro
status: docs-checked
description: "Positional constructors, map-based named-arg construction, @TupleConstructor and init order."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-object-orientation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constructors and map-style construction
- A class with only the default constructor accepts a Map: `new P(n: 'a', age: 3)` (calls no-arg constructor, then setters).
- Positional: define constructors or annotate with `@TupleConstructor`.

## Gotchas
- Named parameters work when no constructor, a no-arg constructor, or a constructor whose first argument is a `Map` (also `@MapConstructor`) is declared; once other constructors are declared you normally cannot use them.
- With a first-argument `Map` constructor, Groovy combines the named parameters into the Map, which suits `final` properties.

## Self-check
`@groovy.transform.TupleConstructor class A { int x; int y }; assert new A(1,2).y == 2`.

## Checked

2026-11-02. Confirmed against the Object orientation chapter (constructors, positional and named parameters). Removed: the this/super chaining line, property initialiser order and MissingPropertyException claims, and the wrong claim that a Map constructor breaks map-style construction.

Method: documentation only; no commands were run.
