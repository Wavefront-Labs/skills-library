---
id: engineering-technology.electronics-engineering.signal-integrity.decoupling-and-pdn
name: decoupling-and-pdn
category: engineering-technology
field: electronics-engineering
product: signal-integrity
tags: [signal-integrity, power-integrity, pdn, power-distribution-network, decoupling, bypass-capacitors, target-impedance, mlcc, dc-bias-derating, esl, mounted-inductance, anti-resonance, plane-capacitance, ir-drop, vrm, load-step, 2-port-shunt-through, vna, pdn-analyzer, siwave, sigrity, ripple]
level: advanced
status: gated
description: "Design a power distribution network: target impedance, decoupling capacitor selection and placement, plane capacitance, via inductance and PDN verification."
sources:
  - "Bogatin, Signal and Power Integrity — Simplified"
  - "Swaminathan & Engin, Power Integrity Modeling and Design for Semiconductors and Systems"
  - "Smith & Bogatin, Principles of Power Integrity for PDN Design — Simplified"
  - "Novak, Frequency-domain characterization of power distribution networks (DesignCon papers)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Decoupling and PDN design — keep the rail's impedance below target across frequency

**Goal:** make the impedance seen by each IC's power pins, from DC to the frequencies
its current transients contain, low enough that the worst load step keeps the rail
inside its tolerance — with the fewest parts that actually do something.

## 1. Compute the target impedance
**Z_target = (V_rail × allowed ripple fraction) / ΔI_transient**
- Example: 1.0 V core, ±3 % → 30 mV; worst load step 2 A → **15 mΩ** (computed; the 3.3 V example gives 0.825 Ω).
- Example: 3.3 V I/O, ±5 % → 165 mV; 200 mA step → ~0.8 Ω (easy: a few MLCCs).
- ΔI comes from the vendor's power estimator (FPGA/SoC tools) or ~50 % of max current
  if you have nothing better (a rule of thumb (gated: unconfirmed, source is paywalled or blocked)). Allow part of the tolerance for the regulator's DC
  accuracy — it shares the same budget.
- The bandwidth you must cover runs up to where the package/die capacitance takes
  over, typically tens to a few hundred MHz at the board. Beyond that, board-level
  capacitors cannot help no matter how many you fit.

## 2. Know what each element covers
| Element | Effective range (rough) |
|---|---|
| Regulator (VRM) control loop | DC to ~10–100 kHz (its loop bandwidth) |
| Bulk caps (polymer/tantalum, 10–470 µF) | ~kHz to ~1 MHz |
| MLCCs (0.1–22 µF, 0402/0603) | ~1 MHz to ~50–200 MHz, limited by mounted inductance |
| Plane pair capacitance | above ~100 MHz; ≈ 37 pF/cm² for 0.1 mm FR-4 (computed: ε0·εr/d = 37.2 pF/cm² at εr = 4.2; εr 4.4 gives 39; scales as εr/d) |
| Package and on-die capacitance | hundreds of MHz and up |

## 3. Pick capacitors by impedance, not by habit
- An MLCC is a series RLC: above its self-resonance it is an inductor with
  Z ≈ 2πf·L_mounted. **Mounted inductance** (part ESL + pads + vias + plane spreading)
  is usually 0.5–1.5 nH for an 0402 (gated: unconfirmed, source is paywalled or blocked) and dominates the high-frequency behaviour —
  layout matters more than the value.
- **DC bias derating**: a 10 µF 0603 X5R 6.3 V part can keep well under half its
  nominal value at 3.3 V (typical, verify in the maker's tool (gated: unconfirmed, source is paywalled or blocked)). Use the manufacturer's model at your bias (Murata SimSurfing,
  KEMET K-SIM, TDK SEAT tools) — this is the most common decoupling mistake.
- **Anti-resonance**: two different-value caps form a parallel resonance between their
  SRFs where impedance peaks. Mitigate by using many caps of a few values with
  overlapping coverage, by having enough ESR (or controlled-ESR caps) to damp it, or by
  plane capacitance. Simulate the combined curve rather than following "0.1 µF + 10 nF
  + 1 nF per pin" folklore.
- Count: N parallel caps of mounted inductance L give ≈ L/N; to reach 15 mΩ at
  100 MHz you need L_total ≈ 24 pH (computed 23.9 pH), i.e. about 42 capacitors of 1 nH, so dozens of capacitors *plus* planes — which
  shows why high-current cores rely on planes and package capacitance.

## 4. Layout rules
- Via directly at each capacitor pad (or via-in-pad), shortest possible connection;
  a 1 mm trace between pad and via can double the mounted inductance.
- Put the power/ground plane pair **close** together (thin dielectric) and close to the
  side where the caps sit; current loop area is inductance.
- Place small caps on the back side directly under BGA power pins where feasible;
  bulk caps near the regulator and where the rail enters a region.
- Wide copper or planes for DC: check **IR drop** (plane resistance, neck-downs between
  vias, BGA via fields). Use remote sense on the regulator for low-voltage high-current rails.

## 5. Analyse
- Spreadsheet first: target, cap list with vendor models at bias, mounted L estimate.
- Then a PDN tool if the design warrants it: Altium PDN Analyzer (DC), Cadence
  Sigrity, Ansys SIwave, Keysight PIPro, or open approaches using vendor S-parameter
  cap models in a circuit simulator. Results are only as good as the cap and via models.
- Vendor PDN capacitor tables assume their reference stack-up; re-check if yours differs.

## 6. Measure
- **Impedance**: 2-port shunt-through measurement with a VNA (e.g. Bode 100 or similar,
  with a common-mode choke/isolator on the cable shield) across the board's
  capacitors. Reaching milliohms takes care with fixturing.
- **Time domain**: step the load (on-board load-step FET or a firmware stress pattern)
  and scope the rail at the IC with a short ground spring, 20 MHz BW limit off, and a
  1:1 or low-noise probe for millivolt ripple.

## Verify
- [ ] Target impedance written down per rail with the ΔI source stated.
- [ ] Capacitor values evaluated at their DC bias, not nominal.
- [ ] Simulated or calculated |Z| stays below target over the needed band, with no large anti-resonance peak.
- [ ] Every decoupling cap has its own short via path to the planes.
- [ ] DC IR drop at the far load is within budget.
- [ ] Measured rail noise under a realistic load step stays inside tolerance.
