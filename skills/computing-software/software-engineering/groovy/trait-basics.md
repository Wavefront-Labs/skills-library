---
id: computing-software.software-engineering.groovy.trait-basics
name: trait-basics
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, trait-basics, groovy-traits]
level: practitioner
status: docs-checked
description: "Groovy traits: properties and methods, private methods, extending traits, runtime mixin with as and withTraits, and conflict resolution."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_traits.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining and implementing traits
- A trait may define properties; they become visible on the implementing class and are used through the regular property accessors. Inside a trait, `this` represents the implementing instance: think of a trait as a superclass.
- Traits support only `public` and `private` methods; `protected` and package-private scopes are not supported. A private trait method is not part of the contract and cannot be called from outside.
- A trait can extend another trait with the `extends` keyword, and then has access to the super-trait's properties.
- A class can implement several traits. If two traits provide the same method, the method from the last declared trait in the `implements` clause wins; call a specific one with the `Trait.super.foo` syntax.
- At runtime, `obj as Trait` applies a trait to an object; use `withTraits` to apply several traits at once.
- Internally a trait is represented as an interface without default methods plus helper classes.

## Checked

2026-11-03. Confirmed against the traits section of the Groovy language documentation (`_traits.adoc`: properties, `this`, public and private methods, extends, conflict resolution, `as`, `withTraits`, implementation). Removed: the code snippet and self-check, the synthetic getter/setter field claim, and the `$self` and `@CompileStatic` version note.

Method: documentation only; no commands were run.
