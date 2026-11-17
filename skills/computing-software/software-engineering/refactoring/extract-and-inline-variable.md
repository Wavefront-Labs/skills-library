---
id: computing-software.software-engineering.refactoring.extract-and-inline-variable
name: extract-and-inline-variable
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, extract-variable, inline-variable, explaining-variable, readability, fowler-catalog]
level: practitioner
status: docs-checked
description: "Apply Extract Variable to name complex expressions and Inline Variable to remove names that add nothing, with the steps and the performance and short-circuit caveats."
sources: ["https://refactoring.guru/extract-variable", "https://refactoring.guru/inline-temp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extract Variable / Inline Variable

**Goal:** make an expression's intent readable by naming its parts, or remove a
temporary that only repeats what the expression already says.

## Extract Variable
Use it for a hard-to-understand expression: an `if` condition, a long arithmetic expression
without intermediate results, or a long multipart line.

Before:
```js
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```
After:
```js
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```
Steps:
1. Insert a new line before the expression and declare a variable there, assigned part of the expression.
2. Replace that part of the expression with the variable.
3. Repeat for the other complex parts.

Name the variable for its purpose. If the same expression is used in other places, the
extracted variable can be the first step towards Extract Method (Extract Function).

## Inline Variable (Inline Temp)
Use it when a temporary is assigned a simple expression and nothing more.

Before: `const isLate = order.dueDate < today; return isLate;`
After: `return order.dueDate < today;`

Steps: replace every use of the variable with the expression, then delete the declaration
and its assignment. It is often done as part of Replace Temp with Query or to pave the way
for Extract Method.

## Gotchas
- Extracting parts of `a() || b()` into variables makes both run every time; the original
  skips `b()` when `a()` is true. That can hurt performance if they do heavy work.
- A temp that looks useless may cache the result of an expensive operation reused several
  times; check before inlining.

## Verify
- [ ] Behaviour unchanged after each step.
- [ ] Each new variable is named for the concept, not its type.

## Checked
2026-11-01. Confirmed against the Refactoring Guru pages "Extract Variable" and "Inline Temp": the uses, steps, the short-circuit and caching drawbacks, and the link to Extract Method and Replace Temp with Query.
Removed: the Fowler mechanics wording (side-effect and immutability checks), IDE shortcut names and the side-effect gotcha, because no page read states them.
Method: documentation only; no commands were run.
