---
id: computing-software.software-engineering.d.d-operators-precedence-assignment
name: d-operators-precedence-assignment
category: computing-software
field: software-engineering
product: d
tags: [d-operators-precedence-assignment, expressions, operators, precedence, power-operator, concatenation, in-operator, is-operator, short-circuit, d]
level: practitioner
status: docs-checked
description: "Use D operators correctly: ^^ power, ~ concatenation, in and !in, is and !is, shifts, comma expressions and the rule on mixing bit operators with comparisons."
sources:
  - https://dlang.org/spec/expression.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operators, precedence and assignment expressions

Goal: write operator expressions without surprises.

- `^^` raises the left operand to the power of the right (`2^^10`); `~` concatenates (string literals are concatenated at compile time) and `~=` appends.
- `a in aa` returns a pointer to the value or null (use `if (auto p = k in aa)`); `!in` negates.
- `is` compares identity (`e1 !is e2` for non-identity): class references are identical when they are the same object, and class references can be compared against null with `is`.
- `==` on class references calls `object.opEquals`; on structs it uses `opEquals`, generated member-wise if absent.
- `&&` and `||` short-circuit; in D the result of a comma expression cannot be used.
- `>>` is a signed right shift and `>>>` an unsigned one; a shift by a negative count, or by at least the operand's bit size, is undefined (a compile error when known at compile time).
- An `|`, `^` or `&` expression directly on either side of `==`, `is` or a relational operator is a compile error: parenthesise, e.g. `(a & b) == c`.

Gotchas:
- `~` produces a new container, so building a string with `~` in a loop allocates each time.

Verify: unittest asserts such as `assert(2^^10 == 1024)`.

## Checked
Checked 2026-11-03 against the D spec Expressions page (equality, identity, `in`, shift, comma, pow, concatenation, bitwise-with-comparison rule). Removed: the `%` on floats remark, array lexicographic comparison, the null-array remark, the "matches C" precedence claim (D makes the mixed expression an error) and the associativity claim.

Method: documentation only; no commands were run.
