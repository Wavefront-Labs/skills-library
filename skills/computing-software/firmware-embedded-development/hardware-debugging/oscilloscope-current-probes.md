---
id: computing-software.firmware-embedded-development.hardware-debugging.oscilloscope-current-probes
name: oscilloscope-current-probes
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [current-probe, hall-effect-probe, degauss, inrush-current, motor-current, current-shunt-scope, oscilloscope, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Measure current on a scope: Hall-effect clamp probes (degauss, zero, sensitivity), shunt plus amplifier options, inrush and motor/LED driver currents."
sources:
  - https://www.tek.com/en/documents/primer/oscilloscope-basics
  - https://www.tek.com/en/datasheet/current-probes
  - https://www.keysight.com/us/en/product/N2820A/high-sensitivity-current-probe.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Current probes

## Probe types
- **AC/DC Hall-effect clamp** (Tek TCP0030A, Keysight N2893A): DC to 50-120 MHz, ranges 5-30 A,
  noise ~mA. Non-intrusive; you thread a wire through the jaw.
- **AC-only current transformer:** cheap, no DC, good for switching ripple.
- **Shunt + differential/current-sense amplifier** (Keysight N2820A, or your own INA/MAX9938 on a
  test fixture): microamp to amp ranges with high dynamic range; intrusive.
- **Dedicated power analysers** (Joulescope, PPK2, Otii) for sleep current; scopes with clamp
  probes cannot resolve microamps.

## Using a clamp probe
1. Warm up 20 minutes; Hall sensors drift.
2. Close jaw with nothing inside, **degauss** (button on the probe/scope), then **zero/balance**.
3. Match the scope channel unit to amps (smart probes do this). Check the sensitivity range.
4. Orientation: arrow in direction of conventional current.
5. Increase sensitivity for small currents by looping the wire N turns through the jaw; divide by N.

## Firmware uses
- **Inrush and brownout:** current into the board at power-on or when a load switch enables a
  radio; check it against regulator current limit and battery peak capability.
- **Motor / solenoid drivers:** verify PWM current ripple, regenerative spikes and stall current
  detection thresholds used by firmware.
- **LED/heater drivers:** confirm duty cycle actually produces the expected average.
- **Power state transitions:** trigger on a firmware marker GPIO and observe current settling.

## Gotchas
- DC offset drifts with temperature and after measuring large currents (magnetised core): degauss
  again before small measurements.
- Max current x frequency derating: high currents at high frequency overheat the probe.
- The probe's propagation delay differs from voltage probes by tens of ns; deskew before computing
  power (V x I).
- Clamping over a ribbon cable measures the net current of all conductors.

## Verify
- [ ] Probe reads ~0 A with no conductor after degauss.
- [ ] Known resistive load current matches a DMM within probe accuracy.
