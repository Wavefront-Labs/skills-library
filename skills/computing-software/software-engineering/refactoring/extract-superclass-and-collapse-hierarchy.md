---
id: computing-software.software-engineering.refactoring.extract-superclass-and-collapse-hierarchy
name: extract-superclass-and-collapse-hierarchy
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, inheritance, extract-superclass, collapse-hierarchy, replace-superclass-with-delegate, replace-subclass-with-delegate, fowler-catalog]
level: practitioner
status: draft
description: "Extract Superclass to share behaviour between similar classes, Collapse Hierarchy when levels merge, and when to replace inheritance with delegation instead."
sources:
  - https://refactoring.com/catalog/extractSuperclass.html
  - https://refactoring.com/catalog/collapseHierarchy.html
  - https://refactoring.com/catalog/replaceSuperclassWithDelegate.html
  - https://refactoring.com/catalog/replaceSubclassWithDelegate.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extract Superclass / Collapse Hierarchy (and the delegate alternatives)

## Extract Superclass
**When:** two classes do similar things (`Employee` and `Department` both have `name` and `annualCost` computed from monthly costs).
Mechanics:
1. Create an empty superclass; make both classes extend it (if they already have different superclasses, you cannot - use Extract Class/delegation instead).
2. Pull Up Constructor Body, Pull Up Field, Pull Up Method one at a time; test after each.
3. Examine remaining methods for common parts: Extract Function then Pull Up.
4. Check clients: can some now use the superclass type?
IDE: IntelliJ "Extract Superclass", "Extract Interface" (often better: share the contract, not the implementation).

## Collapse Hierarchy
**When:** a subclass and its superclass are no longer meaningfully different (after other refactorings moved things around). Pick which one to keep, Pull Up or Push Down all members into it, change references, delete the empty class.

## Prefer delegation when
Fowler (2nd ed.) adds two refactorings because inheritance is often misused:
- **Replace Superclass with Delegate:** the subclass does not satisfy "is-a" for every superclass operation (classic: `Stack extends Vector` exposing `insertElementAt`). Hold the former superclass as a field and forward only what you need.
- **Replace Subclass with Delegate:** you need to vary along more than one axis, or the variant must change at runtime (a booking that becomes premium). Move the variant behaviour to a delegate object.
Rule: inherit for genuine is-a with substitutability (Liskov); otherwise compose. Inheritance is fine to start with and easy to replace later with these refactorings.

## Gotchas
- Superclasses become dumping grounds ("BaseService" with unrelated helpers). Keep them cohesive.
- Deep hierarchies (> 3 levels) are hard to reason about; flatten or compose.
- Serialisation/ORM mappings change when the hierarchy changes.

## Verify
- [ ] Duplicate code between the former siblings is gone (CPD/jscpd report).
- [ ] Substitutability: superclass-typed tests run against each subclass.
