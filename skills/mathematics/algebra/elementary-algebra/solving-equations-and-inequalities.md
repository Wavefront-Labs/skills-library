---
id: mathematics.algebra.elementary-algebra.solving-equations-and-inequalities
name: solving-equations-and-inequalities
category: mathematics
field: algebra
product: elementary-algebra
tags: [elementary-algebra, algebra, equations, inequalities, linear-equations, quadratic-equations, quadratic-formula, discriminant, factorisation, factoring, completing-the-square, simultaneous-equations, systems-of-equations, substitution, elimination, rational-equations, extraneous-solutions, absolute-value, sign-chart, interval-notation, high-school-math, gcse, a-level, sat-math]
level: intro
status: verified
description: "Solve linear, quadratic, rational, radical and absolute-value equations and inequalities reliably, avoiding lost roots, extraneous roots and flipped-sign errors."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving equations and inequalities — without losing or inventing roots

**Goal:** get the complete, correct solution set of an equation or inequality in one
variable (or a small linear system), and know it is complete.

## 1. The one rule behind everything
Every step must be **reversible** (an equivalence). Adding the same thing to both sides,
multiplying by a *nonzero constant* — safe. The dangerous steps are:
- **Dividing by an expression** that could be zero → *loses* roots.
  `x² = 3x`: dividing by x gives `x = 3` and loses `x = 0`. Instead move everything to
  one side and factor: `x(x − 3) = 0`.
- **Squaring both sides** or **multiplying by an expression with x** → can *add* roots
  (extraneous). Always substitute back.
- **Multiplying/dividing an inequality by a negative** → flips the sign. If the sign of
  the multiplier is unknown (it contains x), don't multiply — use a sign chart.

## 2. By equation type
**Linear:** collect x terms one side, constants the other. If x cancels, you get either
`0 = 0` (every real number) or `0 = 5` (no solution) — say which.

**Quadratic `ax² + bx + c = 0`:**
1. Try factoring if roots look rational (discriminant a perfect square).
2. Otherwise `x = (−b ± √(b² − 4ac)) / (2a)`. Compute `D = b² − 4ac` first:
   D > 0 two real roots, D = 0 one repeated, D < 0 none real (two complex).
3. Completing the square (`a(x + b/2a)² = …`) is what you want when you also need the
   vertex or are integrating.
Gotcha: the `2a` divides the *whole* numerator, and `−b` with negative b is positive.

**Rational (x in a denominator):** note excluded values first (denominators ≠ 0),
multiply through by the LCD, solve, then discard any root that is an excluded value.

**Radical:** isolate the root, square, solve, **check every candidate** in the original.
`√(x+5) = x − 1` → `x² − 3x − 4 = 0` → x = 4 or −1; only x = 4 checks (−1 gives 2 = −2).

**Absolute value:** `|A| = k` (k ≥ 0) ⇔ `A = k` or `A = −k`. `|A| < k` ⇔ `−k < A < k`.
`|A| > k` ⇔ `A < −k` or `A > k`. `|A| = |B|` ⇔ `A = ±B`.

## 3. Inequalities: the sign-chart method
For polynomial or rational inequalities (`(x−2)/(x+1) ≥ 0`, `x² − x − 6 < 0`):
1. Get **0 on one side** (never cross-multiply by an x-expression).
2. Factor numerator and denominator fully.
3. Mark critical points (zeros of every factor) on a number line.
4. Test one point per interval, or track signs factor by factor.
5. Include zeros of the numerator if the inequality is `≤`/`≥`; **never** include
   zeros of the denominator.
Example: `(x−2)/(x+1) ≥ 0` → critical points −1, 2 → solution `x < −1 or x ≥ 2`,
i.e. `(−∞, −1) ∪ [2, ∞)`.

## 4. Two linear equations, two unknowns
- **Elimination:** scale to match a coefficient, subtract. Best when coefficients are tidy.
- **Substitution:** best when one variable already has coefficient 1.
- Contradiction (`0 = 7`) → parallel lines, no solution; identity (`0 = 0`) → same
  line, infinitely many. For three or more unknowns switch to row reduction (see
  mathematics.algebra.linear-algebra.eigenvalues-and-diagonalisation and its notes on systems).

## Gotchas
- `√(x²) = |x|`, not x. Solving `x² = 9` gives **±3**.
- `(a + b)² ≠ a² + b²`; `√(a + b) ≠ √a + √b`.
- A "solution" that makes any original denominator or radicand illegal is not a solution.
- Writing the answer: give the set, with interval brackets right (round at excluded or
  strict points, square at included ones).

## Checked
Run with SymPy 1.14: `√(x+5) = x − 1` solves to x = 4 only (x² − 3x − 4 = 0 has roots −1 and 4); `(x−2)/(x+1) ≥ 0` gives (−∞, −1) ∪ [2, ∞); `x² − x − 6 < 0` gives (−2, 3); `x² = 3x` has roots 0 and 3. The cross-referenced skill `mathematics.algebra.linear-algebra.eigenvalues-and-diagonalisation` exists in this library.

## Verify
- [ ] Substituted every root back into the **original** equation (mandatory after
      squaring or clearing denominators).
- [ ] For inequalities, tested one point inside each claimed interval and one outside.
- [ ] No division by an x-expression was used to simplify.
- [ ] Degree check: a degree-n polynomial has at most n roots — more means an error.
- [ ] Quick plot (Desmos/GeoGebra) agrees with crossings and intervals.
