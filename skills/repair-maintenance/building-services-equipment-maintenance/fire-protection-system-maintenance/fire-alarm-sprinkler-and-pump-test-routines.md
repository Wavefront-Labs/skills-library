---
id: repair-maintenance.building-services-equipment-maintenance.fire-protection-system-maintenance.fire-alarm-sprinkler-and-pump-test-routines
name: fire-alarm-sprinkler-and-pump-test-routines
category: repair-maintenance
field: building-services-equipment-maintenance
product: fire-protection-system-maintenance
tags: [building-services-equipment-maintenance, fire-protection-system-maintenance, fire-alarm, fire-alarm-panel, call-point, smoke-detector, heat-detector, weekly-fire-alarm-test, sprinkler, sprinkler-inspection, alarm-valve, inspector-test-valve, main-drain-test, fire-pump, churn-test, no-flow-test, extinguisher, emergency-lighting, nfpa-25, nfpa-72, nfpa-10, bs-5839, bs-en-12845, bs-5266, impairment, fire-log-book, itm]
level: practitioner
status: gated
description: "Run fire-system ITM routines: weekly alarm call-point tests, sprinkler valve and main-drain tests, fire pump churn tests, extinguisher and emergency lighting checks, impairment control."
sources: ["https://www.nfpa.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fire alarm, sprinkler and pump test routines

**Goal:** prove each fire system works on the schedule the code requires, record it, and
never leave a building unprotected without controls. Frequencies come from the governing
standard: **US** NFPA 72 (alarms), NFPA 25 (sprinklers/pumps), NFPA 10 (extinguishers),
NFPA 101 (emergency lighting); **UK** BS 5839-1, BS EN 12845, BS 5306-3, BS 5266-1. The
routines below are the common in-house ones; periodic servicing is done by competent
contractors. Check the current edition and the insurer's requirements.

## 0. Before any test: control the impact
- Tell the alarm receiving centre/monitoring company and the fire brigade link if
  automatic; put the signal "on test" for a set time.
- Warn occupants (and plant that shuts down on alarm: lifts, AHUs, door releases).
- If a system will be out of service: **impairment procedure** — tag the panel/valve,
  notify the insurer/authority where required, fire watch patrols, time-limited.
- Everything goes in the fire log book: date, what was tested, result, defects, who.

## 1. Fire alarm (UK weekly call-point test; US inspection per NFPA 72)
1. Operate **one manual call point** per week in rotation (gated: unconfirmed, source is paywalled or blocked; use the test key), so every
   call point is tested over the cycle. Same time each week helps occupants.
2. Confirm: panel shows the right zone/device, sounders and beacons operate throughout,
   remote signalling received, interfaces (door releases, lift recall, AHU shutdown)
   operate.
3. Reset the call point, silence and reset the panel, confirm normal state.
4. Daily/regular: panel shows normal, no faults; investigate every fault and
   **false alarm** (record its cause — high false alarm counts need action).
- Detector testing (smoke aerosol, heat) is part of periodic servicing; never use spray
  paint or real smoke inside detectors' chambers outside the approved tester.

## 2. Sprinklers
- **Routine visual:** control valves open and **secured** (strapped/locked or
  supervised), gauges normal, no obstructions/damage, heads not painted or blocked,
  clearance below deflectors as the standard requires (gated: unconfirmed, source is paywalled or blocked).
- **Alarm test (frequency per the standard):** open the alarm test valve /
  inspector's test, confirm the water motor gong and/or flow switch signals the panel
  within the time the standard requires.
- **Main drain test (frequency per the standard):** record
  static pressure, open the main drain fully, record residual pressure, close slowly.
  Compare to previous results — a significant drop suggests a partly closed valve or
  supply problem.
- **Dry pipe:** air pressure and priming water level, quick-opening device checks, low-
  point drains before frost.

## 3. Fire pumps
- **Churn (no-flow) test:** frequency per the standard and edition (diesel and electric
  pumps differ). Start automatically by dropping pressure
  (opening the test drain), not by the manual start button alone.
- Record: start pressure, suction and discharge pressure, run time (per the standard), packing gland drip (should drip, not stream or be dry), unusual
  noise/vibration, diesel coolant/oil/fuel, battery voltage and charger.
- Annual **flow test** at rated flows by the contractor, plotted against the pump curve.

## 4. Extinguishers and emergency lighting
- **Monthly:** extinguishers in place, visible, pin and seal intact, gauge in green, no
  damage; tag dated. Annual service by a competent person; extended service/hydro test
  at maker/code intervals.
- **Emergency lighting:** monthly short functional test (simulate mains failure — key
  switch); annual full-rated-duration test (duration per the standard, gated: unconfirmed, source is paywalled or blocked). Record any
  failed fittings and repair promptly.

## Gotchas
- A closed sprinkler valve is the most common reason sprinklers fail: lock and supervise them.
- Tests that "always pass" because the remote centre wasn't actually receiving — confirm receipt.
- Don't leave panels in test/disabled mode overnight; check before leaving.

## Verify
- [ ] Monitoring centre informed before and confirmed back to normal after.
- [ ] Call point (in rotation) operated; all outputs and interfaces confirmed.
- [ ] Sprinkler valves open and secured; gauges recorded; alarm gong/flow switch signalled.
- [ ] Pump started automatically; pressures and run time logged.
- [ ] Extinguisher tags and emergency lighting results logged; defects ticketed.
- [ ] No impairment left open without a recorded fire watch and end time.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (NFPA 72, 25, 10, 101) and United Kingdom (BS 5839-1 and related); the edition in force and the insurer govern.
The governing standards (NFPA 72, NFPA 25, NFPA 10, NFPA 101, BS 5839-1, BS EN 12845, BS 5306-3, BS 5266-1) are paywalled, so the test frequencies, clearances and durations that remain are marked gated. Where a figure was not essential it was replaced by 'per the standard'. Removed: diesel and electric pump run times, sprinkler alarm and main drain frequencies, pump test frequencies.

Method: documentation only; no commands were run.
