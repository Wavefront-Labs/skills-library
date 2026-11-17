---
id: engineering-technology.electrical-engineering.power-electronics.pfc-rectifier
name: pfc-rectifier
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [boost-pfc, electrical-engineering, iec-61000-3-2, inrush-limiting, pfc-control-loops, pfc-rectifier, power-electronics, power-factor-correction-converter, rectifier]
level: practitioner
status: draft
description: "Design a boost PFC stage: inductor, bulk capacitor, voltage and current loops, and inrush limiting."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Rectifiers and active PFC

1. **Need:** diode-bridge plus capacitor draws narrow current pulses; IEC 61000-3-2 limits harmonic current for equipment up to 16 A per phase, so most power supplies above about 75 W use PFC.
2. **Boost PFC:** ac line is rectified, the boost inductor follows `i = k v_in`. Peak input `I_pk = sqrt(2) P/(eta Vrms pf)`. Inductor sized at the worst-case line peak: `L = Vpk (1 - Vpk/Vout) / (dI f_sw)` with `Vpk = sqrt(2) Vin_min,rms` and `dI` about 20 to 30 percent of `I_pk`.
3. **Bulk capacitor:** hold-up time `C = 2 P t_hold / (Vo^2 - Vmin^2)`; ripple at twice line frequency `dV = P/(2 pi f_line C Vo)`.
4. **Loops:** fast inner current loop (average current mode or critical-conduction), slow outer voltage loop with crossover below about 20 Hz so it doesn't distort the current reference.
5. **Inrush:** NTC thermistor with bypass relay or SCR precharge.
6. Include EMI filter, X and Y capacitors, and a brown-out detection.
7. For higher power, use interleaved or totem-pole bridgeless topologies.

**Verify:** measure pf and THD at 10, 50 and 100 percent load across the line-voltage range.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
