---
id: computing-software.software-engineering.groovy.abstract-interface
name: abstract-interface
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, abstract-interface, groovy-inheritance]
level: intro
status: docs-checked
description: "Abstract classes, interfaces with default and private methods, inner and anonymous classes, and when a trait fits better in Groovy."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-object-orientation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Abstract classes and interfaces
- An abstract class is declared with the `abstract` keyword, cannot be instantiated, may contain fields, properties, and abstract or concrete methods; concrete subclasses must implement the abstract methods.
- An interface holds method signatures, which are public by default; using protected or package-private methods in an interface is an error.
- A class can implement several interfaces but extend only one class.
- Interfaces can have default methods, and the shared code for default methods may go in private methods.
- Inner classes can access private members of the enclosing class; anonymous inner classes are supported. Groovy 3+ also accepts the Java syntax for instantiating a non-static inner class.
- Annotation types are declared with `@interface`.
- Traits are the Groovy answer for reusable behaviour with state: a trait can carry state, a Java 8 default method cannot, and Java sees a trait as an interface without default methods.

## Checked

2026-11-03. Confirmed against the Object orientation chapter (inner classes, abstract classes, interfaces and default methods, annotations, traits versus Java 8 default methods). Removed: the version-gated and "unconfirmed" notes, the claim that interface constants are static final, and the code snippets and self-check.

Method: documentation only; no commands were run.
