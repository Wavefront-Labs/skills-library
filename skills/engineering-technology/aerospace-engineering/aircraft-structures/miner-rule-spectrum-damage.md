---
id: engineering-technology.aerospace-engineering.aircraft-structures.miner-rule-spectrum-damage
name: miner-rule-spectrum-damage
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [miner-rule, cumulative-damage, spectrum-loading, rainflow-counting, fatigue, metallic-fatigue]
level: practitioner
status: draft
description: "Accumulate fatigue damage over a load spectrum with rainflow counting and Miner's rule, and understand the sequence effects and scatter it ignores."
sources:
  - "Niu, Airframe Structural Design"
  - "Schijve, Fatigue of Structures and Materials"
  - "ASTM E1049 (rainflow counting practice)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Miner rule spectrum damage

**Goal:** damage per flight or per block from a stress history.

## Procedure
1. Build the stress history for one flight (ground-air-ground cycle, gust, manoeuvre, taxi).
2. Count cycles with rainflow counting (ASTM E1049 defines the practice) to obtain pairs of range and mean.
3. For each bin `i`, find the cycles to failure `N_i` from the S-N curve after mean-stress correction (see s-n-curves-and-mean-stress).
4. Linear damage `D = sum(n_i / N_i)`; failure is predicted at `D = 1` nominally. Flights to failure `= 1 / D_per_flight`.
5. Apply the scatter factor your approach requires to get the safe life; the factor depends on the programme and authority.

## Known limits
- Miner ignores load sequence. High-then-low sequences often fail earlier than `D = 1` would suggest in some materials, and the opposite in others; retardation after overloads in crack growth is a separate effect.
- Real `D` at failure varies from about 0.3 to 3 in test series; do not treat 1.0 as exact.
- Small cycles below the constant-amplitude endurance limit still damage once large cycles exist; use a modified curve (Haibach or similar) rather than dropping them.
- Spectrum testing remains the most reliable check.

## Gotchas
- Truncating the spectrum (removing small cycles) must be justified.
- Do not rainflow count across non-closed residuals incorrectly: close the history by re-ordering to start at the maximum.

## Verify
- [ ] Constant-amplitude history reproduces the S-N life with `D = n/N`.
