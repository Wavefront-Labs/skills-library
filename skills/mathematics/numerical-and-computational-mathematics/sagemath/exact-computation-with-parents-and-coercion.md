---
id: mathematics.numerical-and-computational-mathematics.sagemath.exact-computation-with-parents-and-coercion
name: exact-computation-with-parents-and-coercion
category: mathematics
field: numerical-and-computational-mathematics
product: sagemath
tags: [sagemath, sage, computer-algebra, cas, parents, coercion, polynomial-ring, qq, realfield, preparser, exact-arithmetic, symbolic-ring, maxima]
level: practitioner
status: docs-checked
description: "Compute exactly in SageMath: put objects in the right parent, understand coercion versus conversion and the preparser, and check results."
sources:
  - https://doc.sagemath.org/html/en/tutorial/tour_algebra.html
  - https://doc.sagemath.org/html/en/tutorial/afterword.html
  - https://doc.sagemath.org/html/en/reference/coercion/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exact computation in SageMath with parents and coercion

**Goal:** get exact, correct answers from SageMath by putting every object in the
algebraic structure (its *parent*) you mean, instead of letting it fall into the
symbolic ring.

## 1. Everything has a parent
Every Sage element has a parent: `parent(x)`. Parents include `QQ` (rationals),
`RealField(n)` (floats with n bits of precision) and polynomial rings made with
`PolynomialRing`. Symbolic variables made with `var('x')` are symbolic expressions, and
Sage's calculus uses an interface to Maxima. For algebra prefer an explicit ring over
symbolic expressions, and check `parent()` of inputs and outputs.

## 2. The preparser
Sage pre-parses command lines before passing them to Python: `^` outside strings
becomes `**`, and integer literals are wrapped in `Integer( )`. So in Sage `1/3` is
the exact rational and `2^10` is a power. Plain Python code importing Sage (the
tutorial's Python tabs use `from sage.all import *`) must write `**` and
`Integer(1)/Integer(3)` itself.

## 3. Coercion versus conversion
The Sage coercion docs distinguish converting between parents (explicit, may involve
arbitrary choices such as a lift) from coercing (implicit, must be canonical, defined on
the whole domain and always succeeds).
- Test with `QQ.has_coerce_map_from(ZZ)`, which returns `True`.
- When no common parent can be found, arithmetic raises a `TypeError` about
  `unsupported operand parent(s)`. Fix it by converting explicitly into the parent you want.
- Floating-point literals pull results into an inexact parent; write exact fractions
  in exact work.

## Gotchas
- Do not run exact algorithms (rank, kernel) on floating-point matrices; the results are
  not exact.
- Method and backend names change between Sage releases; confirm in the reference manual
  for your install.

## Verify
- [ ] `parent()` of inputs and outputs is what you intended.
- [ ] No floating-point literals in an exact computation.
- [ ] Results checked by substituting or multiplying back.

## Checked
2026-11-01. Confirmed in the Sage tutorial and coercion reference: `parent()`, `QQ`,
`RealField`, `PolynomialRing`, `var`, the Maxima interface, the preparser (`^` to `**`,
`Integer( )` wrapping), `has_coerce_map_from`, coercion versus conversion, the
`unsupported operand parent(s)` TypeError.
Removed (not stated on pages read): the table of ZZ, GF, Zmod, NumberField, QQbar, RDF,
CDF; `preparse()`, `.sage` versus `.py` behaviour, `R.<x>` notation, `srange`; the claim
that conversion loses information while coercion never does; backend (PARI, FLINT,
Singular, GAP) statements; worked factor, Groebner and graph examples; speed claims.
Method: documentation only; no commands were run.
