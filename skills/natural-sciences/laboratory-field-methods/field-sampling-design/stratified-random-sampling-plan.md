---
id: natural-sciences.laboratory-field-methods.field-sampling-design.stratified-random-sampling-plan
name: stratified-random-sampling-plan
category: natural-sciences
field: laboratory-field-methods
product: field-sampling-design
tags: [field-sampling-design, sampling-design, field-campaign, stratified-random-sampling, simple-random-sampling, systematic-sampling, grid-sampling, transects, quadrats, strata, gis, qgis, random-points, site-selection, sampling-bias, accessibility-bias, spatial-autocorrelation, sample-size, neyman-allocation, field-blanks, duplicates, chain-of-custody, gps, environmental-sampling, ecological-survey]
level: practitioner
status: verified
description: "Plan a field sampling campaign: define population and strata, generate random sites in GIS, allocate samples across strata, handle inaccessible sites and spatial autocorrelation, add QA samples."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A stratified random sampling plan

**Goal:** field samples that represent the area or population you will make claims
about, with known selection probabilities and no hidden bias toward easy-to-reach
places — designed on paper and in GIS before anyone goes out.

## 1. Define what you are sampling
- **Target population:** the full set you want to generalise to (all wetlands in the
  catchment, the whole field, all trees > 10 cm DBH in the reserve).
- **Sampling unit:** a 1 m² quadrat, a 100 m transect, a soil core, a water grab.
- **Sampling frame:** the map or list from which units are drawn. Anything outside the
  frame cannot be represented, so draw the frame to match the population.

## 2. Choose the scheme
| Scheme | Use when | Watch for |
|---|---|---|
| Simple random | Homogeneous area, no prior info | Clusters by chance; can miss small habitats |
| **Stratified random** | Known heterogeneity (habitat, soil type, depth, land use) | Strata must be defined before sampling, from independent data |
| Systematic (grid/transect) | Mapping gradients, even coverage | Aligning with periodic features (crop rows, ridges) biases results; use a random start |
| Adaptive / cluster | Rare, clumped targets | Needs special estimators |

Stratification improves precision when strata differ from each other but are
internally similar, and guarantees coverage of small strata.

## 3. Generate sites
In QGIS: **Vector › Research Tools › Random points inside polygons** (QGIS docs name; it has a per-polygon "Minimum distance between points" and an advanced global minimum distance) (per stratum, with a
minimum distance between points), or `sf::st_sample()` in R. Generate **extra backup
points** per stratum (e.g. 50 % more) in a random order list.
Rule: if a site is inaccessible or unsuitable, move to the **next backup in the list**
— never to the nearest convenient spot. Record every rejected site and the reason;
a high rejection rate in one stratum is itself a bias you must report.

## 4. Allocate samples to strata
- **Proportional:** n per stratum ∝ stratum area/size. Simple and self-weighting.
- **Neyman (optimal):** n_h ∝ N_h × S_h — more samples where strata are large and variable.
  Needs prior estimates of within-stratum SD (pilot or literature).
- Minimum of ~2 per stratum to estimate variance; in practice aim higher.
For estimating a mean within a margin E at 95 % confidence, n ≈ (1.96 × SD ÷ E)² in a
simple random design; stratification usually reduces this.
Worked check (computed): three strata with W = 0.7/0.2/0.1, SD = 2/10/30 and n = 100 give var(mean) 1.13 under proportional and 0.41 under Neyman allocation (n_h = 21.9/31.3/46.9). With stratum means 10/30/60 the true mean is 19.0 but the unweighted mean of an equal-allocation sample estimates 33.3. For E = 2 and SD = 10, n = (1.96 × 10 ÷ 2)² = 96.
Analyse with stratum weights: the overall mean is Σ (W_h × mean_h), where W_h is the
stratum's share of the population. An unweighted mean of a disproportionate design is biased.

## 5. Spatial and temporal structure
- Nearby samples are often correlated (**spatial autocorrelation**); they carry less
  independent information than their count suggests. Set a minimum distance between
  points informed by a pilot variogram or the process scale.
- Time matters: tides, diurnal cycles, season, flow events. Fix sampling windows or
  randomise time as a factor, and record it.

## 6. QA samples and records
- **Field duplicates** (~5–10 % of samples) to quantify small-scale variability and handling error.
- **Field/trip blanks** for contaminant work (water carried to the field and back).
- GPS each site with stated accuracy; photograph; standard field sheet or app form.
- **Chain of custody** forms where results may have regulatory or legal use.
- Label samples with pre-printed IDs; never handwrite IDs in the rain.

## Gotchas
- Road- and trail-side sampling is the classic accessibility bias: edges differ from interiors.
- Strata drawn after seeing data are not strata — they are post-hoc subgroups.
- Permits and landowner permission take weeks; include them in the plan.
- Field safety: lone-working plan, check-in times, tide and weather limits.

Uncertain here: the sample-size formula is the basic
normal approximation and is not adequate for highly skewed data (e.g. counts with many zeros).

## Verify
- [ ] Population, sampling unit and frame written down and mapped.
- [ ] Strata defined from independent data before sampling.
- [ ] Sites randomly generated with an ordered backup list; rejections logged.
- [ ] Allocation and weights documented so stratified estimates can be computed.
- [ ] Duplicates/blanks scheduled; GPS, photos and labels standardised.
