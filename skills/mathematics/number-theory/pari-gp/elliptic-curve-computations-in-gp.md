---
id: mathematics.number-theory.pari-gp.elliptic-curve-computations-in-gp
name: elliptic-curve-computations-in-gp
category: mathematics
field: number-theory
product: pari-gp
tags: [pari-gp, pari, gp, elliptic-curves, ellinit, weierstrass-equation, conductor, discriminant, minimal-model, torsion, elltors, rank, ellrank, mordell-weil, ellap, point-counting, l-function, lfun, lmfdb, ellidentify, gp-scripting, number-theory, birch-swinnerton-dyer]
level: practitioner
status: gated
description: "Compute with elliptic curves in PARI/GP: ellinit and minimal models, conductor and reduction types, torsion, a_p and point counts, rank bounds with ellrank, L-values, and checking against the LMFDB."
sources: ["PARI/GP User's Guide and Reference (Elliptic curves chapter): ellinit, ellglobalred, elltors, ellap, ellrank, lfun", "Silverman, The Arithmetic of Elliptic Curves (2nd ed., Springer GTM 106)", "Cremona, Algorithms for Modular Elliptic Curves (2nd ed., CUP 1997)", "LMFDB, The L-functions and Modular Forms Database (lmfdb.org)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elliptic-curve computations in GP

**Goal:** take an elliptic curve over ℚ (or 𝔽_p), and in a few GP lines get its
standard invariants — minimal model, conductor, torsion, a_p, rank information,
L-function values — while knowing which outputs are proven and which are conditional.

## 1. Defining the curve
`E = ellinit([a1, a2, a3, a4, a6])` for the long Weierstrass form, or `ellinit([a4, a6])`
for y² = x³ + a4·x + a6. Over a finite field: `ellinit([a4, a6], p)` (or with an
`ffgen` element for 𝔽_q).
- `E.disc`, `E.j` give Δ and j; Δ = 0 means singular — in PARI 2.15.4 `ellinit` then returns the empty vector `[]` (it does not raise), so test `#E` before using E. A wrong number of entries (`ellinit([1,2,3])`, `ellinit([1,2,3,4])`) does raise `incorrect type in ellinit (t_VEC)`.
- Minimal model and reduction data: `G = ellglobalred(E)` returns `[N, v, c, F, L]` over ℚ: conductor `G[1]`, global Tamagawa number `G[3]` (`v` is an obsolete field); `E = ellminimalmodel(E)`.
- Local data at p: `elllocalred(E, p)` → Kodaira symbol and Tamagawa number.
- Identify against Cremona labels: `ellidentify(E)` (needs the `elldata` package) or
  look the curve up on the LMFDB by its coefficients.

## 2. Points and torsion
```
P = [2, 3]; ellisoncurve(E, P)   \\ check first!
Q = elladd(E, P, P); ellmul(E, P, 5)
elltors(E)                        \\ [order, structure, generators]
ellheight(E, P)                   \\ canonical height; 0 iff P is torsion
```
Mazur's theorem limits torsion over ℚ to ℤ/n (n ≤ 10 or 12) or ℤ/2 × ℤ/2m (m ≤ 4) —
an `elltors` result outside that list means a typo in the curve. The point at
infinity is `[0]`.

## 3. Reduction mod p and a_p
- `ellap(E, p)` gives a_p = p + 1 − #E(𝔽_p) for good p.
- `ellcard(E, p)` (point count) — uses SEA for large p.
- Hasse bound |a_p| ≤ 2√p is a free sanity check.
- `ellan(E, n)` lists the first n Dirichlet coefficients of L(E, s).

## 4. Rank: what you can and cannot get
- `ellrank(E)` returns `[r1, r2, s, L]`: lower and upper bounds for the rank via 2-descent, a Sha[2]-related indicator `s`, and a list `L` of independent points (run on PARI 2.15.4; check `?ellrank` on older versions). If the bounds agree, the rank is **proven** (modulo
  the correctness of the implementation); if not, the gap is Sha[2]-related ambiguity.
- `ellanalyticrank(E)` returns `[r, value]`: the numerically detected order of vanishing r of L(E, s) at s = 1 and the first non-zero derivative (for 389a1 it returned r = 2).
  It is a *conjecturally* equal quantity (BSD); analytic rank 0 or 1 implies the
  algebraic rank equals it (Gross–Zagier–Kolyvagin), higher values are evidence only.
- `ellsaturation(E, V, B)` (saturates the point set at all primes below B) and `ellheightmatrix` (Néron–Tate height pairing) help verify independence: a nonzero
  regulator (`matdet(ellheightmatrix(E, pts))`) proves the points are independent.

## 5. L-functions and BSD quantities
`L = lfuncreate(E); lfun(L, 1)` for L(E, 1); `lfun(L, 1, r)` for the r-th derivative.
`ellbsd(E)` returns the constant c with L^(r)(1)/r! = c·R·S (R regulator, S = #Sha), so S = lfun(L,1,r)/(r!·c·R); it should come out as a perfect square
integer up to numerical precision (checked on 37a1, rank 1: S = 1.0000000000; and 11a-type curve [0,-1,1,-10,-20], rank 0: S = 1.0000000000). `ellbsd` is documented in the PARI reference. Increase precision with `\p 60` (or
`default(realprecision, 60)`) and confirm stability.

## 6. Scripting
GP scripts in a `.gp` file, loaded with `\r file.gp`:
```
forprime(p = 3, 1000, if(ellap(E, p) == 0, print1(p, " ")))   \\ supersingular primes
```
Use `my(...)` for local variables inside functions, `parfor`/`parforprime` for parallel
loops (if built with threads), and `allocatemem()` for stack errors (all run or documented; `` to read a file, `\q` to quit and the `gp2c` compiler were not exercised here (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- `ellinit([a, b])` means y² = x³ + ax + b, but `ellinit([a1, a2, a3, a4, a6])` has five
  entries; supplying three or four entries is an error, not a shorthand.
- Many outputs depend on `realprecision`; L-values near zero need extra digits before
  concluding vanishing.
- Rank results that rely on unproven conjectures (analytic rank ≥ 2, Sha finiteness)
  must be labelled as such.
- Function availability (`ellrank`, `ellbsd`, `ellsaturation`) depends on the PARI version (checked on 2.15.4) — run `?ellrank` to check; the older-version fallback to Denis Simon's `ell.gp` scripts is unconfirmed (gated: unconfirmed, source is paywalled or blocked). `ellidentify` needs the `elldata` package (it failed here without it).

## Verify
- [ ] `ellisoncurve` true for every point used; curve non-singular.
- [ ] Conductor, torsion and a_p match the LMFDB entry for the curve.
- [ ] Rank claim says whether bounds agree (proven) or rely on analytic rank/BSD.
- [ ] Numerical L-values stable when `realprecision` is raised.
