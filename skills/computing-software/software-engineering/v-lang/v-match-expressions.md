---
id: computing-software.software-engineering.v-lang.v-match-expressions
name: v-match-expressions
category: computing-software
field: software-engineering
product: v-lang
tags: [v-match-expressions, control-flow-if-and-match, match, switch, range match, else, match expression, pattern, v-lang]
level: practitioner
status: docs-checked
description: "Use match on ints, strings, enums and ranges, with comma lists, range arms 1..5 and else, as statement or expression."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# match expressions

Goal: replace long if chains.

```v
c := `v`
typ := match c {
    `0`...`9` { 'digit' }
    `A`...`Z` { 'uppercase' }
    `a`...`z` { 'lowercase' }
    else { 'other' }
}
```
- A `match` is a shorter way to write a sequence of `if - else`. The `else` branch runs when no other branch matches. A match expression returns the value of the final expression of the matching branch.
- Works on strings, ints, runes, enums, sum types and ranges. Comma separates several values in one arm: `.red, .blue { true }`.
- Ranges in branches use `...` (three dots), which is inclusive of the last element; `..` in a match branch throws an error. Constants can be used as range ends (`start...end`).
- Enum matches must be exhaustive or have `else`; with all variants covered, `else` is not allowed. Sum-type matches are exhaustive when every variant type is listed.
- `match true { 2 > 4 { ... } 2 == 2 { ... } else { ... } }` acts as an if/else-if chain; `match false` acts as an "unless".
- A match can return multiple values and can propagate results with `!` in its branches.
- Note from the docs: `match` as an expression is not usable in `for` loop and `if` statements conditions.

Verify: test boundary values of each range.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Match"). Removed as not stated there: "no fallthrough", `$if` arms in comptime match, string matching being a series of comparisons, the 3, 4, 9, 10 range example values.

Method: documentation only; no commands were run.
