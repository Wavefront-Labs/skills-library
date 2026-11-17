---
id: engineering-technology.electronics-engineering.hardware-bringup-test.first-power-on
name: first-power-on
category: engineering-technology
field: electronics-engineering
product: hardware-bringup-test
tags: [hardware-bringup-test, bring-up, board-bring-up, first-power-on, smoke-test, current-limit, bench-power-supply, power-rails, oscilloscope, multimeter, thermal-camera, short-circuit, fault-isolation, rework, power-sequencing, clock-check, reset, jtag, swd, validation, dvt, evt]
level: practitioner
status: draft
description: "Power up a new board safely: pre-power checks, current-limited ramp, rail verification, thermal scan, clock/reset checks, then staged functional bring-up."
sources:
  - "Horowitz & Hill, The Art of Electronics, 3rd ed."
  - "Tektronix, ABCs of Probes (primer)"
  - "Keysight, Evaluating Oscilloscope Fundamentals / probing application notes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# First power-on — find the faults before they find your only prototype

**Goal:** take a freshly assembled board from "never powered" to "every rail correct,
processor reachable by debugger" without damaging it, and leave a written record
that makes the next board faster.

## 0. Prepare (before the board arrives)
- A **bring-up sheet**: every rail with nominal voltage, tolerance, expected idle
  current, and its test point; sequencing order; expected clock frequencies; strap
  levels. Fill in measured values as you go.
- Expected input current from the power budget, so you can set a meaningful limit.
- The assembled board's BOM variant and any known errata.

## 1. Unpowered checks (10 minutes, saves boards)
1. **Visual under magnification**: polarity of diodes, electrolytics, tantalums
   (tantalum stripe = **positive**), pin-1 of ICs, solder bridges on fine pitch,
   tombstoned passives, missing parts, wrong regulator variant.
2. **Resistance from each rail to ground** with a DMM. Compare with a second board or
   expectations: a few ohms on a high-current core rail can be normal (large loads);
   **< 1 Ω on an I/O rail is suspicious**, 0 Ω is a short. Measure both polarities —
   ESD diodes and caps make readings drift.
3. Rail-to-rail resistance (e.g. 3.3 V to 1.8 V) — a short here destroys parts.
4. Check input connector polarity against the supply/cable you will use.

## 2. Current-limited first power
1. Bench supply set to the nominal input voltage, **current limit just above the
   expected idle current** (e.g. 1.5× expected, or 50–100 mA for a small MCU board).
2. Connect with the output **off**, then enable while watching the current. Ideally
   ramp voltage slowly from 0 V on the first board to see where current starts.
3. If the supply goes into current limit: power off immediately. Do not raise the
   limit "to see what happens".
4. If current is plausible, measure every rail at its test point and record it.
   Out-of-tolerance → stop and investigate before moving on.

## 3. Find heat and shorts
- **Thermal camera** (or IPA/freeze spray, or a finger with care on low-voltage boards)
  after 10–30 s: the hot part is usually the culprit or the victim.
- **Shorted rail localisation**: inject a current-limited supply (e.g. 1 A at ≤ 1 V)
  into the shorted rail and look for the hot spot with a thermal camera, or measure
  millivolt drops along the plane with a sensitive DMM — current flows toward the
  short.
- Remove suspected parts one at a time (start with the cheapest/most likely: a reversed
  tantalum, a bridged decoupling cap) and re-measure.

## 4. Rails done properly
Using an oscilloscope (not just a DMM):
- **Sequencing and ramp**: trigger on the first rail, capture all rails; compare to the
  datasheet sequence and monotonic ramp requirements.
- **Ripple/noise**: short ground spring at the capacitor, not the 15 cm ground lead
  (it adds tens of mV of pickup on switchers). Note the scope bandwidth limit used.
- **Load transient** later when the real load runs.

## 5. Clocks, reset, boot
- Crystal/oscillator running at the right frequency (use a low-capacitance probe or
  measure a buffered clock output; a 10× probe on a crystal pin can stop or pull it).
- Reset deasserts after rails are good; strap pins at intended levels during reset.
- Debugger connects (SWD/JTAG): read the device ID. Then a minimal "blink + UART"
  firmware before anything ambitious.

## 6. Staged functional bring-up
Enable one subsystem at a time: memory, then high-speed interfaces, then peripherals,
then radio/analog. After each, re-check rail currents and temperature. Keep a log of
every rework (what, why, on which board serial) — it becomes the ECO list for the next
revision.

## 7. Into validation
Once alive, move to a written design-validation plan: each requirement mapped to a
test, run across voltage/temperature corners and multiple boards (EVT/DVT style).
One working board proves little about production.

## Verify
- [ ] Rail-to-ground and rail-to-rail resistances recorded before power was applied.
- [ ] First power done current-limited, with input current within expectation.
- [ ] Every rail measured at its test point and within tolerance; sequencing captured on a scope.
- [ ] No unexpected hot spots after several minutes of operation.
- [ ] Clocks at the right frequency, reset/straps correct, debugger reads the device ID.
- [ ] Bring-up log and rework list saved with board serial numbers.
