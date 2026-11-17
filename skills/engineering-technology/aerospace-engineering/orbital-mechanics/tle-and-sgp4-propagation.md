---
id: engineering-technology.aerospace-engineering.orbital-mechanics.tle-and-sgp4-propagation
name: tle-and-sgp4-propagation
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, orbit-determination, space-situational, sgp4, tle, two-line-element, teme, propagation-accuracy]
level: practitioner
status: gated
description: "Read two-line element sets, propagate with SGP4, convert TEME to ECEF, and know the accuracy limits and epoch handling."
sources:
  - "Hoots and Roehrich, Spacetrack Report No. 3"
  - "Vallado, Crawford, Hujsak and Kelso, Revisiting Spacetrack Report No. 3 (AIAA 2006)"
  - "CelesTrak documentation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# TLE and SGP4 propagation

**Goal:** position and velocity from public two-line elements.

## TLE format basics
- Line 1: catalogue number, classification, international designator, epoch (year and day of year), mean motion first derivative, `B*` drag term, element set number.
- Line 2: inclination, RAAN, eccentricity (decimal point assumed), argument of perigee, mean anomaly, mean motion (revolutions per day), revolution number.
- Elements are mean elements specific to the SGP4 model; do not treat them as osculating Keplerian elements.

CelesTrak's documentation page (https://celestrak.org/NORAD/documentation/) lists Spacetrack Report No. 3, the TLE format description, and AIAA 2006-6753 "Revisiting Spacetrack Report #3" (non-proprietary SGP4 code with test cases), and stresses that mean element sets must be used with the matching model.

## Propagation
1. Parse and initialise with an SGP4 implementation (for example the `sgp4` Python package or Vallado's reference code); the deep-space branch (SDP4) is used automatically when the period exceeds 225 minutes (gated: unconfirmed, source is paywalled or blocked).
2. Propagate to a time offset from epoch; output position and velocity in the TEME frame.
3. Convert TEME to ECEF using sidereal time (and polar motion if accuracy demands) for ground track.

## Accuracy
- Roughly kilometre-level at epoch for LEO, growing with time from epoch by a km or more per day (more for low orbits at high drag and solar activity) (gated: unconfirmed, source is paywalled or blocked). Use the latest element set; do not use TLEs for conjunction decisions without covariance information from a catalogue provider.

## Gotchas
- Epoch year uses two digits; century rollover logic matters.
- Incorrect units for `B*` or unit conversions of mean motion.

## Verify
- [ ] The reference test cases in the SGP4 documentation reproduce to the published precision.
