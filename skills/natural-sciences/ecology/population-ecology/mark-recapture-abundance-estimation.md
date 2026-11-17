---
id: natural-sciences.ecology.population-ecology.mark-recapture-abundance-estimation
name: mark-recapture-abundance-estimation
category: natural-sciences
field: ecology
product: population-ecology
tags: [population-ecology, mark-recapture, capture-recapture, capture-mark-recapture, cmr, lincoln-petersen, chapman-estimator, schnabel, closed-population, open-population, cormack-jolly-seber, jolly-seber, robust-design, program-mark, rmark, marked, secr, spatial-capture-recapture, abundance-estimation, population-size, detection-probability, trap-happy, trap-shy, tag-loss, pit-tags, photo-identification, survival-estimation]
level: practitioner
status: verified
description: "Estimate animal abundance by mark-recapture: Lincoln-Petersen with Chapman correction, closed vs open models, assumptions, marking, sample-size planning and software."
sources: ["D. L. Otis, K. P. Burnham, G. C. White and D. R. Anderson, Statistical inference from capture data on closed animal populations, Wildlife Monographs 62 (1978)", "G. C. White and K. P. Burnham, Program MARK, Bird Study 46 (1999) S120", "E. Cooch and G. White, Program MARK: A Gentle Introduction (online book)", "D. G. Chapman (1951) Univ. Calif. Publ. Stat. 1:131"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mark-recapture abundance estimation

**Goal:** an estimate of population size N (with a confidence interval) for animals
you can't count completely, using the proportion of marked animals in later samples.

## 1. The simplest case: two samples, closed population
Catch and mark n₁ animals, release, later catch n₂ of which m₂ are marked.
- Lincoln–Petersen: N̂ = n₁n₂/m₂ (biased high when m₂ is small).
- **Chapman** (use this): N̂ = (n₁+1)(n₂+1)/(m₂+1) − 1, approximately unbiased when
  n₁ + n₂ ≥ N; variance
  var = (n₁+1)(n₂+1)(n₁−m₂)(n₂−m₂) / ((m₂+1)²(m₂+2)).
- Plan for **many recaptures**: the relative standard error is roughly 1/√m₂ (simulated: n₁=120, n₂=100, N=500 gives m₂≈24 and SE≈16 %), so m₂ of 7–10 gives 30–40 % and a very wide CI. Rough planning: expected m₂ ≈ n₁n₂/N — guess N, then size the samples.

Worked example: n₁ = 120, n₂ = 100, m₂ = 24 → Chapman N̂ = 121·101/25 − 1 ≈ 488.

## 2. The assumptions (and what breaks them)
1. **Closure:** no births, deaths, immigration, emigration between samples → keep the
   interval short relative to the species' life history and movement.
2. **Equal catchability:** every animal has the same capture probability → violated by
   trap-happy/trap-shy behaviour, sex/age/size differences, home ranges at the edge of
   the trapping grid. Heterogeneity biases N̂ **low**.
3. **Marks not lost, not missed, and not affecting survival/behaviour** → double-mark a
   subsample to estimate tag loss; use marks appropriate to the taxon (PIT tags,
   bands, fin clips, toe clips where ethically approved, photo-ID natural markings).
4. Marked animals **mix** with unmarked ones before resampling.

## 3. Beyond two samples
- **Multiple occasions, closed (Otis models):** M₀ (constant p), Mt (time varying),
  Mb (behaviour/trap response), Mh (individual heterogeneity) and combinations. Fit in
  Program MARK / RMark or the `Rcapture` package; compare with AICc.
- **Open populations:** Cormack–Jolly–Seber estimates survival (φ) and recapture (p),
  not N; Jolly–Seber / POPAN adds entries and abundance.
- **Robust design:** closed secondary sessions nested in open primary periods — N each
  period plus survival and temporary emigration.
- **Spatial capture–recapture (secr, oSCR):** uses where animals were caught to model
  detection with distance and estimate *density* directly; solves the "effective
  area trapped" problem of non-spatial models.

## 4. Field protocol essentials
- Standardise effort (traps, nights, search time) across occasions; record it.
- Record individual ID, occasion, location, sex/age, condition, and any mark damage.
- Animal welfare and permits: handling, marking methods and trap checks are usually
  governed by an ethics approval and wildlife permits — follow them.
- Build the capture history matrix (individual × occasion, 1/0) as you go.

## Gotchas
- Population "estimates" from capture histories that are mostly singletons (caught once)
  are unreliable regardless of model.
- Non-spatial N̂ divided by grid area overestimates density (animals living partly outside).
- Simulation check (N=500): Chapman averaged 500.6 at n₁=120, n₂=100; with n₁=n₂=30 (n₁+n₂<N) Lincoln–Petersen averaged 553 while Chapman averaged 436, so the n₁+n₂ ≥ N condition matters. Run a simulation for important designs.

## Verify
- [ ] Interval between occasions justified for closure (or an open model used).
- [ ] Expected recaptures ≥ ~10 from planning; actual m₂ reported.
- [ ] Heterogeneity and behavioural response tested (Mh, Mb) where ≥ 3 occasions.
- [ ] Tag loss estimated or argued negligible.
- [ ] N̂ reported with CI, model, and software version.
