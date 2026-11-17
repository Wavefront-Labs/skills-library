---
id: computing-software.software-engineering.prolog.if-then-else-naf
name: if-then-else-naf
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, if-then-else-naf, negation-as-failure]
level: practitioner
status: docs-checked
description: "Use if-then-else, soft-cut, negation as failure and once/1 correctly, and avoid unsound negation with unbound variables."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# If-then-else and negation
- `( Cond -> Then ; Else )`: commits to the choices made in Cond. Without else, `( Cond -> Then )` fails if Cond fails.
- `( Cond *-> Then ; Else )`: soft cut; if Cond succeeds at least once this is `call(Cond), Then` and Cond can backtrack, otherwise Else runs.
- `\+ G`: true if G cannot be proven (SWI-Prolog compiles it as a control structure). `once/1` can in many cases be replaced with `->`; they differ in how cut behaves.
```prolog
sign(X, S) :- ( X > 0 -> S = pos ; X < 0 -> S = neg ; S = zero ).
?- \+ member(z, [a,b]).     % true
```
## Gotchas
- `\+ member(X, [a])` with X unbound fails because a proof exists; `\+` is negation as failure (weak negation), so call it on ground goals.
- `( If -> Then )` without `;` acts as `( If -> Then ; fail )`.
## Self-check
Predict `?- \+ \+ X = 1, var(X).` (X stays unbound) and run it.

## Checked

2026-11-02. SWI-Prolog manual control predicates: ->/2 (commits, defined as If, !, Then; If -> Then acts as If -> Then ; fail), *->/2 (soft cut semantics), \+/1 (cannot be proven, weak negation, compiled as control structure), once/1. Removed: dif/2 advice and the guard remark.

Method: documentation only; no commands were run.
