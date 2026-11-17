---
id: repair-maintenance.watch-clock-repair.quartz-watch-service.quartz-battery-replacement-and-circuit-testing
name: quartz-battery-replacement-and-circuit-testing
category: repair-maintenance
field: watch-clock-repair
product: quartz-watch-service
tags: [quartz-watch-service, watch-repair, horology, quartz-watch, battery-replacement, silver-oxide, sr626sw, 377, 371, 364, 395, ac-reset, multimeter, coil-resistance, consumption-current, stepper-motor, lavet-motor, eta-f06, miyota, ronda, movement-swap, chronograph-reset, kinetic, capacitor, gasket, water-resistance, leaking-battery]
level: practitioner
status: draft
description: "Service quartz watches: correct battery swap with AC reset, test battery, coil and circuit with a multimeter or quartz tester, clean leaks, swap a dead movement, and reseal the case."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quartz battery replacement and circuit testing

**Goal:** get a stopped quartz watch running reliably — not just by putting in a
battery, but by finding out why it stopped and leaving the case sealed.

> Draft: reset procedures, coil resistances and consumption figures are calibre-
> specific; check the movement maker's technical sheet (ETA, Ronda, Miyota, Seiko/
> Hattori). Values below are typical ranges for small analogue movements.

## 1. Open and identify
- Note the case type: screw-back (case wrench), snap-back (case knife at the lug
  notch), or screwed back with four screws. Protect the case.
- Read the **battery number** on the old cell and the calibre on the movement.
  Common: 364/SR621SW, 371/SR920SW, 377/SR626SW, 395/SR927SW, 2016/2025 lithium
  coin for digitals and some chronographs.
- Use **silver-oxide** (SR) cells for analogue watches, not alkaline (LR — lower,
  falling voltage, leak more).

## 2. Replace the battery
1. Use **plastic or non-magnetic tweezers** — steel tweezers can short the cell
   against the plate and magnetise parts.
2. Note battery orientation and clamp/strap; some straps carry the **AC reset**
   marking ("AC" or "R" with an arrow).
3. Check for leakage (white crust, green corrosion) — see section 5.
4. Insert new cell (check voltage first: SR fresh ≈ **1.55 V**), secure the clamp.
5. **AC reset** where required: short the AC point to the battery + (housing)
   with tweezers for ~2 s — resets the IC; needed on many movements to avoid
   erratic stepping, and essential on chronographs before hand-zeroing.
6. Watch the seconds hand for a few steps; confirm 1-second steps (a **4-second jump**
   = end-of-life indicator — the battery or a weak cell).
7. Chronographs: run the hand-zero procedure from the calibre sheet (e.g. pull crown
   to position 2, use pushers to advance each counter to zero).

## 3. If it still doesn't run: test, don't guess
With a multimeter (or a dedicated quartz tester):
- **Battery under load** — voltage shouldn't sag much below ~1.5 V.
- **Coil resistance:** disconnect power, measure across coil terminals. Typical small
  movements **~1.5–3 kΩ**. Open circuit = broken coil wire (replace coil or movement);
  far below = shorted.
- **Consumption current:** meter in series with the battery (µA range). Typical
  analogue movement **~0.5–3 µA** average (pulses higher). High consumption = dirt,
  stiff train, or circuit fault; zero = no output.
- **Pulse test:** a quartz tester detects motor pulses without opening the movement;
  pulses present but hands stopped = mechanical (train, hands catching, dirt);
  no pulses = circuit/IC or quartz failure.
- Also check: hands touching each other or the crystal; stem not pushed fully in
  (many movements stop in the setting position); date wheel jammed.

## 4. Mechanical service or swap
- Most inexpensive quartz movements (Miyota 2035, Ronda 515, ETA F06/G10) are
  **replaced** rather than serviced — compare movement cost vs labour.
- Swapping: match calibre, hand hole sizes, date position and **stem** (cut the new
  stem to the old length — tip to crown seat — and fit crown). Transfer dial feet
  or use dial dots if feet don't match.
- Higher-grade quartz (e.g. ETA high-accuracy, Grand Seiko 9F): service like a
  mechanical — clean, minimal lubrication per chart, and the rate trimming procedure
  for the calibre.

## 5. Battery leaks
- Remove cell; clean corrosion from contacts and plate with a cotton bud and a little
  isopropyl alcohol; light abrasive (glass fibre brush) on contacts only.
- If electrolyte reached the circuit or coil, test as above; often replace movement.

## 6. Reseal
- Inspect and **replace the caseback gasket** (don't reuse flattened or cracked ones);
  lightly grease with silicone.
- Check crown gasket; replace crown if it's sloppy.
- Close the case; for water-resistant watches, pressure test (dry tester) and do a
  condensation check. Tell the customer if the watch wasn't tested.

## Gotchas
- Old cell measured with no load can read fine yet fail under the motor pulse.
- Fingers on the cell's flat faces — oils reduce contact; handle by edges.
- Steel tweezers across the cell = shorted battery and magnetised parts.
- Forgetting the AC reset gives "new battery, still stopped" complaints.

## Verify
- [ ] Correct SR cell, ≥ 1.55 V, inserted with plastic tweezers.
- [ ] AC reset done where specified; chronograph hands zeroed.
- [ ] Seconds hand steps once per second; runs for a check period (e.g. 24 h).
- [ ] If faulty: coil, consumption and pulse tests recorded.
- [ ] Gasket replaced; case closed; water resistance tested or customer told.
