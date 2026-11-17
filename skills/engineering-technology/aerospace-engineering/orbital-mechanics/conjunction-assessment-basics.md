---
id: engineering-technology.aerospace-engineering.orbital-mechanics.conjunction-assessment-basics
name: conjunction-assessment-basics
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [conjunction-assessment, collision-probability, miss-distance, conjunction-data-message, space-safety, orbit-determination]
level: practitioner
status: gated
description: "Assess satellite conjunctions: screening, time of closest approach, covariance-based collision probability, thresholds and manoeuvre decision workflow."
sources:
  - "Chan, Spacecraft Collision Probability"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "CCSDS Conjunction Data Message standard (site root: public.ccsds.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Conjunction assessment

**Goal:** decide whether a predicted close approach needs action.

## Workflow
1. **Screening**: compare predicted trajectories of your satellite against the catalogue with a distance threshold volume; flag objects approaching within the volume.
2. **Refine**: compute time of closest approach (TCA), miss distance, relative velocity (often several km/s in LEO (gated: unconfirmed, source is paywalled or blocked)) and the position covariances of both objects at TCA.
3. **Probability of collision (Pc)**: project the combined covariance into the encounter plane (perpendicular to the relative velocity) and integrate the 2D Gaussian density over the circle of combined hard-body radius; the short encounter justifies the linear relative-motion and constant-covariance assumptions.
4. **Decide**: compare Pc with the operator's threshold. NASA CARA states Pc above 1e-7 merits operational attention and above 1e-4 requires mitigation (nasa.gov/cara); other operators set their own thresholds.
5. **Manoeuvre**: find the burn that reduces Pc below a target with minimum fuel and no new conjunctions.

## Data
Conjunction Data Messages (a CCSDS standard format) carry TCA, miss distance, covariances; catalogue sources include national space surveillance services and commercial providers.

## Gotchas
- Covariance realism matters: unrealistic covariances give misleading Pc; large covariance can lower Pc (dilution), so also look at miss distance and the covariance scale.
- Objects without good covariance data (debris) need assumptions.
- Atmospheric drag uncertainty dominates LEO propagation error over days.

## Verify
- [ ] Pc computed by your method matches a published test case (Monte Carlo or analytic) within tolerance.
