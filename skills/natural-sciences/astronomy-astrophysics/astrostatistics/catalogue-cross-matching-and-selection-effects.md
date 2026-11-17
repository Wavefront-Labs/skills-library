---
id: natural-sciences.astronomy-astrophysics.astrostatistics.catalogue-cross-matching-and-selection-effects
name: catalogue-cross-matching-and-selection-effects
category: natural-sciences
field: astronomy-astrophysics
product: astrostatistics
tags: [astrostatistics, cross-matching, catalogue-matching, positional-uncertainty, match-radius, false-match-rate, likelihood-ratio, nway, topcat, stilts, astropy-match-coordinates, proper-motion, epoch-propagation, gaia, selection-effects, malmquist-bias, eddington-bias, completeness, upper-limits, censored-data, survival-analysis, kaplan-meier, survey-analysis]
level: advanced
status: verified
description: "Cross-match astronomical catalogues with a quantified false-match rate, propagate proper motions, and handle completeness, Malmquist/Eddington bias and upper limits correctly."
sources: ["Feigelson & Babu, Modern Statistical Methods for Astronomy (CUP)", "Salvato et al. 2018, NWAY (MNRAS)", "TOPCAT/STILTS documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catalogue cross-matching and selection effects

**Goal:** joined catalogues where you know how many matches are wrong, and samples whose
selection you can describe — so trends you find are in the sky, not in the survey.

## 1. Cross-matching basics
```python
from astropy.coordinates import SkyCoord
import astropy.units as u
c1 = SkyCoord(ra1*u.deg, dec1*u.deg); c2 = SkyCoord(ra2*u.deg, dec2*u.deg)
idx, sep, _ = c1.match_to_catalog_sky(c2)
good = sep < 1.0*u.arcsec
```
`match_to_catalog_sky` returns the **nearest** neighbour by default (`nthneighbor=1`), always — even if it's 5° away.
You must apply a radius, and nearest ≠ correct.

TOPCAT (GUI) / STILTS (scripted) do the same with "best/all/symmetric" options; use
**best match, symmetric** to avoid one source matching many.

## 2. Choose the radius from the data
- Combine positional errors: σ = √(σ1² + σ2² + systematic²). For Gaussian errors, a
  radius of ~3σ captures ~99% of true counterparts.
- Plot the **separation histogram**: true matches pile up at small separations; random
  matches grow ∝ separation. Pick the radius where the true peak has decayed.
- **False-match rate:** shift one catalogue by e.g. 1′ in declination (several offsets)
  and re-match; the number of "matches" estimates chance coincidences. Report it.
- For large error circles (X-ray, radio, far-IR) where several candidates fall in the
  circle, use a **likelihood-ratio / Bayesian** method (NWAY, LR with magnitude priors)
  rather than nearest neighbour.

## 3. Epochs and proper motion
Gaia DR3 positions are at epoch J2016.0 (DR2: J2015.5); older catalogues at J2000 or their observation epoch.
High-proper-motion stars (≳ 100 mas/yr) move arcseconds over decades. Propagate with
`SkyCoord.apply_space_motion` or ADQL `EPOCH_PROP` in the Gaia archive before matching.

## 4. Selection effects to name explicitly
- **Flux limit / Malmquist bias:** a magnitude-limited sample over-represents intrinsically
  luminous objects at large distance. Trends of luminosity with distance are often this.
- **Eddington bias:** near the detection limit, noise scatters more faint objects up than
  bright ones down — measured fluxes and number counts are biased high.
- **Completeness:** measure it by **injecting artificial sources** into the images and
  recovering them, as a function of magnitude, size and crowding. Correct counts by 1/completeness only where completeness is reasonably high (e.g. >50%; *convention varies*).
- **Footprint and masks:** stars, bright-star halos, bad-data regions — any spatial
  statistic needs the mask (random catalogues in the same footprint).

## 5. Upper limits (censored data)
Non-detections carry information. Don't drop them, and don't set them to the limit value.
- Use **survival analysis**: Kaplan–Meier estimator for distributions, censored
  correlation tests and regression (e.g. Buckley–James, Schmitt's binning; Python:
  `lifelines` `KaplanMeierFitter.fit_left_censoring` (checked on lifelines 0.30.3); R: `NADA`).
- Or forward-model: include the detection probability in the likelihood of a Bayesian fit.

## 6. Bayesian fitting hygiene
Fit with errors in both variables and intrinsic scatter (e.g. `linmix`, hierarchical
models in Stan/PyMC). Ordinary least squares on log-log data with heteroscedastic errors
and a flux limit is the classic way to get a wrong slope.

## Gotchas
- Mixing positions from different reference frames (FK5 vs ICRS — small, but matters at
  sub-arcsec).
- Matching by name strings instead of positions.
- A 2″ radius in a crowded Galactic-plane field has a very different false-match rate
  than at high latitude — compute it per region.

## Verify
- [ ] Match radius justified by error budget and separation histogram.
- [ ] False-match rate estimated by offset matching and reported.
- [ ] Positions propagated to a common epoch where proper motions matter.
- [ ] Completeness measured by injection-recovery, not assumed.
- [ ] Upper limits included via survival analysis or the likelihood.
