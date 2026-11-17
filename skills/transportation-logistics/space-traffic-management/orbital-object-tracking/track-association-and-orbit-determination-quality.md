---
id: transportation-logistics.space-traffic-management.orbital-object-tracking.track-association-and-orbit-determination-quality
name: track-association-and-orbit-determination-quality
category: transportation-logistics
field: space-traffic-management
product: orbital-object-tracking
tags: [orbital-object-tracking, space-surveillance, sensor-tasking, radar, optical-telescope, track-association, uct, uncorrelated-track, orbit-determination, od, residuals, batch-least-squares, kalman-filter, covariance, breakup, fragmentation, debris, cross-tag, ssa, space-domain-awareness]
level: advanced
status: draft
description: "Tasking sensors, associating observations to catalogued objects, judging orbit-determination quality from residuals and covariance, and handling uncorrelated tracks after breakups."
sources: ["Vallado, Fundamentals of Astrodynamics and Applications, ch. 10 (orbit determination)", "NASA Conjunction Assessment Best Practices Handbook (2023)", "ESA Space Environment Report (annual)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Track association and orbit-determination quality

**Goal:** turn raw sensor observations into trustworthy orbits — every downstream
conjunction warning is only as good as the orbit determination (OD) behind it.

## 1. Task the sensors deliberately
- Rank objects by **need**: high-interest conjunction secondaries, objects with stale
  orbits (last update > 2–3 days in LEO), recently manoeuvred payloads, new launches
  and breakup fragments.
- Match sensor to regime: radar (phased-array, S-band fences) for LEO and small
  debris; optical telescopes for GEO/MEO, only at night with the object sunlit.
- Spread observations along the orbit: two short arcs from different sensors and
  geometries beat one long arc from a single site (better in-track/radial separation).
- Request **revisits within one or two revolutions** after an event; observability
  degrades fast as along-track error grows quadratically with drag uncertainty.

## 2. Associate observations to objects
1. Propagate each candidate object to the observation time; compute the residual
   (range, range-rate, angles) against the predicted state.
2. Gate with a statistical test (e.g. Mahalanobis distance against the object's
   covariance) rather than a fixed kilometre threshold.
3. If more than one object passes the gate, do **not** take the closest — hold the
   observation and wait for a second track to disambiguate. Wrong association
   ("cross-tagging") corrupts two orbits at once.
4. Observations that fit nothing become **uncorrelated tracks (UCTs)**. Group UCTs by
   plausible orbit (initial orbit determination from 3+ angles or a radar track) and
   look for a parent: a manoeuvre, a new launch, a breakup, or a lost object.

## 3. Judge the OD
Run batch least squares (or a sequential filter for operations) and check:
- **Residual RMS** near the sensor's known noise, and **no trend** across the arc.
  A bow or slope in residuals means a model problem (drag, solar pressure, an
  unmodelled manoeuvre), not noise.
- **Weighted RMS ≈ 1.** Much above 1 → noise underweighted or model wrong; much below
  → over-fitting or inflated noise.
- **Covariance realism:** compare predicted positions against later observations;
  the normalised errors should look chi-squared. Unrealistically small covariance
  makes Pc look falsely low or high (see the conjunction-assessment skill).
- **Fit span:** LEO 2–7 days is typical; longer spans hide drag changes, shorter ones
  leave the radial component poorly observed.
- **Drag solution:** a solved ballistic coefficient that jumps between fits signals
  either a geomagnetic storm (density modelling error) or attitude change.

## 4. Breakup events
- Expect hundreds of UCTs in hours. Freeze automatic association in the affected
  shell — cross-tags spike.
- Back-propagate fragment orbits to find the common time/position (the break epoch).
- Publish a notice to affected operators early, even with poor orbits; flag that the
  catalogue is incomplete for days to weeks.

## Gotchas
- A manoeuvring satellite looks like a bad OD; check operator ephemeris and planned
  burns before inflating noise.
- Geomagnetic storms (high Kp/Ap) can shift LEO predictions by kilometres within a
  day — shorten prediction spans and increase revisit priority.
- Optical angles-only data have poor range; never trust a single-pass optical orbit
  for screening.
- *Exact gating thresholds and fit spans vary by organisation; values above are
  typical practice, not a standard.*

## Verify
- [ ] Residuals show no trend and weighted RMS is ~1.
- [ ] Every association was unique within the gate, or held for confirmation.
- [ ] Predicted-vs-observed checks support the covariance size.
- [ ] UCTs are grouped and each group has a hypothesised parent.
- [ ] High-interest objects have an orbit update younger than your staleness limit.
