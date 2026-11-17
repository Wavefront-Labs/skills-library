---
id: computing-software.software-engineering.refactoring.replace-temp-with-query
name: replace-temp-with-query
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, encapsulation, replace-temp-with-query, extract-function, temporary-variables, long-method, fowler-catalog]
level: practitioner
status: docs-checked
description: "Replace Temp with Query: move the expression behind a temp variable into a method so it can be reused and so Extract Method on a long method gets easier."
sources:
  - https://refactoring.guru/replace-temp-with-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Temp with Query

**Why:** a temp holding an expression's result ties that expression to one method body. Moving it to its own method lets other methods reuse it, removes duplication, names the idea, and lays groundwork for Extract Method on part of a very long method.

## Before / after
```javascript
// before
calculateTotal() {
  const basePrice = this.quantity * this.itemPrice;
  return basePrice > 1000 ? basePrice * 0.95 : basePrice * 0.98;
}
// after
calculateTotal() {
  return this.basePrice() > 1000 ? this.basePrice() * 0.95 : this.basePrice() * 0.98;
}
basePrice() { return this.quantity * this.itemPrice; }
```

## Mechanics
1. Check the variable is assigned exactly once in the method. If not, use Split Temporary Variable first.
2. Extract the expression into a new method (Extract Method). The method must only return a value and not change object state; if it does, use Separate Query from Modifier first.
3. Replace each use of the variable with a call to the new method.

## Gotchas
- Performance: the extra calls cost something, though modern compilers and CPUs usually make it minimal. If the temp caches a truly time-consuming expression, stop after extracting the method and keep the temp.

## Verify
- [ ] Tests unchanged and green after each step.
- [ ] The new method has no side effects.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page for this technique: problem, solution, steps (single assignment, query-only method, replace the variable), benefits and the performance note. Removed: the const/final step, memoisation advice, the loop-counter rule and the profiler claim, which that page does not state. The refactoring.com catalog page returns no text and is not cited.
Method: documentation only; no commands were run.
