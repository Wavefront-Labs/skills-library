---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.flat-ride-pitch-heave-tuning
name: flat-ride-pitch-heave-tuning
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [flat-ride, pitch-heave, ride-frequency-split, olley, pitch, heave, ride-balance]
level: practitioner
status: gated
description: "Tune pitch and heave to a flat ride using front-rear frequency split, pitch/bounce centre and damping, and verify with pitch rate over bumps."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Flat-ride pitch and heave tuning

1. Concept: if the rear frequency is slightly higher than the front, the rear catches up after a bump so pitch dies out quickly (flat ride; Maurice Olley's principle).
2. Targets: rear ride frequency typically about 10-20% above front for flat ride (gated: unconfirmed, source is paywalled or blocked), within limits set by comfort, ride height and trim; verify with benchmarking.
3. Compute frequencies from wheel rates and sprung corner masses; account for the tyre in series, and for load-dependent masses (passengers, luggage).
4. Pitch/bounce decoupling: the dynamic index `k^2/(a*b)` (radius of gyration squared over product of CG-to-axle distances) near 1 decouples front and rear motions.
5. Damping: front and rear ratios similar; excess rear compression damping hurts cross-axle harshness.
6. Test: drive over a single bump at 40-60 km/h, record pitch rate and body accelerations; fewer cycles of pitch means flatter ride.

**Gotchas:** passenger-load changes can reverse the frequency split; check laden and unladen.

## Verify
- [ ] Measured body pitch decays within about one cycle after a bump at the test speed.
- [ ] Laden and unladen frequency splits recorded.
