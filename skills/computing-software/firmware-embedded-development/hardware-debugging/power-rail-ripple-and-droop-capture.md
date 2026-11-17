---
id: computing-software.firmware-embedded-development.hardware-debugging.power-rail-ripple-and-droop-capture
name: power-rail-ripple-and-droop-capture
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [oscilloscope, power-rail-measurement, ripple, droop, brownout-capture, ac-coupling, radio-tx-burst, decoupling, firmware-embedded-development]
level: advanced
status: draft
description: "Measure supply ripple and load-step droop with a scope to explain resets and radio failures: AC coupling, 20 MHz limit, triggering on the dip, and correlating with firmware events."
sources:
  - https://www.tek.com/en/documents/application-note/measuring-power-supply-ripple-and-noise
  - https://www.keysight.com/us/en/assets/7018-06784/application-notes/5992-3165.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power rail ripple and droop capture

**Goal:** prove or rule out the supply as the cause of random resets, brown-outs, ADC noise
or Wi-Fi/cellular failures.

## Setup for ripple (mV-level noise on a DC rail)
- **AC coupling** on the channel, or DC with offset, at 5-20 mV/div.
- **20 MHz bandwidth limit** on (the conventional ripple spec bandwidth) unless chasing RF.
- Probe 1x or a dedicated power-rail probe (low noise, high offset range); 10x probes add
  noise floor at mV scales.
- Ground spring at the decoupling capacitor of the device in question, not at the regulator.

## Setup for droop (load step, radio burst)
- DC coupling, offset the trace to the nominal voltage (e.g. 3.3 V offset, 100 mV/div).
- **Trigger on the dip**: edge trigger falling at e.g. 3.1 V, or runt/window trigger, normal
  (not auto) mode, single shot.
- Second channel on a **firmware marker GPIO** set just before the event (TX start, motor
  enable, flash erase) to correlate timing.
- Optional third channel: current via a shunt + differential probe or current probe.

## What the numbers mean
- MCU brown-out thresholds (BOR/BOD) are typically 1.7-2.9 V configurable; a dip below that,
  even for microseconds, resets the chip. Compare dip minimum to the configured BOR level.
- ESP32 Wi-Fi TX and cellular modems (2 A bursts for GSM) cause the classic "brownout detector
  was triggered" resets on weak supplies, thin USB cables and too-small bulk capacitors.
- Coin cells: internal resistance 10-30 ohm, 15 mA pulse = 0.15-0.45 V drop; worse when cold.

## Fixes (in the order usually cheapest)
- Bulk capacitance near the load (100-470 uF for radio modules, low-ESR).
- Shorter/thicker supply wiring; avoid USB cables with thin power conductors.
- Regulator with adequate transient response / current headroom.
- Firmware: stagger high-current events (don't start Wi-Fi TX while the motor starts), lower
  TX power, raise CPU clock only when needed.
- Configure BOR level sensibly: too high resets on harmless dips, too low lets flash writes
  happen at unsafe voltages.

## Verify
- [ ] Worst-case event captured with min voltage annotated and compared to BOR threshold.
- [ ] After fix, 1000 repetitions of the event without reset.
