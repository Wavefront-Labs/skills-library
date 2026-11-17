---
id: mathematics.mathematical-analysis.complex-analysis.evaluating-real-integrals-by-residues
name: evaluating-real-integrals-by-residues
category: mathematics
field: mathematical-analysis
product: complex-analysis
tags: [complex-analysis, residue-theorem, residues, contour-integration, contour-integrals, poles, laurent-series, jordans-lemma, semicircle-contour, keyhole-contour, principal-value, indented-contour, trigonometric-integrals, improper-integrals, fourier-integrals, branch-cut, holomorphic-functions, mathematical-methods, physics-math]
level: advanced
status: verified
description: "Evaluate real integrals with the residue theorem: semicircle contours for rational and Fourier integrals, z = e^{iθ} for trig integrals, residue formulas, Jordan's lemma, indentations."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating real integrals by residues

**Goal:** compute definite real integrals that resist elementary antiderivatives by
turning them into contour integrals and summing residues.

## 1. Residue theorem and residue formulas
`∮_C f(z) dz = 2πi · Σ Res(f, z_k)` over poles **inside** C, C positively oriented
(counter-clockwise).
- **Simple pole:** `Res = lim_{z→z₀} (z − z₀) f(z)`; if f = g/h with g(z₀) ≠ 0 and h
  having a simple zero, `Res = g(z₀) / h'(z₀)` (usually fastest).
- **Pole of order m:** `Res = (1/(m−1)!) · d^{m−1}/dz^{m−1} [(z − z₀)^m f(z)]` at z₀.
- Messy cases: read the coefficient of `(z − z₀)^{−1}` from a Laurent expansion.

## 2. Type A — trig integrals over a full period
`∫₀^{2π} R(cos θ, sin θ) dθ`: put z = e^{iθ}, `cos θ = (z + z⁻¹)/2`,
`sin θ = (z − z⁻¹)/(2i)`, `dθ = dz/(iz)`; integrate over |z| = 1.
Example: `∫₀^{2π} dθ/(2 + cos θ)` → `∮ 2 dz / (i(z² + 4z + 1))`; poles at −2 ± √3;
only −2 + √3 is inside. Result **2π/√3**. (General: `2π/√(a² − b²)` for a > |b|.)

## 3. Type B — rational functions on ℝ
`∫_{−∞}^{∞} P(x)/Q(x) dx` with Q having no real zeros and `deg Q ≥ deg P + 2`:
close with a large upper semicircle (its contribution → 0 by the ML estimate), so the
answer is `2πi Σ Res` over poles in the **upper** half-plane.
Example: `∫ dx/(1 + x²)`: pole i, residue 1/(2i) ⇒ **π**.

## 4. Type C — Fourier-type integrals
`∫ e^{iax} P/Q dx`, a > 0, `deg Q ≥ deg P + 1`: close in the **upper** half-plane
(where |e^{iaz}| = e^{−a·Im z} ≤ 1); **Jordan's lemma** kills the arc. For a < 0 close
below and include a minus sign for clockwise orientation.
For `∫ cos(ax) f(x) dx` integrate `e^{iaz} f(z)` and take the real part — never put
cos(az) itself on the arc (it grows like e^{a|Im z|}).
Example: `∫ cos x /(1 + x²) dx = Re[2πi · e^{−1}/(2i)] = **π/e**`.

## 5. Poles on the real axis — indent
If f has a simple pole on the contour, the integral is a **principal value**; detour with
a small semicircle of radius r → 0 around it. A small semicircle around a simple pole
contributes `−πi · Res` (traversed clockwise above the pole), i.e. half a residue.
Example: `∫_{−∞}^{∞} sin x / x dx = Im PV∫ e^{iz}/z dz = π`.

## 6. Multivalued integrands
`∫₀^∞ x^{α−1}/(1 + x) dx`, `∫₀^∞ ln x … dx`: use a **keyhole** contour around a branch
cut on the positive real axis; the two edges differ by a factor e^{2πiα}. Fix the branch
(argument in (0, 2π)) before computing residues. Answer for the example: π/sin(πα),
0 < α < 1.

Checked numerically: the Type A integral equals 2π/√3 = 3.62760 (quad and SymPy `residue`); Type C gives π/(2e) on (0, ∞) with `quad(weight='cos')`, so π/e on ℝ; the residue of 1/(1+z²) at i is −i/2 = 1/(2i); the keyhole result π/sin(πα) matched `mpmath.quad` at α = 0.3; `mpmath.quadosc` gives π/2 for ∫₀^∞ sin x/x dx.

## Gotchas
- Including poles in the wrong half-plane, or outside |z| = 1.
- Orientation: clockwise contours carry a minus sign.
- Proving the arc vanishes is part of the proof — state the degree condition or Jordan.
- Even integrands over (0, ∞): compute over ℝ and halve; odd ones need a different trick.
- Result must be real for a real integral; an imaginary leftover means an arithmetic slip.

## Verify
- [ ] Listed every pole and which are enclosed, with their orders.
- [ ] Arc and indentation contributions justified (→ 0, or the half-residue).
- [ ] Final value real and with the right sign (positive integrand ⇒ positive).
- [ ] Numerical check: `scipy.integrate.quad` (use `weight='cos'` / `'sin'` for
      oscillatory infinite-range integrals) or `mpmath.quad`.
