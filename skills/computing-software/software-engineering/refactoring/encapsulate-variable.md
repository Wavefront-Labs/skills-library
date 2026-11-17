---
id: computing-software.software-engineering.refactoring.encapsulate-variable
name: encapsulate-variable
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, encapsulate-variable, encapsulate-field, global-state, accessors, data-ownership]
level: practitioner
status: draft
description: "Wrap widely accessed mutable data (globals, public fields, module state) behind accessor functions so you can monitor, restrict and later restructure it."
sources: ["https://refactoring.com/catalog/encapsulateVariable.html", "Refactoring, 2nd ed. (Fowler), ch6 Encapsulate Variable"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encapsulate Variable

**Goal:** turn "anyone can read and write this data from anywhere" into a single
choke point, the prerequisite for changing how that data is stored or validated.

## When
- A global, module-level variable or public field is read/written from many places.
- You need to change its representation, add validation or logging, make it
  thread-safe, or find out who mutates it.
Data with wide scope is harder to refactor than functions: you can't redirect a raw
variable access, but you can redirect a function call.

## Mechanics
1. Create getter and setter functions around the variable.
   ```js
   let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };
   export function defaultOwner() { return defaultOwnerData; }
   export function setDefaultOwner(arg) { defaultOwnerData = arg; }
   ```
2. Run static checks.
3. Replace each reference with a call to the accessor; test after each.
4. Restrict visibility of the variable (unexport it, make it private) so new direct
   access fails to compile/lint.
5. Test.

## Going further: protect the contents too
Encapsulating the reference doesn't stop `defaultOwner().lastName = "x"`. Options:
- getter returns a copy: `return { ...defaultOwnerData };` (callers mutating the
  copy silently do nothing - surprising; add tests).
- return an immutable object/record (`Object.freeze`, records, frozen dataclass).
- encapsulate the record into a class with explicit methods (Encapsulate Record).

## Language notes
- C#/Kotlin/Swift/Python properties let you change a field to a computed accessor
  without changing call sites, so you can defer this refactoring until needed in those
  languages (but binary compatibility differs: field -> property breaks compiled C#
  consumers).
- In Java, IDE "Encapsulate Fields" automates steps 1-4.

## Verify
- [ ] grep finds no direct references to the variable outside its module.
- [ ] Visibility reduced so the compiler/linter prevents regression.
