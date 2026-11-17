---
id: engineering-technology.electrical-engineering.power-electronics.inverter-modulation
name: inverter-modulation
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [electrical-engineering, grid-tied-inverter-control, inverter-modulation, inverter-pwm, pll, power-electronics, spwm, svpwm, third-harmonic-injection, three-phase-inverter-dead-time]
level: advanced
status: draft
description: "Choose PWM strategies for single and three-phase inverters: sine-triangle, SVPWM, dead-time compensation and grid-tied current control."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Inverter modulation and control

1. **Sine-triangle PWM:** modulation index `m = V_ref_peak/V_carrier_peak`; linear range `m <= 1` gives `V_LL,rms = 0.612 m Vdc`; overmodulation distorts.
2. **SVPWM / third-harmonic injection:** extends the linear range 15.5 percent (`V_LL,rms` up to `0.707 Vdc`) by centring the zero vectors; generate with min-max offset `v_offset = -(max + min)/2` added to the three references.
3. **Dead time:** blanking between complementary switches (a few hundred ns for MOSFETs, 1 to 3 us for IGBTs) creates voltage error `dV ~ 2 Td f_sw Vdc` with polarity depending on current sign; compensate by current-sign feed-forward, and check at low current.
4. **Grid-tied inverter:** a PLL (SRF-PLL) locks to grid voltage; inner current loop in dq frame, outer DC link or power loop; LCL filter with active damping or passive damping; follow the grid code (IEEE 1547, EN 50549).
5. **Output filter:** choose `f_c` between 10 times grid frequency and one tenth of `f_sw`.

**Verify:** measure THD at several loads; check duty-cycle saturation and shoot-through protection.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
