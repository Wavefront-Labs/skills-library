---
id: engineering-technology.electrical-engineering.electromagnetics.transmission-line-waves
name: transmission-line-waves
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [characteristic-impedance, electrical-engineering, electromagnetics, microstrip, pcb-trace-impedance, reflection-and-vswr, reflection-coefficient, transmission-line-waves, vswr, wave-propagation]
level: practitioner
status: draft
description: "Treat signal lines as transmission lines: characteristic impedance, reflections, VSWR and PCB trace impedance."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Waves and signal transmission lines

1. **Characteristic impedance:** lossless `Z0 = sqrt(L'/C')`; velocity `v = 1/sqrt(L'C')`. Coax: `Z0 = (60/sqrt(er)) ln(b/a)`.
2. **Reflection coefficient:** `Gamma = (ZL - Z0)/(ZL + Z0)`; `VSWR = (1 + |Gamma|)/(1 - |Gamma|)`; return loss `RL = -20 log|Gamma|`. A 75 ohm load on a 50 ohm line: `Gamma = 0.2`, VSWR 1.5, RL 14 dB.
3. **When it matters:** treat the interconnect as a transmission line if the electrical length exceeds about one tenth of the signal rise time (`t_r`) times velocity (`length > t_r v / 6` is a commonly quoted rule).
4. **PCB microstrip:** `Z0` depends on width, dielectric height and `er`; use a field solver or IPC-2141 formulas; keep reference plane continuous.
5. **Termination:** series source termination, parallel, AC termination, differential 100 ohm; match to avoid ringing.
6. **Pulse reflections:** a step into an open end returns with `Gamma = +1`; short returns with `-1`; time-domain reflectometry measures impedance versus distance.

**Verify:** TDR or VNA measurement of the impedance of a test coupon.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
