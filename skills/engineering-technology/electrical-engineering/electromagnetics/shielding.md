---
id: engineering-technology.electrical-engineering.electromagnetics.shielding
name: shielding
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [aperture-leakage, cable-shield-termination, electrical-engineering, electromagnetics, faraday-shield, magnetic-shielding, shield-pigtail, shielding, shielding-effectiveness]
level: advanced
status: draft
description: "Select shielding approaches: shielding effectiveness, aperture leakage and cable shield termination."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Electromagnetic shielding

1. **Shielding effectiveness:** `SE = R + A + B` (reflection, absorption, multiple-reflection correction, in dB). Absorption `A = 8.69 t/delta` dB with `delta = 1/sqrt(pi f mu sigma)` skin depth. Copper at 1 MHz: delta about 0.066 mm, so a 0.5 mm wall gives about 66 dB absorption (reflection adds more).
2. **Low-frequency magnetic fields:** reflection is small; use high-permeability materials (mu-metal) or a conductive loop (shorted turn) for cancellation; absorption is minimal at 50/60 Hz in copper (skin depth about 9 mm at 50 Hz).
3. **Apertures:** leakage is set by the largest dimension; a slot length `l` gives roughly `SE = 20 log(lambda/(2 l))` dB, so a 10 cm slot yields about 0 dB near 1.5 GHz. Use many small holes, waveguide-below-cutoff vents, honeycomb panels.
4. **Gaskets / seams:** conductive gaskets with adequate compression and corrosion-compatible finishes.
5. **Cable shields:** terminate at 360 degrees at the connector; pigtails add inductance and ruin high-frequency shielding. Ground at both ends for high-frequency noise and at one end for low-frequency hum-sensitive circuits (with capacitive grounding at the other).
6. **Test:** measure transfer impedance of cables and enclosure SE using IEEE 299 or equivalent method.

**Verify:** compare the measured SE with the target in the frequency band that matters.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
