---
id: mathematics.number-theory.elementary-number-theory.solving-linear-congruences-and-the-crt
name: solving-linear-congruences-and-the-crt
category: mathematics
field: number-theory
product: elementary-number-theory
tags: [elementary-number-theory, modular-arithmetic, congruences, linear-congruence, euclidean-algorithm, extended-euclidean-algorithm, bezout, modular-inverse, chinese-remainder-theorem, crt, fermats-little-theorem, euler-totient, eulers-theorem, modular-exponentiation, linear-diophantine-equations, gcd, python-pow, number-theory]
level: intro
status: verified
description: "Solve ax ≡ b (mod m), systems of congruences and linear Diophantine equations by hand or in code: extended Euclid, modular inverses, the CRT (including non-coprime moduli) and Fermat/Euler."
sources: ["Niven, Zuckerman & Montgomery, An Introduction to the Theory of Numbers (5th ed., Wiley 1991)", "Hardy & Wright, An Introduction to the Theory of Numbers (6th ed., OUP 2008)", "Python documentation: built-in pow with negative exponent and modulus (3.8+)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving linear congruences and the Chinese Remainder Theorem

**Goal:** find all integers x satisfying one or several congruences, or all integer
solutions of ax + by = c, with the extended Euclidean algorithm as the single engine.

## 1. Extended Euclid (the engine)
gcd(a, b) and integers s, t with s·a + t·b = gcd(a, b) (Bézout). By hand, keep a table:

| r | q | s | t |
|---|---|---|---|
| 240 | | 1 | 0 |
| 46 | | 0 | 1 |
| 10 | 5 | 1 | −5 |
| 6 | 4 | −4 | 21 |
| 4 | 1 | 5 | −26 |
| 2 | 1 | −9 | 47 |
| 0 | 2 | | |
Each row = previous-but-one minus q × previous. Result: gcd = 2 = −9·240 + 47·46.
**Check the final identity numerically** — it catches every arithmetic slip.

In code: Python ≥ 3.8 `pow(a, -1, m)` returns the inverse of a mod m (docs; raises
`ValueError` if gcd(a, m) ≠ 1, confirmed); `math.gcd`; SymPy `sympy.ntheory.modular.crt` and `solve_congruence` (both run on SymPy 1.14.0). PARI/GP has its own modular arithmetic and CRT functions (see its manual). The table above was recomputed and matches (the final row is `0 | 2 | 23 | -120`).

## 2. One congruence: ax ≡ b (mod m)
Let g = gcd(a, m).
- If g ∤ b: **no solutions**.
- If g | b: divide through: (a/g)x ≡ b/g (mod m/g); a/g is invertible mod m/g, so
  x ≡ (a/g)⁻¹(b/g) (mod m/g). That is **g distinct solutions mod m**:
  x₀, x₀ + m/g, …, x₀ + (g−1)m/g.
Example: 6x ≡ 4 (mod 10): g = 2 | 4 → 3x ≡ 2 (mod 5) → x ≡ 2·2 ≡ 4 (mod 5) →
x ≡ 4, 9 (mod 10). Check: 6·4 = 24 ≡ 4 ✓, 6·9 = 54 ≡ 4 ✓.

## 3. Linear Diophantine equation ax + by = c
Solvable iff g = gcd(a, b) divides c. From Bézout s·a + t·b = g, a particular solution
is (x₀, y₀) = (s·c/g, t·c/g); all solutions:
x = x₀ + (b/g)k, y = y₀ − (a/g)k, k ∈ ℤ.
For non-negative solutions, bound k from both inequalities and list the integers in the
interval.

## 4. Systems: the Chinese Remainder Theorem
x ≡ a₁ (mod m₁), …, x ≡ a_k (mod m_k) with **pairwise coprime** moduli has a unique
solution mod M = m₁⋯m_k:
x = Σ a_i M_i y_i, where M_i = M/m_i and y_i = M_i⁻¹ mod m_i.
Easier by hand: **solve iteratively** — from x = a₁ + m₁t substitute into the second
congruence, solve for t mod m₂, and continue.

**Non-coprime moduli:** x ≡ a (mod m), x ≡ b (mod n) is solvable iff
a ≡ b (mod gcd(m, n)); the solution is unique mod lcm(m, n). The iterative method
handles this automatically via step 2 (it reports "no solution" when g ∤ b). Many
library CRT routines assume coprime moduli, so check. Tested: SymPy `solve_congruence((1,4),(3,6))` gives `(9, 12)` (modulus lcm = 12) and `None` for the inconsistent `(1,4),(2,6)`; `crt(m, v)` has `check=True` by default, and with `check=False` on non-coprime moduli it returned `(0, 24)` for an inconsistent system, so do not disable the check.

## 5. Powers: Fermat and Euler
- Fermat: p prime, p ∤ a ⇒ a^{p−1} ≡ 1 (mod p). Euler: gcd(a, n) = 1 ⇒ a^{φ(n)} ≡ 1
  (mod n). Reduce exponents mod φ(n) (or mod the order of a) — only when a is
  coprime to n.
- Compute a^e mod n by square-and-multiply (`pow(a, e, n)`), never `a**e % n` for large e.
- For composite n, split with CRT: compute mod each prime power, recombine.

## Gotchas
- "Dividing" a congruence by d is only valid mod m/gcd(m, d), or when d is invertible.
- Negative remainders: Python's `%` returns a non-negative result for positive m; C,
  Java and JavaScript return a negative one for negative operands. Normalise.
- φ(n) requires the factorisation of n; for large n that is the hard part (that's
  what RSA relies on).
- SymPy 1.14.0 signatures: `crt(m, v, symmetric=False, check=True)`, `solve_congruence(*remainder_modulus_pairs, **hint)`; they can differ by version, check `help()` locally.

## Verify
- [ ] Bézout identity checked numerically.
- [ ] Number of solutions mod m equals gcd(a, m) (or zero) as predicted.
- [ ] Every solution substituted back into every original congruence.
- [ ] For CRT, final answer reduced to the range [0, lcm) and checked mod each modulus.
