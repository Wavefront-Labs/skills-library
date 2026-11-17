---
id: computing-software.software-engineering.refactoring.split-variable
name: split-variable
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, organizing-data, split-variable, single-assignment, temporary-variables, fowler-catalog]
level: practitioner
status: draft
description: "Split Variable: give each responsibility its own variable when one temp is reassigned for different purposes; mechanics, collecting variables, and parameter reuse."
sources:
  - https://refactoring.com/catalog/splitVariable.html
  - https://refactoring.guru/split-temporary-variable
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Split Variable

**Smell:** a variable assigned more than once for different meanings (`temp = 2 * (h + w); print(temp); temp = h * w; print(temp)`). Readers must track which meaning applies on each line, and Extract Function cannot pull either use out cleanly.

Exception: **collecting variables** (accumulators `total += x`, string builders, loop counters `i++`) are legitimately reassigned for one purpose. Leave them.

## Mechanics
1. Rename the variable at its declaration and first assignment to name the first meaning (`perimeter`).
2. Declare it `const`/`final`/`val` - compiler errors reveal any later assignment.
3. Change references up to the second assignment to the new name.
4. At the second assignment, declare a new variable with its own meaning (`area`).
5. Test, repeat for further assignments.

```javascript
// before
let temp = 2 * (height + width);
console.log(temp);
temp = height * width;
console.log(temp);
// after
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```

## Assigning to parameters
Reassigning an input parameter (`inputValue = inputValue - 50`) is the same smell and confuses pass-by-value expectations. Split: `let result = inputValue; if (inputValue > 50) result -= 50; return result;`. Linters: ESLint `no-param-reassign`, PMD `AvoidReassigningParameters`, Checkstyle `FinalParameters`.

## Tooling
- IntelliJ/ReSharper highlight reassigned locals; ESLint `prefer-const`, Rust `let` is immutable by default.
- After splitting, Replace Temp with Query often applies to the new single-assignment variables.

## Verify
- [ ] Each variable is const/final except deliberate accumulators.
- [ ] Tests green after each split.
