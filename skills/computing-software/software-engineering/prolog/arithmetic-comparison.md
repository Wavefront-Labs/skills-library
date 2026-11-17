---
id: computing-software.software-engineering.prolog.arithmetic-comparison
name: arithmetic-comparison
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, arithmetic-comparison, bigints]
level: practitioner
status: docs-checked
description: "Compare with =:= and the other arithmetic operators, and use SWI-Prolog unbounded integers (GMP) and float flags safely."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arithmetic comparison and big integers
`=:=`, `=\=`, `<`, `>`, `=<`, `>=` evaluate both sides. `=` unifies and does not evaluate.
```prolog
?- 1+2 =:= 3.        % true
?- 1+2 = 3.          % false
?- X is 2**200.      % exact big integer (GMP)
?- X is 10.0**400.   % float overflow error unless flag float_overflow=infinity
?- current_prolog_flag(bounded, B).   % false
```
## Gotchas
- Floats are IEEE doubles; compare with tolerance: `abs(A-B) < 1.0e-9`.
- Rationals are introduced with `rdiv/2`, `rational/1` or `rationalize/1`; the flag `prefer_rationals` changes the result of `/` (and integer `^`).
## Self-check
Compute 100 factorial with a recursive predicate and verify no overflow.

## Checked

2026-11-02. SWI-Prolog manual sections on arithmetic (GMP unbounded integers, flag bounded, rational numbers, float flags table float_overflow error/infinity, prefer_rationals, rdiv/2, rational/1, floats as C double, ** and ^ with Int and Int). Removed: the 0.1+0.2 example (not stated in the manual).

Method: documentation only; no commands were run.
