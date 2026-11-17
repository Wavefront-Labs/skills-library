---
id: computing-software.software-engineering.refactoring.replace-type-code-with-subclasses
name: replace-type-code-with-subclasses
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, inheritance, replace-type-code-with-subclasses, type-code, polymorphism, fowler-catalog]
level: practitioner
status: docs-checked
description: "Replace a type code field with subclasses so behaviour varies polymorphically, and know when to use State/Strategy instead."
sources:
  - https://refactoring.guru/replace-type-code-with-subclasses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Type Code with Subclasses

**Smell:** a field like `employee.type in ("engineer", "manager", "salesman")` is tested in conditionals (`if`, `switch`, `?:`) in several methods, so the coded values drive behaviour.

## When not to use it
- You already have a class hierarchy on another axis: you cannot build a second one by inheritance. Use Replace Type Code with State/Strategy (composition) instead.
- The type code can change after the object is created: the object's class cannot change on the fly. Use State/Strategy here too.

## Mechanics
1. Self-encapsulate the type code field (a getter).
2. Make the superclass constructor private and add a static factory method taking the type-code value; it returns the matching subclass. This holds the one conditional that remains.
3. Create a subclass per type-code value; override the getter to return that value.
4. Delete the type-code field from the superclass and make its getter abstract.
5. Move fields and methods into the subclasses with Push Down Field and Push Down Method.
6. Finish with Replace Conditional with Polymorphism to remove the remaining conditions on the type code.

## Why it helps
Adding a new value means adding a subclass without touching existing code (open/closed principle), the conditionals move out of the original class, and the language can type-check the values instead of raw strings or numbers.

## Verify
- [ ] No conditional on the type code remains outside the factory.
- [ ] Tests green after each step.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page for this technique: problem and solution, when not to use (existing hierarchy, mutable type), and the step list. Removed: the ORM mapping notes, the sealed-type and enum alternatives, the Remove Subclass section and the exhaustiveness check, which that page does not state. The refactoring.com catalog pages return no text and are not cited.
Method: documentation only; no commands were run.
