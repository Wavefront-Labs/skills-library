---
id: computing-software.software-engineering.refactoring.slide-statements-and-move-statements
name: slide-statements-and-move-statements
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, moving-features, slide-statements, move-statements, move-statements-into-function, move-statements-to-callers, fowler-catalog]
level: practitioner
status: draft
description: "Slide Statements to group related code, and Move Statements into Function / to Callers to adjust a function's boundary; how to check that reordering is safe."
sources:
  - https://refactoring.com/catalog/slideStatements.html
  - https://refactoring.com/catalog/moveStatementsIntoFunction.html
  - https://refactoring.com/catalog/moveStatementsToCallers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slide Statements / Move Statements into Function / Move Statements to Callers

## Slide Statements
Put code that works together next to each other, usually as a prelude to Extract Function. Declare variables just before first use.
```javascript
const pricingPlan = retrievePricingPlan();
const order = retrieveOrder();
let charge;
const chargePerUnit = pricingPlan.unit;
// slide: move `let charge` down next to where it is computed and the plan-related lines together
```
**Is the slide safe?** You cannot move a statement past another if:
- one writes a variable the other reads or writes (data dependency),
- either has an observable side effect that must keep its order (I/O, logging, mutation of shared objects, exceptions thrown),
- one modifies an object the other reads through an alias.
Command-query separated code (queries have no side effects) slides freely. When unsure, slide one line at a time and test.

## Move Statements into Function
Every caller does the same thing right before or after calling a function: move that code into the function.
1. If the repeated code is not adjacent to the call, Slide Statements first.
2. If only one caller, cut and paste it in; otherwise Extract Function on one caller's call plus the statements, giving a new function.
3. Point other callers at the new function; then inline the old one and rename (Change Function Declaration).

## Move Statements to Callers
The inverse: a function's behaviour must now differ for some callers. Move the varying lines out to each caller.
1. Slide the varying statements to the start or end of the function.
2. Extract the remaining (common) body into a new function; inline the old function into all callers so each now has the common call plus the varying lines.
3. Adjust each caller's varying lines as needed.

## Verify
- [ ] Each move is a separate commit with tests green.
- [ ] Code review checks every slide that crosses an I/O, lock, or mutation.
