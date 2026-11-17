---
id: computing-software.software-engineering.crystal.inheritance-abstract
name: inheritance-abstract
category: computing-software
field: software-engineering
product: crystal
tags: [inheritance-abstract, structs-vs-classes, inheritance, super, abstract-class, previous-def, subclass, polymorphism, override, crystal]
level: practitioner
status: docs-checked
description: "Model Crystal hierarchies: inheritance, overriding, super, previous_def, abstract classes and methods, virtual types."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/inheritance.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/virtual_and_abstract_types.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/methods_and_instance_variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance, super and abstract classes

Goal: model hierarchies.

- `class Employee < Person` inherits instance variables and instance and class methods. Defining `new` or `initialize` in the subclass hides the superclass constructors.
- Override a method by redefining it; or add specialised overloads with type restrictions.
- `super` with no arguments or parentheses passes all of the method's parameters; `super(x)` passes only what you give.
- Redefining a method in a reopened class: the last definition wins; `previous_def` calls the earlier one (also forwards all parameters when bare).
- A union of types in one hierarchy becomes a virtual type (`Animal+`), except for `Reference`, `Value`, `Int` and `Float`. Calling a method only defined on the subclasses then errors.
- `abstract class Animal` cannot be instantiated; `abstract def talk` makes the compiler check that all subclasses implement it (matching parameter types and names), even unused ones. Abstract methods also work in modules.
- `[Bar.new] of Foo` is an `Array(Foo)`; `[Foo.new] of Bar` is a compile error.
- `private` methods are callable only without receiver (or `self`) and are visible to subclasses; `protected` only from the type's scope and descendants.

Verify: spec calling `talk` on a collection of `Animal+` values.

## Checked
Checked 2026-11-02 against the crystal-book Inheritance, Virtual and abstract types, and Methods pages and Visibility. Removed: "single inheritance" (not stated in the pages read), the return-subtype and arg-compatibility rule, `super` inside blocks, the composition advice.

Method: documentation only; no commands were run.
