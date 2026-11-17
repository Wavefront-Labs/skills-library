---
id: engineering-technology.electrical-engineering.motor-drive-design.vfd-application
name: vfd-application
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [vfd, vsd, variable-frequency-drive, ac-drive, inverter, induction-motor, motor-sizing, normal-duty, heavy-duty, inverter-duty, nema-mg1, nema-mg1-part-31, iec-60034-17, iec-60034-25, reflected-wave, dv-dt-filter, sine-filter, bearing-currents, shaft-grounding, harmonics, ieee-519, line-reactor, afe, 18-pulse, nec-430, braking-resistor, field-oriented-control, v-hz, affinity-laws, vfd-cable-and-dv-dt, vfd-bearing-currents]
level: practitioner
status: gated
description: "Apply a VFD to an AC motor: size by current and duty, inverter-duty insulation, cable length/dv-dt, bearing currents, harmonics (IEEE 519), NEC 430."
sources:
  - "NEMA MG 1, Motors and Generators (Parts 30 and 31)"
  - "IEC TS 60034-17 and IEC TS 60034-25 (converter-fed induction motors)"
  - "IEEE Std 519-2022, Standard for Harmonic Control in Electric Power Systems"
  - "NFPA 70, National Electrical Code, Article 430"
  - "Bose, Modern Power Electronics and AC Drives"
  - "ABB Technical Guide series (drives application guides)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# VFD application — matching drive, motor, cable and supply

**Goal:** a drive–motor system that delivers the load's torque across the speed range,
survives its duty, doesn't destroy the motor's insulation or bearings, and stays
within the supply's harmonic limits and the electrical code.

## 1. Characterise the load first
- **Variable torque** (centrifugal pumps, fans): T ∝ n², P ∝ n³. Running at 80% speed
  needs ~51% power (0.8³ = 0.512, computed) — this is where VFD energy savings come from.
- **Constant torque** (conveyors, PD pumps, extruders, hoists): full torque at low
  speed, often high breakaway torque.
- **Constant power** (winders, spindles above base speed): field-weakening region.
Get the torque–speed curve, required overload (and for how long), starts per hour,
and whether the load overhauls (regenerates).

## 2. Size the drive by current, not kW
- Drive continuous output current ≥ motor nameplate FLA at the operating voltage
  (more if service factor is used or motor is multi-pole/low-efficiency).
- Typical duty ratings: **normal duty** ≈ 110% for 60 s (VT loads), **heavy duty**
  ≈ 150% for 60 s (CT loads). Exact values vary by manufacturer (typical figures (gated: unconfirmed, source is paywalled or blocked)).
- Derate for altitude (often above 1000 m), ambient above ~40 °C, and raised carrier
  frequency (manufacturers publish curves; 2–4 kHz is a common default).
- One drive feeding several motors: sum currents, add per-motor overloads, and use
  V/Hz control (vector modes assume one motor).

## 3. Motor suitability
- Specify inverter-duty: NEMA MG 1 Part 31 (vendor summaries give a design limit of 3.1 × rated line-to-line voltage peak, with rise time 0.1 µs or slower, for ≤600 V motors; the exact MG 1 figure (gated: unconfirmed, source is paywalled or blocked)) or IEC TS 60034-25/-17 equivalents. General-purpose motors
  (Part 30) have a much lower peak-voltage capability.
- Low-speed cooling: a TEFC motor's shaft fan loses airflow; constant-torque loads
  below ~50% speed often need derating, a constant-speed blower, or a motor rated for
  the turndown (e.g. 10:1 or 1000:1). Variable-torque loads rarely have this issue.
- Above base speed torque falls ~1/n; check the load's demand there.

## 4. Cable, reflected wave and bearings
- Fast IGBT edges plus long motor leads cause reflected-wave overshoot up to ~2× DC
  bus at the motor terminals. Critical length can be tens of metres at 480 V.
  Beyond the drive maker's limit fit a **dV/dt filter** (moderate lengths) or **sine
  filter** (very long runs, submersible pumps, step-up transformers).
- Use symmetrical shielded VFD cable with 360° gland termination at both ends; run
  separate from signal cables.
- Common-mode voltage drives **bearing currents** (EDM fluting). Mitigate with shaft
  grounding rings, and an insulated non-drive-end bearing on larger frames (often
  quoted above ~100 kW / frame 280+ (gated: unconfirmed, source is paywalled or blocked); confirm with the motor maker).

## 5. Supply side
- 6-pulse diode front end draws ~30–40% THDi with a 3–5% line reactor or DC choke,
  much more without. Check IEEE 519-2022 current distortion limits at the PCC (they
  depend on Isc/IL). Escalate to 12/18-pulse, active filters or an **active front
  end** (also regenerative) when large drive load is a big fraction of the transformer.
- Regeneration: an overhauling/high-inertia load trips on DC overvoltage unless you
  add a braking chopper + resistor or use AFE; size the resistor for peak power and
  duty cycle.

## 6. Code and protection (NEC, US)
- NEC 430.122: input conductors ≥ 125% of the drive's rated input current (confirm section and percentage in the adopted NEC edition (gated: unconfirmed, source is paywalled or blocked)).
- Branch short-circuit protection: use the type and maximum rating listed by the
  drive maker (often semiconductor fuses) to keep the drive's SCCR valid.
- Motor overload: the drive's electronic overload may be accepted if listed for it;
  separate overloads still needed per motor on multi-motor drives.
(IEC installations follow IEC 60364 and the manufacturer's EMC/IEC 61800 guidance.)

## 7. Commissioning
Enter full nameplate data, run autotune (rotating if the load can be uncoupled, else
static), set accel/decel to the process, set skip frequencies around mechanical
resonances, set min speed for pump cooling/lubrication, confirm motor rotation.

## Verify
- [ ] Drive current rating and duty class cover the load's continuous and overload demand after derates.
- [ ] Motor is inverter-duty and its low-speed thermal capability matches the load type.
- [ ] Motor lead length is within the drive limit or a filter is fitted.
- [ ] Harmonic study shows IEEE 519 (or utility) limits met at the PCC.
- [ ] Braking path exists for any overhauling/fast-decel duty.
- [ ] Input conductors and SCPD meet NEC 430.122 / maker's listing (or local IEC equivalent).
