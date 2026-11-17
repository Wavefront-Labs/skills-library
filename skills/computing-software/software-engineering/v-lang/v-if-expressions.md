---
id: computing-software.software-engineering.v-lang.v-if-expressions
name: v-if-expressions
category: computing-software
field: software-engineering
product: v-lang
tags: [v-if-expressions, control-flow-if-and-match, if, else if, if expression, ternary, conditions, bool, v-lang]
level: intro
status: docs-checked
description: "Use if/else if/else as statements and expressions, no parentheses, and ternary-style assignment with if."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if statements and if expressions

Goal: branch cleanly.

- No parentheses around the condition and the braces are always required: `if a < b { ... } else if a > b { ... } else { ... }`.
- The condition cannot start with another `if`, not even parenthesized: store the inner `if` expression in a variable first. When the condition starts with a `match` expression, parentheses are required around the condition.
- There is no ternary operator; use `if` as an expression: `x = if c { 1 } else { 2 }`, `s := if num % 2 == 0 { 'even' } else { 'odd' }`.
- Each branch can hold several statements followed by a final value, which becomes the value of the whole expression.
- When the first branch has type `?T`, later branches may supply `T` or `none`.
- Comparing an enum with `==` or `!=` in an `if`/`match` expression lets the enum operand type shorthand values such as `.red` in the branches.

Verify: `assert (if 2 > 1 { 'y' } else { 'n' }) == 'y'`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "If", "If expressions"). Removed as not stated there: "conditions must be bool, no truthy checks", short-circuit remark, `in` in conditions example, stray-semicolon and unreachable-else gotchas.

Method: documentation only; no commands were run.
