---
id: computing-software.software-engineering.c.sequence-points-and-evaluation-order
name: sequence-points-and-evaluation-order
category: computing-software
field: software-engineering
product: c
tags: [c, sequence-point, unsequenced-modification, evaluation-order, comma-operator]
level: advanced
status: docs-checked
description: "Avoid unsequenced side effects like i = i++ + 1 and unspecified argument evaluation order."
sources: ["https://en.cppreference.com/w/c/language/eval_order", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequence points and evaluation order

Goal: expressions whose result does not depend on compiler choices.

- Modifying an object twice, or modifying and reading it (other than to compute the new value), between sequence points is undefined: `i = i++ + 1;`, `a[i] = i++;`, `f(i, i++)`.
- Function arguments and operands of most binary operators are evaluated in unspecified order; only `&&`, `||`, `?:`, the comma operator and the end of a full expression sequence evaluations (C11 words this as "sequenced before").
- Calls to different functions with side effects as arguments, such as `f(read(), read())`, have unspecified order; assign to separate temporaries on separate statements.
- Keep one side effect per statement; avoid `++`/`--` inside larger expressions.
- GCC and Clang GCC's `-Wsequence-point` (in `-Wall`) catches many cases.

Verify: compile with both GCC and Clang with `-Wall`; differing results between compilers confirm unspecified behaviour.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference eval_order: unspecified order of operands and arguments, sequence points at `&&`, `||`, `,`, `?:` and full expressions, the undefined-behaviour examples (`i = i++ + 1`, `a[i] = i++`, `f(i, i++)`), and that distinct function calls are indeterminately sequenced; GCC manual `-Wsequence-point`, enabled by `-Wall`. Removed: `-Wunsequenced` for Clang (not verified).
Method: documentation only; no commands were run.
