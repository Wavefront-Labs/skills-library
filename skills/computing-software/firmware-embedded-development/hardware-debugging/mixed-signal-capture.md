---
id: computing-software.firmware-embedded-development.hardware-debugging.mixed-signal-capture
name: mixed-signal-capture
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [mixed-signal, mso, analog-digital-correlation, logic-analyzer-analog, trigger-on-protocol, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Correlate analog and digital signals in one capture (MSO or analog logic analyser): rail droop vs bus traffic, ADC timing, PWM vs current, sample-rate trade-offs."
sources:
  - https://support.saleae.com/
  - https://www.tek.com/en/documents/primer/oscilloscope-basics
  - https://www.keysight.com/us/en/assets/7018-06483/application-notes/5992-0294.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mixed-signal capture

**Use when:** the question is "what was the firmware doing when the analog thing happened" —
brownout during a radio burst, ADC sample taken mid-switching edge, motor current vs PWM.

## Instruments
- **MSO** (scope with 8-16 digital channels): best analog fidelity and triggering; short memory.
- **Logic analyser with analog inputs** (Saleae Pro, DSLogic U3Pro analog variants): long captures,
  analog at only a few MS/s and ~5 MHz bandwidth; fine for rails and currents, not edges.
- Two instruments: share a trigger (scope trigger-out -> LA trigger-in) and accept tens of ns skew.

## Firmware cooperation
Add marker GPIOs: set a pin at the start of an operation (ADC conversion, radio TX, flash erase) and
clear it after. Digital channels then label the analog trace, and you can trigger on the marker.

## Setups
- **Rail droop vs activity:** analog on the rail (AC coupled, 20 MHz BW limit), digital on radio
  enable / SPI CS. Trigger on the analog falling below threshold; read which digital event lined up.
- **ADC sample timing:** analog on the ADC input, digital on the conversion-start marker; check the
  sample instant avoids PWM edges and settling.
- **Current vs firmware state:** current probe or shunt amplifier on analog, state GPIOs on digital;
  integrate per state to build an energy budget.
- **Protocol-triggered analog:** trigger on an I2C address/SPI byte (MSO protocol trigger) and
  inspect the analog edges of that exact transaction.

## Sample-rate rules
- Digital: 4-10x the fastest edge rate you care about (10x for timing measurement).
- Analog on an LA: enabling more channels lowers per-channel rate on USB devices; turn off unused
  channels.
- Use the instrument's deep memory or streaming for events that happen once a minute.

## Gotchas
- Ground everything at one point; a long LA ground lead adds noise to the analog channels.
- MSO digital thresholds default to TTL (1.4 V); set for 1.8 V logic.
- Analog channels on LAs are often 1 MOhm, 10x attenuation not available; mind input range (+/-10 V).

## Verify
- [ ] Marker GPIO edges line up with the analog event within the stated skew.
- [ ] Conclusion reproducible across multiple triggered captures.
