---
id: computing-software.firmware-embedded-development.hardware-debugging.differential-probing
name: differential-probing
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [differential-probe, high-side-measurement, can-bus-probing, rs485-probing, usb-signal, cmrr, ground-loop, oscilloscope, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Probe floating or differential signals safely: no floating scope grounds, active differential probes, CMRR, CAN/RS-485 and high-side shunt measurements."
sources:
  - https://www.tek.com/en/documents/primer/oscilloscope-basics
  - https://www.ti.com/lit/an/slla270/slla270.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Differential probing

## Why
A passive probe's ground clip is tied to the scope chassis and mains earth. Clipping it to a node
that is not ground (high-side shunt, half-bridge switch node, mains-referenced circuit) shorts that
node to earth: destroyed parts, blown traces, or worse. Never "float" the scope by removing earth.

## Options
- **Active differential probe:** two high-impedance inputs, output = V+ - V-. Specify by
  bandwidth, differential range, common-mode range and CMRR at the frequency of interest.
- **High-voltage differential probe** (1000 V+ CAT ratings) for mains/inverter work.
- **Two passive probes + math (CH1-CH2):** acceptable for slow signals with low common-mode;
  CMRR is poor (~20-30 dB at high frequency) because the two channels are not matched.
- **Isolated-channel scopes** or battery-powered handheld scopes for floating measurements.

## Firmware-relevant measurements
- **CAN:** probe CANH-CANL differentially; recessive ~0 V, dominant ~2 V. Check bit timing,
  ringing at the sample point, and termination (should read 60 ohm between H and L unpowered).
- **RS-485:** A-B differential; failsafe biasing keeps idle > +200 mV. Idle near 0 V means missing
  bias resistors, garbage bytes on line release.
- **USB FS/HS, Ethernet:** need >= 1-3 GHz differential probes for eye analysis; for firmware work,
  usually decode with a protocol analyser instead.
- **High-side current shunt:** differential across the shunt; common mode is the rail voltage.
- **Gate drive / switch nodes:** high common-mode slew (dV/dt) demands high CMRR; otherwise the
  "signal" is mostly common-mode feedthrough.

## Gotchas
- Check CMRR at the switching frequency, not DC; it falls with frequency.
- Keep both input leads the same length and twisted.
- Differential probes have offset and need warm-up; zero before small measurements.

## Verify
- [ ] Shorting both inputs to the same node shows ~0 V with the circuit running (residual common-mode).
- [ ] Measured CAN dominant/recessive levels match the transceiver datasheet.
