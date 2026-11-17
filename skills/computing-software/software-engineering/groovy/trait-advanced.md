---
id: computing-software.software-engineering.groovy.trait-advanced
name: trait-advanced
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, trait-advanced]
level: advanced
status: docs-checked
description: "Advanced Groovy traits: @SelfType constraints, stackable traits with super, static members per implementing class, and method scope limits."
sources:
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_traits.adoc
  - https://groovy-lang.org/objectorientation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trait self types, composition and limits
- `@groovy.transform.SelfType` states the types a class implementing the trait must inherit or implement, and makes the type checker aware of the trait's own type; a class that does not satisfy the constraint gets a compile-time error.
- Stackable traits: a trait can delegate to the next one with `super`. In a chain, `super` calls the next trait; when no trait is left, `super` refers to the superclass of the implementing class. Reordering the traits in the `implements` clause changes which handler runs first.
- Traits may extend another trait with `extends`.
- A trait may declare static methods, properties and fields. A static member declared on a trait belongs to the implementing class, not to the trait: two implementing classes each get a distinct static field.
- Only `public` and `private` methods are supported in traits (no `protected` or package-private).
- Java sees a trait as an interface without default methods.

## Checked

2026-11-03. Confirmed against the traits chapter (`_traits.adoc`: SelfType section, stackable traits, static methods and fields, method scope warning) and the Object orientation chapter. Removed: the right-to-left ordering claim, the `synchronized` limitation, and the self-check.

Method: documentation only; no commands were run.
