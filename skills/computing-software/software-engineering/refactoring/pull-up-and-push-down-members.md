---
id: computing-software.software-engineering.refactoring.pull-up-and-push-down-members
name: pull-up-and-push-down-members
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, inheritance, inheritance-refactoring, pull-up-method, push-down-method, pull-up-field, push-down-field, pull-up-constructor-body, fowler-catalog]
level: practitioner
status: draft
description: "Pull Up and Push Down methods, fields and constructor bodies to put members at the right level of a class hierarchy; mechanics, duplication checks and IDE support."
sources:
  - https://refactoring.com/catalog/pullUpMethod.html
  - https://refactoring.com/catalog/pushDownMethod.html
  - https://refactoring.com/catalog/pullUpField.html
  - https://refactoring.com/catalog/pullUpConstructorBody.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pull Up / Push Down Method and Field

## Pull Up Method
**When:** subclasses have methods with identical bodies (often after Parameterize Function or making them identical through small edits).
Mechanics:
1. Inspect the methods; make them identical if they differ only slightly (signature, field names).
2. Check every call and field reference inside the body can be resolved from the superclass. If it uses a subclass field, Pull Up Field first; if it calls a subclass-only method, declare it abstract in the superclass.
3. Copy one method into the superclass; delete it from one subclass; test. Delete from the others.

## Pull Up Field
Subclasses declare the same field (possibly with different names) used the same way: rename to match, move the declaration up, check visibility (`protected` or accessor).

## Pull Up Constructor Body
Common constructor statements move into a superclass constructor called via `super(...)`. Statements that must run after subclass-specific setup become a template method or stay in subclasses.

## Push Down Method / Field
**When:** a superclass member is relevant to only one (or some) subclasses.
Mechanics: copy the member into each subclass that needs it, remove it from the superclass, test. If callers use the superclass type and invoke the member, pushing down breaks them: they need a subclass type, or the member stays (perhaps as an abstract method).

## IDE support
IntelliJ "Pull Members Up"/"Push Members Down" (Refactor menu), Rider/ReSharper equivalents, Eclipse JDT. They detect conflicts (references to members that would not be visible).

## Gotchas
- Pulling up methods that are identical by accident (same code, different meaning) couples subclasses that will diverge.
- Changing a member's declared level changes binary compatibility for published libraries.
- In languages with structural typing or mixins (TypeScript, Python), consider composition instead of deepening inheritance.

## Verify
- [ ] Duplicate detection (PMD CPD, jscpd, SonarQube) shows the duplicate gone.
- [ ] Tests green after each subclass change.
