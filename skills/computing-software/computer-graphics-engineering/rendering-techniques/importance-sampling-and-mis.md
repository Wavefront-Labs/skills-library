---
id: computing-software.computer-graphics-engineering.rendering-techniques.importance-sampling-and-mis
name: importance-sampling-and-mis
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, path-tracing, importance-sampling, multiple-importance-sampling, mis, power-heuristic, balance-heuristic, next-event-estimation, monte-carlo, russian-roulette, pbrt]
level: advanced
status: docs-checked
description: "Cut path tracer noise as pbrt-v4 does: importance sampling, MIS of light and BSDF samples with the power heuristic, delta lights, Russian roulette with etaScale, regularization."
sources: ["https://pbr-book.org/4ed/Light_Transport_I_Surface_Reflection/A_Better_Path_Tracer", "https://www.pbr-book.org/4ed/Monte_Carlo_Integration/Improving_Efficiency", "https://graphics.stanford.edu/papers/veach_thesis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importance sampling and MIS

**Goal:** converge a path tracer with fewer samples by sampling where the integrand is large and
combining strategies without bias. Follows pbrt-v4 section 2.2 (Improving Efficiency) and 13.4
(A Better Path Tracer). Veach's dissertation (1997) introduced multiple importance sampling and
efficiency-optimised Russian roulette.

## 1. Importance sampling
The Monte Carlo estimator converges faster when samples come from a distribution similar to the
integrand. A PDF exactly proportional to the integrand would give zero variance (but needs the
answer in advance). A badly chosen PDF can raise variance: sampling more where the integrand is
near zero and less where it is large makes the rare large-region samples very heavy.
Stratified sampling subdivides the domain into non-overlapping strata and never increases
variance; its drawback is the curse of dimensionality, so stratify some dimensions
independently.

## 2. Two strategies for direct lighting
- **BSDF sampling** is much more effective when the BSDF is large on a narrow set of directions
  (smooth surfaces, large light sources).
- **Light sampling** is more effective for small light sources and less concentrated BSDF lobes.
- Averaging one sample of each is of limited benefit, because variance adds. Use MIS.

## 3. Multiple importance sampling
Draw from several distributions and weight each sample so that large variance spikes from
mismatches are suppressed. For the estimator to be unbiased the weights must sum to 1 wherever
the integrand is nonzero, and a weight is zero where its PDF is zero.
- **Balance heuristic:** weight `nf*pf / (nf*pf + ng*pg)`; each sample is divided by the sum of
  the PDFs of all techniques that could have produced it.
- **Power heuristic** (exponent 2 in pbrt): `(nf*pf)^2 / ((nf*pf)^2 + (ng*pg)^2)`. It often
  reduces variance further; the book shows less noise behind a light source than with balance.
- MIS can very slightly increase variance when one technique already matches the integrand, but
  is almost always worthwhile in rendering.
- **MIS compensation:** because MIS needs only one PDF nonzero where the integrand is, other
  distributions may be sharpened (zeroed where low). pbrt passes `allowIncompletePDF = true` to
  light sampling because BSDF sampling covers all valid directions.

## 4. The MIS path integrator (as pbrt's PathIntegrator)
1. At a non-specular surface, sample a light (via a light sampler), evaluate the BSDF and cosine
   for the sampled direction, trace a shadow ray, and weight with `PowerHeuristic(1, p_l, 1, p_b)`
   where `p_l = lightChoicePmf * lightSamplePdf`. For a delta light there is no BSDF-sampling
   counterpart, so return the unweighted estimator `L * f / p_l` (no MIS).
2. Sample the BSDF for the next direction. When that ray hits an emitter (area light or infinite
   light), add `beta * Le` weighted by `PowerHeuristic(1, p_b, 1, p_l)`, where `p_l` is the
   light's choice probability times its PDF for that direction.
3. For camera rays and after a perfect specular bounce, add emission with no MIS weight, since
   light sampling was not done at the previous vertex. Skip light sampling for purely specular
   BSDFs.
4. Keep `p_b` (the BSDF PDF of the last bounce). If the BSDF sample's pdf is only proportional
   to the true value (pbrt's `pdfIsProportional`, e.g. layered BxDFs), call the BSDF's `PDF()`
   for the true value.
5. Skip a light sample if its radiance or pdf is zero, or if the BSDF value for the sampled
   direction is zero, before tracing a shadow ray.
6. Nudge the light-sampling reference point to the side of the surface the outgoing ray leaves
   from for purely reflective or purely transmissive BSDFs, to avoid bright pixels on the back
   of one-sided lights.

## 5. Russian roulette
Russian roulette skips low-contribution samples without bias: terminate with probability `q`
and divide survivors by `1 - q`. It never reduces variance, but can improve efficiency.
pbrt's choice: `rrBeta = beta * etaScale`; if `max component of rrBeta < 1` and `depth > 1`,
`q = max(0, 1 - maxComponent(rrBeta))`; if the random number is below `q` stop, otherwise
`beta /= 1 - q`.
- Base `q` on the path throughput so survivors have `beta` near 1.
- Track `etaScale` (the product of squared refraction ratios) and remove it from `beta` for the
  test, or paths through glass are killed on entry and noise rises.
- Use the maximum component, not the average, so saturated reflectances do not push a component
  above 1.

## 6. Splitting and regularization
- **Splitting** takes several samples of an inner integral per outer sample, amortising the cost
  of the first ray.
- **Path regularization** blurs difficult-to-sample paths (for example a bright small sun seen via
  a specular bounce after a diffuse one). pbrt roughens BSDFs only after the first non-specular
  bounce (`anyNonSpecularBounces`), so camera and pure specular paths keep the scene as authored.
  For the microfacet distribution, when alpha is below 0.3 it doubles it and clamps to 0.1..0.3.
  This adds bias; say so when using it.

## Gotchas
- Each contribution must be divided by the exact PDF of how it was generated, in the same measure.
- Do not count emission twice: if you light-sample, BSDF-sampled emitter hits need MIS weights.
- A zero pdf from a light sample means skip it; do not divide.

## Verify
- [ ] Compare against a brute-force BSDF-only reference at very high sample counts: means agree.
- [ ] MIS beats either strategy alone across a roughness by light-size grid (compare MSE).
- [ ] With Russian roulette on, mean image unchanged within noise; noise near glass not increased.

## Checked
Checked 2026-11-08 against pbrt-v4 sections 2.2 (Improving Efficiency) and 13.4 (A Better Path
Tracer), and the Veach dissertation landing page (abstract only). Removed because those pages
do not state them: the PBR4 ch. 2 cross-references, GGX VNDF and cosine sampling advice, the
area-to-solid-angle conversion formula, the `max(0.05, ...)` roulette constant, Sobol/Owen
low-discrepancy advice, furnace tests, and the Veach chapter details.
Method: docs-only read of cited pages, 2026-11-08
