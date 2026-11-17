---
id: natural-sciences.astronomy-astrophysics.time-domain-astronomy.light-curve-period-finding-and-transit-detection
name: light-curve-period-finding-and-transit-detection
category: natural-sciences
field: astronomy-astrophysics
product: time-domain-astronomy
tags: [time-domain-astronomy, light-curve, period-finding, lomb-scargle, periodogram, bls, box-least-squares, transit-detection, exoplanets, tess, kepler, lightkurve, detrending, aliasing, false-alarm-probability, phase-folding, variable-stars, eclipsing-binaries, barycentric-correction, bjd, ztf, alerts, transients]
level: practitioner
status: verified
description: "Find periods and transits in light curves: detrending, Lomb-Scargle and BLS periodograms, aliases and false-alarm levels, phase folding, BJD timing and false-positive checks."
sources: ["VanderPlas 2018, Understanding the Lomb-Scargle Periodogram (ApJS)", "Kovács, Zucker & Mazeh 2002, BLS algorithm", "Lightkurve documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Light-curve period finding and transit detection

**Goal:** decide whether a light curve contains a real periodic signal, measure its
period honestly, and — for transits — rule out the common impostors.

## 1. Prepare the light curve
- Use **barycentric time** (BJD_TDB) for anything you'll compare across observatories or
  years; TESS/Kepler products already provide it, ground data usually doesn't.
- Remove flagged cadences (quality flags), obvious outliers (sigma-clip *upwards* only if
  hunting transits — don't clip the dips you want).
- **Detrend** instrumental and stellar trends. Window length must be much longer than the
  transit duration (e.g. ≥3× duration) or you will eat the transit.
```python
import lightkurve as lk
lc = lk.search_lightcurve("TIC 0000000", mission="TESS").download().remove_nans()  # placeholder target
flat = lc.flatten(window_length=901)   # odd number of cadences: 901 x 2 min = 30 hr; for a ~3 hr window use 91 (default is 101)
```

## 2. Periodic variability: Lomb-Scargle
```python
from astropy.timeseries import LombScargle
ls = LombScargle(t, y, dy)
freq, power = ls.autopower(minimum_frequency=1/30, maximum_frequency=20, samples_per_peak=10)
fap = ls.false_alarm_probability(power.max())
```
- **Frequency grid:** spacing fine enough — `samples_per_peak` 5–10 over a baseline T
  gives step ≈ 1/(n·T).
- **Aliases:** ground data sampled nightly produce peaks at f ± 1 cycle/day; satellite
  data have orbit-related aliases. Check the spectral window (periodogram of the sampling).
- **Harmonics:** eclipsing binaries often peak at half the true period — fold at 2P and see
  whether alternate eclipses differ.
- **False-alarm probability** assumes white noise; red noise (stellar granulation,
  spots) makes it optimistic. Bootstrap or inject-recover for a realistic threshold.

## 3. Transits: Box Least Squares
```python
from astropy.timeseries import BoxLeastSquares
bls = BoxLeastSquares(t, flat_flux, dy)
res = bls.autopower([0.04, 0.08, 0.16])   # trial durations in days
```
Inspect the top peaks, not just the highest. `astropy` BLS returns `depth_snr` (no SDE; compute it yourself from the power spectrum). Measure SDE or
S/N; a common heuristic threshold for TESS is S/N ≳ 7 (*pipeline-specific*). Then fit a
physical transit model (batman, exoplanet, juliet) for depth, duration, impact parameter.

## 4. False-positive checklist for a transit
1. **Odd/even depths** differ → eclipsing binary at 2P.
2. **Secondary eclipse** at phase 0.5 → probably a binary (or a hot planet — check depth).
3. **V-shaped** rather than flat-bottomed → grazing binary likely.
4. **Centroid shift** during transit → the signal is on a nearby star (blend). TESS pixels
   are ~21″, so contamination is common; check the pixel-level data and Gaia neighbours.
5. Duration consistent with the host star's density (from Gaia/TIC parameters).
6. Signal present in independent data (different sector, ground photometry).

## 5. Report
Period with uncertainty (from model fit or periodogram peak width ~1/T, refined by
fitting), epoch T0 in BJD_TDB, depth, duration, S/N, and which checks were passed.

## Gotchas
- Detrending with a window shorter than the signal.
- Calling a 1-day or 13.7-day (TESS orbit) period astrophysical without checking systematics.
- Mixing HJD, BJD_UTC and BJD_TDB (can differ by ~1 min — enough to break transit timing).
- *Uncertainty note:* thresholds above are rules of thumb; survey pipelines use their own vetting.

## Verify
- [ ] Times are in BJD_TDB and quality-flagged points removed.
- [ ] Detrending window ≫ signal duration (injection test recovers a fake signal).
- [ ] Aliases and harmonics checked; spectral window inspected.
- [ ] Transit candidates pass odd/even, secondary, shape and centroid tests.
- [ ] Period and epoch reported with uncertainties.
