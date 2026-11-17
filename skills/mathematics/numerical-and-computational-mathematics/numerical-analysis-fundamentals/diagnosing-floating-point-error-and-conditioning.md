---
id: mathematics.numerical-and-computational-mathematics.numerical-analysis-fundamentals.diagnosing-floating-point-error-and-conditioning
name: diagnosing-floating-point-error-and-conditioning
category: mathematics
field: numerical-and-computational-mathematics
product: numerical-analysis-fundamentals
tags: [numerical-analysis, floating-point, ieee-754, machine-epsilon, rounding-error, cancellation, catastrophic-cancellation, condition-number, conditioning, backward-stability, forward-error, backward-error, relative-error, log1p, expm1, kahan-summation, compensated-summation, newton-method, finite-differences, error-analysis]
level: practitioner
status: verified
description: "Tell a badly conditioned problem from an unstable algorithm: estimate condition numbers, spot cancellation, pick step sizes, and rewrite formulas so float64 answers can be trusted."
sources: ["Higham, Accuracy and Stability of Numerical Algorithms (2nd ed., SIAM 2002)", "Trefethen & Bau, Numerical Linear Algebra (SIAM 1997), lectures 12-15", "Goldberg, What Every Computer Scientist Should Know About Floating-Point Arithmetic (1991)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing floating-point error and conditioning

**Goal:** when a computed number looks wrong (or you need to know how many digits to
trust), decide whether the *problem* is sensitive (ill-conditioned) or the *method* is
throwing accuracy away (unstable), and fix the right one.

## 1. Know the unit you are measuring in
- IEEE 754 double (`float64`): unit roundoff u = 2^-53 ≈ 1.1e-16; "machine epsilon"
  is usually quoted as 2^-52 ≈ 2.2e-16 (`numpy.finfo(float).eps`). Check which one a
  library calls eps before using it in a tolerance.
- Single (`float32`): u ≈ 6e-8, about 7 decimal digits. GPU and ML code often runs here
  silently.
- Every basic operation is exact-then-rounded: fl(x op y) = (x op y)(1 + δ), |δ| ≤ u.
  The error is *relative*, so a large result has a large absolute error.

## 2. The master rule of thumb
**forward error ≲ condition number × backward error.**
- *Condition number* κ: how much the exact answer moves when the input moves (relative).
  It belongs to the problem, not the algorithm.
- *Backward error*: the smallest input perturbation for which your computed answer is
  exact. A backward-stable algorithm achieves O(u).
- So with a stable algorithm you lose about log10(κ) digits out of ~16. κ = 1e10 leaves
  ~6 trustworthy digits; κ ≥ 1e16 means the answer can be all noise and no algorithm in
  double precision will save it.

Common condition numbers:
| Problem | κ |
|---|---|
| f(x) scalar | \|x f'(x) / f(x)\| |
| x − y | (\|x\|+\|y\|)/\|x − y\| — huge when x ≈ y |
| Ax = b | κ(A) = ‖A‖‖A⁻¹‖ (`numpy.linalg.cond`) |
| simple root of p | 1/\|x p'(x)\| scaled by coefficient sizes — multiple roots are ill-conditioned |

## 3. Spot the usual accuracy killers
1. **Catastrophic cancellation** — subtracting nearly equal rounded numbers. The
   subtraction is exact; it just exposes earlier rounding. Fixes: rewrite algebraically.
   - `1 - cos(x)` → `2*sin(x/2)**2`
   - `sqrt(x+1) - sqrt(x)` → `1/(sqrt(x+1)+sqrt(x))`
   - `log(1+x)`, `exp(x)-1` for small x → `log1p(x)`, `expm1(x)`
   - quadratic formula: compute the root with no cancellation, q = −(b + sign(b)√disc)/2,
     then x1 = q/a, x2 = c/q.
2. **Summation of many terms** — error grows with n and with the size of partial sums.
   Use `math.fsum`, Kahan/compensated summation, or pairwise summation (NumPy docs: `sum` uses partial pairwise summation always when no `axis` is given, and with an `axis` only along the fast memory axis; for float32 data pass `dtype=np.float64`: on 10^7 float32 values of 0.1 a float64 accumulator gave 1000000.0149 versus a naive Python sum of the first 10^6 float32 values drifting to 100000.0015).
3. **Overflow/underflow in intermediates** — `sqrt(x*x + y*y)` overflows; use `hypot`.
   Softmax: subtract the max first. Products of probabilities: work in logs.
4. **Comparing floats with `==`** — use `abs(a-b) <= rtol*max(|a|,|b|) + atol`;
   `atol` matters near zero, where relative tolerance is meaningless.

## 4. Finite-difference step size (a classic trap)
Forward difference (f(x+h) − f(x))/h has truncation error ~h and rounding error ~u/h,
so the best h ≈ √u·|x| ≈ 1e-8·|x|. Central differences: h ≈ u^(1/3)·|x| ≈ 6e-6·|x|.
Making h "smaller for accuracy" past that point makes the answer *worse* (measured for d/dx exp at x=1: forward-difference error 1.4e-4 at h=1e-4, 6.6e-9 at 1e-8, 4.3e-4 at 1e-12, 2.7 at 1e-16; complex step with h=1e-20 gave 0 error). Complex-step
(Im f(x+ih)/h, for real-analytic f) avoids the cancellation entirely and allows h = 1e-20.

## 5. Root finding: what the stopping test means
Newton's method converges quadratically near a simple root but only linearly at a
multiple root and can diverge from a poor start. Safeguard with a bracket (e.g. Brent's
method, `scipy.optimize.brentq`) when you have a sign change. Stop on both a small step
|x_{k+1} − x_k| ≤ tol·|x_k| *and* a small residual — a tiny residual alone is not a
small error when the root is ill-conditioned.

## 6. Diagnostic experiments (do these before blaming the algorithm)
- **Perturb the input** by ~1e-12 relative and recompute; a big output swing = the
  problem is ill-conditioned.
- **Rerun in higher precision** (`mpmath`, `numpy.longdouble` — note on some platforms
  longdouble is just float64) or in float32; digits that agree are probably real.
- **Compute the residual** (e.g. ‖Ax − b‖/(‖A‖‖x‖)); O(u) residual with a wrong-looking
  answer points at conditioning, not at a bug.

## Gotchas
- Reformulating the *model* (e.g. a better basis, scaling variables to similar
  magnitudes) can reduce κ; no amount of algorithmic care reduces it otherwise.
- Confirmed in NumPy: `finfo(float).eps` = 2^-52 = 2.22e-16 and `finfo(float32).eps` = 1.19e-7; the 2^-53 unit roundoff is the textbook u. Check what any other library calls eps.

## Verify
- [ ] You can state κ (or an estimate) and how many digits it leaves you.
- [ ] Inputs perturbed at the 1e-12 level change the answer only as κ predicts.
- [ ] Every subtraction of close quantities has been rewritten or justified.
- [ ] Tolerances combine relative and absolute parts and use the right epsilon.
- [ ] A higher-precision rerun agrees with the digits you report.
