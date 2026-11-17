---
id: computing-software.software-engineering.prolog.term-ordering
name: term-ordering
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, term-ordering, standard-order]
level: practitioner
status: docs-checked
description: "Compare terms with ==, @<, compare/3 and the standard order Var < Number < Atom < String < Compound."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity and standard order of terms
- `==` structural identity; `=@=` structural equivalence (variant) ignoring variable names.
- Standard order: Var < Number < String < Atom < Compound.
- Compounds compare by arity, then name, then args left to right.
- Numbers compare by value; if equal, Float < Int.
```prolog
?- compare(O, 1, 1.0).        % O = (>)  (1.0 < 1 in standard order)
?- msort([b, 1, "s", f(x), A, 2.0], L).
?- f(A) =@= f(B).             % true
```
## Gotchas
- `1 =:= 1.0` is arithmetic equality (true); `1 == 1.0` is false.
- `sort/2` removes duplicates under `==`; `msort/2` keeps them.
- Variables are sorted by address; the manual warns that the ordering of variables has unexpected properties (for example it can change when variables are unified).
## Self-check
Predict `compare(O, a, "a")` then run it; check the String < Atom rule.

## Checked

2026-11-02. SWI-Prolog manual section Standard Order of Terms: Variables < Numbers < Strings < Atoms < Compound terms; numbers by value with the float smaller when equal; compound terms by arity, name, then arguments left to right; variables by address. Fixed: the skill had Atom before String.

Method: documentation only; no commands were run.
