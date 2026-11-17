---
id: computing-software.software-engineering.refactoring.replace-control-flag-with-break
name: replace-control-flag-with-break
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, replace-control-flag, conditional-logic, early-return, loops]
level: intro
status: docs-checked
description: "Remove control-flag variables that steer loops and functions, replacing them with break, continue or return so the control flow is explicit."
sources: ["https://refactoring.guru/remove-control-flag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Control Flag with Break

**Smell:** a boolean variable whose only job is to steer control flow later, used across several boolean expressions:
```js
let found = false;
for (const p of people) {
  if (!found) {
    if (p === "Don")  { sendAlert(); found = true; }
    if (p === "John") { sendAlert(); found = true; }
  }
}
```

## Mechanics
1. Find the assignment to the flag that causes the exit from the loop or the current iteration.
2. Replace it with `break` (leave the loop), `continue` (skip to the next iteration) or `return` (leave the function, with a value if needed).
3. Remove the remaining flag code and checks.

```js
for (const p of people) {
  if (p === "Don" || p === "John") { sendAlert(); break; }
}
```

## Why
Flags date from the single-entry, single-exit style of function writing, which modern languages make obsolete because loops have `break`, `continue` and `return`. Flag code is often more ponderous than code that uses these operators.

## Verify
- [ ] Behaviour is unchanged after each replacement (run tests).
- [ ] No leftover flag variable or check remains.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page for Remove Control Flag: problem, solution, meaning of break, continue and return, and the steps. Removed: the Extract Function step, the variants (nested loops, labelled break, while loops), the cleanup-code caveat and the library-call alternative, which that page does not state. The refactoring.com catalog page returns no text and the book page was not used.
Method: documentation only; no commands were run.
