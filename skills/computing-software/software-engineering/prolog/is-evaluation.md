---
id: computing-software.software-engineering.prolog.is-evaluation
name: is-evaluation
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-arithmetic, is-evaluation, arithmetic-is]
level: intro
status: docs-checked
description: "Compute with is/2 and arithmetic functions; understand instantiation errors and that is/2 is one-way evaluation."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# is/2
`Result is Expression` evaluates the right side as an arithmetic expression.
```prolog
?- X is 7 mod 3 + max(2, 5) * 2**3.     % 1 + 5*8 = 41
?- X is 7 / 2.        % 3.5 (prefer_rationals false); 7 // 2 = 3
?- X is truncate(3.7). % 3
?- X = 1 + 2.         % X = 1+2 (no evaluation)
```
## Gotchas
- `is/2` evaluates its right operand; use it with an unbound left operand, and test equality with `=:=` (`1 is sin(pi/2)` fails because the result is the float 1.0).
- `/` on two integers: with `prefer_rationals` false (the default) and `iso` false the result is an integer when the division is exact and a float otherwise; `//` is integer division using the `integer_rounding_function` flag (towards zero in C99).
- In SWI-Prolog `^/2` is equivalent to `**/2`: with integer inputs and an integer result the result is an integer, otherwise a float; `float/1` forces a float result.
## Self-check
Evaluate `X is 5 / 2`, `X is 5 // 2`, `X is -5 // 2` and `X is -5 mod 2` and explain each.

## Checked

2026-11-02. SWI-Prolog manual arithmetic section: is/2 (sin(pi/2) example), mod/2 (floored), //, / (depends on prefer_rationals and iso, default false), truncate/1, max/2, **/2 and ^/2 (equivalent in SWI-Prolog, integer result for integer inputs, float otherwise). Removed: the clpfd advice and the instantiation-error claim.

Method: documentation only; no commands were run.
