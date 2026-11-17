---
id: engineering-technology.automotive-vehicle-engineering.nvh.intake-and-exhaust-noise
name: intake-and-exhaust-noise
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [intake-exhaust-noise, helmholtz-resonator, quarter-wave, muffler, transmission-loss, drone, tailpipe-noise]
level: practitioner
status: gated
description: "Tune intake and exhaust noise: Helmholtz and quarter-wave resonators, muffler transmission loss, drone control and regulatory pass-by considerations."
sources:
  - "Munjal, Acoustics of Ducts and Mufflers"
  - "ISO 362 pass-by noise overview; UN R51 limits (confirm current)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Intake and exhaust noise

1. Sources: intake pulsations at firing order, exhaust pressure pulsations; radiated from the intake mouth and tailpipe plus shell noise from the muffler.
2. **Helmholtz resonator:** `f = (c/(2*pi))*sqrt(A/(V*L_eff))` with neck area A, effective neck length `L_eff` (add end corrections), cavity volume V, c speed of sound (about 343 m/s at 20 C); tune to the offending frequency (e.g. 120 Hz drone).
3. **Quarter-wave tube:** `f = c/(4*L)` for a closed side branch; attenuates at that frequency and odd multiples.
4. Mufflers: reactive (expansion chambers, perforated) vs dissipative (absorbent); evaluate by transmission loss (dB) and insertion loss in 1-D acoustic codes or with FE/BEM; keep back-pressure low for power.
5. Drone: low frequency (typically 1.5-3 order near cruise rpm (gated: unconfirmed, source is paywalled or blocked)) boom; address with resonators, tailpipe length and diameter, and valves.
6. Regulatory pass-by noise (ISO 362 method; UN R51 and EU limits; not fetched (gated: unconfirmed, source is paywalled or blocked)); confirm current limit values and test method.
7. Active sound control and exhaust valves allow sound design for modes.

**Gotchas:** temperature dependence of c in exhaust (hot gas) shifts tuning.

## Verify
- [ ] Measured transmission loss at the target frequency within a few dB of design.
- [ ] Pass-by test and cabin drone level at cruise within target.
