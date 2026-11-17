---
id: repair-maintenance.automotive-repair.auto-electrical-diagnostics.charging-starting-and-parasitic-drain-testing
name: charging-starting-and-parasitic-drain-testing
category: repair-maintenance
field: automotive-repair
product: auto-electrical-diagnostics
tags: [automotive-repair, auto-electrical-diagnostics, car-battery, battery-test, conductance-tester, agm, efb, battery-registration, alternator, charging-voltage, ripple, starter-motor, voltage-drop, parasitic-drain, key-off-draw, module-sleep, fuse-voltage-drop, can-bus, termination-resistance, 60-ohms, multimeter, clamp-meter, oscilloscope, ground-strap]
level: practitioner
status: draft
description: "Find why a car battery goes flat or won't crank: battery test, charging voltage and ripple, starter voltage-drop tests, parasitic drain with module sleep timing, and a quick CAN bus resistance check."
sources: ["Midtronics / battery-tester application guides (conductance testing)", "Manufacturer parasitic draw procedures (sleep times, limits; structure only)", "ISO 11898 CAN physical layer (termination)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Charging, starting and parasitic drain testing

**Goal:** answer "why is my battery flat?" with measurements: is it the battery, the
charging system, the starting circuit, or something draining it while parked? Treat the
battery as the first suspect, and the last thing you replace without testing the rest.

## 1. Battery
1. Surface charge off (headlights on 30 s, or wait an hour after driving).
2. **Resting voltage:** ~12.6–12.7 V full, ~12.4 V ≈ 75 %, ≤ 12.0 V heavily discharged
   (lead-acid at ~ 20 °C).
3. **Conductance/load test** (e.g. Midtronics-type tester) set to the battery's type
   (flooded/EFB/AGM) and rated CCA/EN. Charge first if low — testers can't judge a flat battery.
4. Terminals: clean, tight, no white/green corrosion; check the main ground straps
   (battery–body, engine–body).
5. Replacing on start-stop cars: fit the same **type** (AGM/EFB) and capacity, and do
   **battery registration/coding** with a scan tool where required (BMW, VAG, some Ford and
   others) so the charging strategy adapts.

## 2. Charging system
- Engine running at ~ 2,000 rpm with loads off: typically **13.8–14.7 V** at the battery
  (smart-charging systems vary widely, 12.5–15 V by strategy — check spec before condemning).
- Load test: headlights, blower, rear demister on — voltage should stay above ~ 13.2 V.
- **AC ripple** at the battery (meter AC mV or scope): high ripple (commonly > ~ 0.5 V AC)
  → failed alternator diode; drains battery and confuses modules.
- **Voltage drop** on the charge path: positive (alternator B+ to battery +) and ground
  (alternator case to battery −) under load: each ideally < ~ 0.2–0.3 V.
- Serpentine belt slipping (squeal, glazed) mimics alternator failure.

## 3. Starting system (slow crank / click, no crank)
- During cranking, battery should stay above ~ 9.6–10 V (warm).
- **Voltage drop test while cranking** (fuel or ignition disabled):
  - Battery + post to starter B+ terminal: ≤ ~ 0.5 V.
  - Battery − post to starter body/engine block: ≤ ~ 0.3 V.
  - High drop → corroded cable/terminal/ground strap: fix that, not the starter.
- Click with no crank and good voltage at the starter's main terminal → starter
  solenoid/motor. No click → check the start signal at the solenoid trigger wire
  (immobiliser, neutral/clutch switch, relay).
- Clamp-meter crank current: a few hundred amps petrol, much higher diesel; very high
  current + slow crank → tight engine or failing starter.

## 4. Parasitic drain (flat after sitting)
1. Fully charged battery. Close doors but **latch the door/bonnet switches** (screwdriver in
   the latch) so the car thinks it's closed while you work; keep the key fob far away.
2. Fit a clamp meter capable of low DC amps around the negative cable (no disconnection
   needed), or an ammeter in series using a battery-terminal switch so modules don't wake on
   reconnection.
3. Lock the car and **wait for modules to sleep**: often 20–60+ minutes on modern cars
   (some manufacturers specify longer). Watch the draw step down.
4. Acceptable sleep current: commonly **≤ ~ 50 mA** (many modern cars 20–30 mA; check spec).
5. If high: find the circuit **without pulling fuses** (that can wake or reset modules) —
   measure **mV drop across each fuse** with the meter, and use a fuse voltage-drop chart to
   convert to mA. The fuse showing a drop is the drawing circuit.
6. Common culprits: aftermarket accessories (dashcams, trackers, alarms), glovebox/boot
   lights, a module not sleeping because of CAN traffic from a faulty device, failing
   alternator diode.

## 5. CAN bus quick check (U-codes, multiple modules offline)
- Battery disconnected, measure resistance between CAN-High and CAN-Low at the DLC
  (pins 6 and 14): **~ 60 Ω** = two 120 Ω terminators intact; ~ 120 Ω = one terminator/branch
  missing; near 0 Ω = short.
- Scope CAN-H/CAN-L: mirror-image signals around ~ 2.5 V (high-speed CAN).

## Gotchas
- Disconnecting the battery to "reset" can lose radio codes, window learn and adaptations.
- Smart alternators deliberately run low voltage at times — use the manufacturer's test.
- Uncertain: thresholds are typical for 12 V passenger cars; hybrids/EVs (12 V DC-DC) and
  48 V systems differ — and high-voltage systems need HV training.

## Verify
- [ ] Battery charged and tested to its type/rating; terminals and grounds good.
- [ ] Charging voltage and ripple within spec under load.
- [ ] Cranking voltage drops measured on both positive and ground paths.
- [ ] Sleep current measured after full sleep; drawing circuit found via fuse voltage drop.
- [ ] Battery registration done where required; drain rechecked after the fix.
