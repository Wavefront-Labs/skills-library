---
id: repair-maintenance.appliance-repair.cooking-appliance-repair.oven-element-sensor-and-igniter-faults
name: oven-element-sensor-and-igniter-faults
category: repair-maintenance
field: appliance-repair
product: cooking-appliance-repair
tags: [appliance-repair, cooking-appliance-repair, oven, range, stove, cooker, bake-element, broil-element, grill-element, oven-sensor, rtd, 1080-ohm, oven-temperature, calibration, hot-surface-igniter, glow-bar, surface-element, infinite-switch, ceramic-hob, induction-hob, microwave, magnetron, door-switch, microwave-capacitor, thermal-fuse]
level: practitioner
status: draft
description: "Fix common oven and range faults: dead bake/broil elements, RTD temperature sensor checks (~1,080 ohm), slow gas igniters, surface element switches, plus microwave no-heat safety and checks."
sources: ["Manufacturer range tech sheets (sensor resistance tables)", "Author's synthesis; values vary by brand"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oven: elements, sensors and igniters

**Goal:** diagnose the fault families behind "oven won't heat", "temperature is off",
"hob ring won't work" and "microwave runs but doesn't heat", with measurements rather
than parts-swapping. Isolate power at the breaker (ranges are often hard-wired) and
confirm dead with a tester before opening.

## 1. Electric oven doesn't heat (or heats slowly / unevenly)
1. Does the display show error codes? Look them up (sensor open/short codes are common).
2. **Visual:** a failed bake or broil element often has a blister, split or burn mark.
3. **Measure the element** (disconnected): typically ~15–40 Ω for 240 V elements
   (R = V²/W: 240 V, 2,500 W ≈ 23 Ω). Open = dead. Check each terminal to the sheath:
   any continuity = shorted element (it'll trip breakers).
4. If elements are good, check voltage at the element terminals with the oven calling
   for heat (careful, live work — only if trained): no voltage → control board relay,
   wiring, or a tripped **thermal cutoff/high-limit** (often on the rear panel or above
   the oven cavity).
5. Convection fan ovens: fan element and fan motor are separate; a seized fan shows as
   uneven baking.

## 2. Temperature wrong: the oven sensor (RTD)
Most electronic ovens use a platinum RTD probe in the cavity's rear wall.
- Resistance at room temperature: commonly **~1,080–1,100 Ω at ~21 °C (70 °F)**
  for many US brands; rises with temperature (roughly +2 Ω per °F). Check your tech
  sheet — some brands use different values (e.g. ~500 Ω or 2 kΩ types).
- Measure at the sensor connector and again at the board harness (rules out wiring).
- An oven that reads correctly but bakes 15–25 °C off: many controls allow user **offset
  calibration** (often ±35 °F) via a button sequence — check with an oven thermometer
  in the centre after 20 minutes of cycling, average the high/low swings.

## 3. Gas oven slow to light / no bake (hot-surface igniter)
- Igniter glows orange but no flame for 60–90 s, or never: igniter has weakened and
  doesn't draw enough current to open the bi-metal safety valve.
- Measure igniter current in series (with an ammeter/clamp on a wire): a common flat
  "glow-bar" spec opens the valve at ≥ ~3.2–3.6 A; a weak igniter may draw ~2.5 A and glow
  but never open the valve. Replace with the same type.
- Never touch the igniter element — skin oil and knocks crack it.
- If the igniter is good and the valve doesn't open, test valve continuity. For gas
  safety, combustion and leak checks, see
  `repair-maintenance.appliance-repair.gas-appliance-service.combustion-and-leak-testing-gas-appliances`.

## 4. Hob: surface element won't heat
- Coil/radiant element: swap with a known-good same-size element where they plug in.
- Radiant (ceramic glass) elements: measure resistance; also the **limiter** (a rod
  thermostat across the element) can fail open.
- **Infinite switch** (energy regulator) controlling the element: cycles power by duty
  cycle. Test continuity across the switch line-to-load terminals at "high"; it should be
  closed. Stuck-on-high = welded contacts.
- Induction: error codes often mean pan detection or fan/cooling faults; inverter board
  work is specialist and high-voltage.

## 5. Microwave runs, turntable turns, no heat
**Danger:** the high-voltage capacitor can hold a lethal charge (around 2,000+ V) even
unplugged. Discharge it with an insulated screwdriver/resistor across terminals and to
chassis, per the service manual, before touching anything in the HV section. Many
technicians decline microwave HV work; doing so is reasonable.
- Check door interlock switches (several, including a monitor switch), the thermal fuse,
  and the main fuse; a blown fuse often means a failed interlock monitor switch.
- HV diode, capacitor and magnetron failures need proper testing equipment and
  knowledge; magnetron filament ≈ under 1 Ω, terminal-to-case open.

## Gotchas
- Self-clean cycles often kill thermal fuses, control boards and door locks — a typical
  "after self-clean it stopped working" pattern.
- Hard-wired ranges: turning off at the wall switch may not isolate everything; use the breaker.
- Uncertain: resistance and current values are typical published figures; confirm
  per model.

## Verify
- [ ] Power isolated and verified dead before disassembly; microwave capacitor discharged.
- [ ] Element resistance and insulation to sheath measured.
- [ ] RTD measured at the sensor and at the board; calibration offset checked with a thermometer.
- [ ] Gas igniter current measured; flame established within normal time.
- [ ] Oven reaches set temperature within tolerance after repair.
