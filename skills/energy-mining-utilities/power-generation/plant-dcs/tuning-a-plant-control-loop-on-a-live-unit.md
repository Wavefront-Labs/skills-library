---
id: energy-mining-utilities.power-generation.plant-dcs.tuning-a-plant-control-loop-on-a-live-unit
name: tuning-a-plant-control-loop-on-a-live-unit
category: energy-mining-utilities
field: power-generation
product: plant-dcs
tags: [plant-dcs, power-generation, dcs, distributed-control-system, scada, emerson-ovation, abb-symphony, abb-800xa, siemens-t3000, ge-mark-vie, yokogawa-centum, honeywell-experion, pid, loop-tuning, bump-test, step-test, manual-mode, bumpless-transfer, feedforward, cascade, setpoint, gain, integral, derivative, valve-stiction, deadband, management-of-change, interlocks]
level: advanced
status: draft
description: "Retune a power-plant DCS loop on a running unit without tripping it: permissions, a safe bump test, reading the response, small parameter moves, valve stiction checks and documenting the change."
sources: ["Vendor DCS engineering manuals (general practice, paraphrased)", "ISA-5.1 / ISA-18.2 concepts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tuning a plant control loop on a live unit

**Goal:** improve a misbehaving loop — a cycling deaerator level, a sluggish
superheater spray, a hunting fuel-gas pressure — on a unit that is generating,
without causing a trip or an emissions excursion. The tuning theory is covered in
engineering-technology.chemical-engineering.process-control.pid-loop-tuning; this skill
is about doing it safely on a live power-plant DCS (Emerson Ovation, ABB, Siemens
T3000, GE Mark VIe, Yokogawa, Honeywell and similar).

## 1. Permission and boundaries
- Tuning is a change to plant: raise it under your **management-of-change** (MOC)
  or controls-change procedure and get the shift supervisor's agreement for the
  window. Many plants require a second engineer to review.
- Pick a time with stable load, no other evolutions, and the grid operator aware if
  the unit's output could move (e.g. tuning a master pressure or load loop).
- Know the **trip-related limits** near this loop (drum level trip points, furnace
  pressure trips, steam temperature limits). Agree with the operator the value at
  which you abort and they take manual control.
- Save/record the **existing parameters** — screenshot or export — before changing
  anything.

## 2. Diagnose before tuning
- Trend PV, SP and controller output (OUT) together, plus valve position feedback if
  available, over hours.
- **Is it really tuning?** Check for:
  - **Valve stiction:** output ramps, valve doesn't move, then jumps; PV shows a
    square-ish wave and output a sawtooth. Retuning won't fix it — maintenance will.
  - **Interaction:** two loops fighting (e.g. spray and burner tilt both controlling
    steam temperature).
  - **Disturbance:** a feedforward missing or wrong (load change causing level swings).
  - **Measurement:** noisy or slow transmitter, wrong range, impulse line problems.

## 3. A safe bump test
1. With the operator, put the loop in **manual** (bumpless transfer — check output
   doesn't jump).
2. Make a small output step — often 2–5 % — in the safe direction, as agreed.
3. Record the response: dead time, time constant, gain (ΔPV/ΔOUT). Wait until it
   settles or reaches your abort limit.
4. Step back. Repeat in the other direction if safe (it reveals nonlinearity and
   stiction).
5. Return to auto only once PV is near SP.
For integrating processes (levels), PV won't settle; record the ramp rate and step
back promptly.

## 4. Change parameters in small moves
- Calculate new settings from the model (lambda/SIMC rules), but move toward them in
  steps — e.g. change gain by no more than ~25–50 % at a time.
- Check the controller's **algorithm form** (ideal, series, parallel) and units: some
  systems use reset in repeats/minute, others integral time in seconds. Confusing
  them is the most common tuning error.
- After each change, make a **small setpoint step** (if the operator agrees) and
  watch overshoot and settling.
- For cascade loops, tune the inner (secondary) loop first, faster than the outer.

## 5. Document
- Record before/after parameters, test trends, and the reason on the MOC.
- Update the loop's tuning sheet; tell the next shift what changed.
- Download/save to the DCS database so a controller reload doesn't revert it.

## Gotchas
- Tuning around a sticky valve hides the problem and makes the loop worse when the
  valve is fixed.
- Online changes on some systems apply immediately; on others they need an explicit
  download — know which, and whether redundant controllers stay in sync.
- Never disable an interlock or protection to make a test easier.
- Uncertain: parameter names, units and download steps differ by vendor and version.

## Verify
- [ ] MOC approved, abort limits agreed with the operator, old parameters saved.
- [ ] Stiction, interaction and measurement problems ruled out first.
- [ ] Bump test trend saved with dead time, time constant and gain noted.
- [ ] Parameter changes made in small steps with a setpoint test after each.
- [ ] New settings saved in the database and handed over to shift.
