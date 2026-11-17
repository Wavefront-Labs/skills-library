---
id: natural-sciences.ecology.community-ecology.diversity-indices-and-rarefaction
name: diversity-indices-and-rarefaction
category: natural-sciences
field: ecology
product: community-ecology
tags: [community-ecology, biodiversity, species-diversity, species-richness, alpha-diversity, beta-diversity, shannon-index, simpson-index, inverse-simpson, hill-numbers, effective-number-of-species, rarefaction, extrapolation, sample-coverage, chao1, ace, species-accumulation-curve, inext, vegan, r, evenness, pielou, abundance-data, incidence-data, sampling-effort, community-composition]
level: practitioner
status: gated
description: "Compare species diversity between sites fairly: richness, Shannon and Simpson as Hill numbers, rarefaction and extrapolation by sample coverage, with iNEXT and vegan."
sources: ["A. Chao et al., Rarefaction and extrapolation with Hill numbers, Ecol. Monogr. 84 (2014) 45", "L. Jost, Entropy and diversity, Oikos 113 (2006) 363", "T. C. Hsieh, K. H. Ma & A. Chao, iNEXT, Methods Ecol. Evol. 7 (2016) 1451", "vegan R package documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diversity indices and rarefaction

**Goal:** say "site A is more diverse than site B" in a way that isn't an artefact of
having sampled A more, and report diversity in units people can interpret.

## 1. Use Hill numbers (effective number of species)
Raw Shannon H′ and Simpson's index are not on the same scale as richness and don't
behave linearly (doubling the number of equally common species doesn't double H′).
Convert to **Hill numbers** ^qD:
- **q = 0:** species richness (rare species count as much as common ones).
- **q = 1:** exp(H′) — "effective number of common species".
- **q = 2:** 1/Σpᵢ² (inverse Simpson) — "effective number of dominant species".
Plot all three (a diversity profile): if site rankings change with q, the sites
differ in evenness, not just richness.

## 2. Effort is the main confounder
Observed richness rises with the number of individuals or samples. Comparing raw
richness of 300 trapped beetles at A vs 1,200 at B is meaningless.
- **Rarefaction:** interpolate each site down to a common sample size (individuals for
  abundance data; sampling units for incidence data).
- **Extrapolation:** iNEXT extends curves to ~2× the observed sample size reliably,
  not further.
- **Coverage-based comparison (preferred):** compare at equal **sample completeness**
  (coverage, e.g. 95%) rather than equal n — fairer when communities differ in
  total abundance. Good–Turing coverage estimate: Ĉ ≈ 1 − f₁/n (f₁ = singletons).

## 3. In R
(R is not installed in the review environment, so the calls below are unrun (gated: unconfirmed, source is paywalled or blocked); the formulas in sections 1 and 4 were computed in Python: for counts 50/30/10/5/3/1/1, q0 = 7, q1 = 3.62, q2 = 2.83, f1 = 2, f2 = 0 (bias-corrected Chao1 7.99), Good-Turing coverage 1 - f1/n = 0.98, and Shannon H' of 8 equal species is 2.08 vs 2.77 for 16, so doubling species adds ln 2 only).
```r
library(iNEXT); library(vegan)
# abundance: named list of species-count vectors, one per site
out <- iNEXT(list(A = countsA, B = countsB), q = c(0, 1, 2), datatype = "abundance")
ggiNEXT(out, type = 1, facet.var = "Order.q")   # size-based curves with 95% CIs
ggiNEXT(out, type = 3)                          # coverage-based curves
estimateD(list(A = countsA, B = countsB), datatype = "abundance", base = "coverage", level = 0.95)
# classic indices & estimators
diversity(comm_matrix, "shannon"); specpool(comm_matrix)   # Chao, jackknife, bootstrap richness
```
For incidence data (presence/absence per plot, camera, trap) use `datatype =
"incidence_freq"` with the number of sampling units first in each vector.

## 4. Asymptotic richness
**Chao1** = S_obs + f₁²/(2f₂) (bias-corrected form when f₂ = 0) gives a *lower bound*
on true richness. Large gaps between S_obs and Chao1 = many singletons = undersampled.
Report the estimate with its CI, and don't treat it as the true total.

## Gotchas
- Pooling samples with different methods (pitfall + light trap) mixes detectabilities.
- Evenness indices (Pielou's J) are mathematically tied to richness; prefer comparing
  Hill-number ratios.
- Beta diversity: use multiplicative partitioning with Hill numbers (γ = α × β) or
  dissimilarity indices (Bray–Curtis, Sørensen) — different questions.
- Unidentified morphospecies counted inconsistently across sites inflate differences.
- *Uncertainty note:* function arguments reflect iNEXT 3.x and vegan 2.6 (gated: unconfirmed, source is paywalled or blocked); check the package docs for your installed versions.

## Verify
- [ ] Diversity reported as Hill numbers (q = 0, 1, 2) with CIs.
- [ ] Comparisons made at equal coverage (or equal sample size), not raw counts.
- [ ] Extrapolation stays within ~2× the observed sample.
- [ ] Sample coverage per site reported; low-coverage sites flagged.
- [ ] Data type (abundance vs incidence) matches the sampling design.
