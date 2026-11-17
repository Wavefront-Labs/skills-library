---
id: engineering-technology.electrical-engineering.power-electronics.converter-emi
name: converter-emi
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [cispr-32, common-mode-choke, conducted-emi, converter-emi, electrical-engineering, hot-loop, input-filter-design, lisn, power-electronics, power-stage-layout]
level: advanced
status: draft
description: "Design converter EMI filters and layout: differential-mode and common-mode filter sizing, LISN measurement and hot-loop minimisation."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Converter EMI filtering

1. **Limits:** conducted emissions limits depend on the product standard (for example CISPR 32 for multimedia, CISPR 11 for industrial/scientific); measured using a LISN (50 ohm / 50 uH network) in a 150 kHz to 30 MHz sweep with quasi-peak and average detectors.
2. **Separate modes:** differential-mode (current in the loop between lines) and common-mode (noise returning through ground capacitance); use a mode separator or measure with a current probe.
3. **DM filter:** attenuation required at the switching frequency (and harmonic) `A_dB`; for a second-order LC `f_c = f_sw 10^(-A/40)`; damp resonance with R-C branch (damping resistor in series with a larger capacitor) to avoid peaking and negative-impedance interaction with the converter (Middlebrook criterion: filter output impedance well below converter input impedance).
4. **CM filter:** common-mode choke with Y capacitors; the Y capacitor value is limited by leakage current safety limits; choke saturates with imbalance.
5. **Layout:** minimise the hot loop (input capacitor, high-side and low-side switch) area, place decoupling directly across the switch, keep the switch-node copper small, use solid return plane, shield or spread-spectrum clock if allowed.
6. **Snubbers and gate resistors** for ringing damping.

**Verify:** pre-compliance LISN scan with a margin of at least 6 dB below the limit.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
