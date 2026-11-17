---
id: engineering-technology.electrical-engineering.power-electronics.buck-converter-design
name: buck-converter-design
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [buck-converter, step-down, dc-dc, smps, synchronous-buck, switching-regulator, inductor-sizing, ripple-current, output-capacitor, input-capacitor, mlcc-dc-bias, mosfet-losses, switching-losses, gate-drive, dead-time, thermal-design, junction-temperature, loop-compensation, type-ii, type-iii, current-mode, voltage-mode, pcb-layout, hot-loop, ltspice, buck-capacitor-selection]
level: practitioner
status: verified
description: "Design a synchronous buck converter: duty cycle, inductor and capacitor sizing, MOSFET loss and thermal budget, loop compensation, layout."
sources:
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
  - "Mohan, Undeland & Robbins, Power Electronics: Converters, Applications, and Design"
  - "Basso, Switch-Mode Power Supplies: SPICE Simulations and Practical Designs"
  - "https://www.ti.com/lit/an/slva477b/slva477b.pdf"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Synchronous buck converter design — from spec to a stable, cool board

**Goal:** choose L, C, switches and compensation for a step-down converter so ripple,
efficiency, thermal and transient specs are met with margin, using a 12 V → 3.3 V,
5 A, 500 kHz example throughout.

## 1. Spec and duty cycle
Write down Vin(min/nom/max), Vout, Iout(max), ripple (e.g. 1% Vout p-p), transient
step (e.g. 2.5 A in 1 µs, ±3% deviation), fsw, ambient.
`D = Vout / (Vin · η)` → ideal D = 3.3/12 = 0.275. Use Vin(max) for inductor ripple
and Vin(min) for max duty / current-limit checks.

## 2. Inductor
Pick ripple ΔIL = 20–40% of Iout (TI application note SLVA477 eq. 6 gives the same 20% to 40% of IOUT(max); its eq. 5 inductor formula equals the one below) (30% → 1.5 A):
`L = (Vin − Vout) · D / (fsw · ΔIL) = 8.7 × 0.275 / (500e3 × 1.5) ≈ 3.2 µH` → 3.3 µH (computed 3.19 µH).
Peak current = Iout + ΔIL/2 = 5.75 A (computed). Choose an inductor with **saturation current
above the controller's current-limit**, not just above 5.75 A (else a short-circuit
saturates it), RMS rating ≥ Iout, and check its core loss at your fsw and ripple —
DCR-only loss estimates underestimate hot ferrite parts.

## 3. Output capacitor
Ripple has two parts: `ΔV ≈ ΔIL / (8 · fsw · C) + ΔIL · ESR`. For 33 mV:
C ≥ 1.5 / (8 × 500e3 × 0.033) ≈ 11 µF (computed 11.4) and ESR well below 22 mΩ (33 mV / 1.5 A, computed) → ceramics.
Transient usually dominates: C ≳ ΔI² · L / (2 · Vout · ΔV) for overshoot on load
release (2.5 A step, 3.3 µH, ±3% gives 31.6 µF, computed) — size for that and the loop bandwidth, often several × 22 µF.
**MLCC DC-bias:** an X5R/X7R part can lose half or more of its capacitance at rated
voltage in small case sizes (gated: unconfirmed, source is paywalled or blocked). Use the maker's bias curve, not the box value.

## 4. Input capacitor
RMS current `Iout · √(D(1−D))` = 5 × 0.447 ≈ 2.2 A (computed 2.23 A; the maximum of √(D(1−D)) is at D = 0.5, giving 2.5 A). Place MLCCs
right at the high-side drain / low-side source; add bulk for the source impedance.

## 5. MOSFETs and losses
- Voltage rating ≥ 1.25–1.5 × Vin(max) for ringing margin (30 V parts for 12 V rails) (practice figure (gated: unconfirmed, source is paywalled or blocked)).
- High-side: conduction `Irms² · Rds(on)` with Irms ≈ Iout√D, plus switching
  `½ · Vin · Iout · (tr + tf) · fsw` — low Qg/Qgd matters most here.
- Low-side: conduction dominates (Irms ≈ Iout√(1−D)) — pick lowest Rds(on).
- Gate drive loss `Qg · Vdrive · fsw` per FET; dead-time body-diode loss
  `Vf · Iout · 2·t_dead · fsw` and reverse-recovery loss.
- Rds(on) rises ~1.4–1.8× from 25 °C to 125 °C; use the hot value (gated: unconfirmed, source is paywalled or blocked).
- Junction: `Tj = Ta + P · RθJA`; RθJA on a datasheet assumes a specific copper
  area — your board may be much worse. Target Tj ≤ ~110–125 °C at worst ambient (gated: unconfirmed, source is paywalled or blocked).

## 6. Control loop
- Current mode is easier to compensate (Type II); voltage mode with an LC double
  pole needs Type III.
- Crossover fc ≈ fsw/10 to fsw/5 (50–100 kHz here), phase margin ≥ 45° (60° preferred),
  gain margin ≥ 10 dB (rules of thumb (gated: unconfirmed, source is paywalled or blocked)), over Vin and load range and with derated capacitance.
- Ceramic outputs push the ESR zero very high, so don't rely on it for phase boost.

```python
Vin, Vo, Io, fsw, r = 12, 3.3, 5, 500e3, 0.3
D = Vo/Vin; dI = r*Io
L = (Vin-Vo)*D/(fsw*dI); C = dI/(8*fsw*0.033)
print(f"D={D:.3f} L={L*1e6:.2f}uH Ipk={Io+dI/2:.2f}A Cmin={C*1e6:.1f}uF Icin={Io*(D*(1-D))**0.5:.2f}A")
```

## 7. Layout (where most buck designs actually fail)
Minimise the **hot loop** (Cin → high-side → low-side → Cin) — it carries the
di/dt; keep the switch node copper small (EMI) but the power paths wide; Kelvin-route
the feedback from the output cap; single solid ground plane under the stage.

## Verify
- [ ] Measured ripple and inductor peak current match the calc within ~20%.
- [ ] Inductor Isat exceeds the current-limit setpoint at hot temperature.
- [ ] Output capacitance computed with DC-bias derating.
- [ ] Bode plot (network analyser or injection) shows PM ≥ 45° at min/max Vin and load.
- [ ] Thermal camera at max load/ambient keeps FETs and inductor within rating.
- [ ] Switch-node ringing stays below the FET Vds rating with margin.
