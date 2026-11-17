---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.can-bus-wiring-and-termination-troubleshooting
name: can-bus-wiring-and-termination-troubleshooting
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, can-bus-troubleshooting, isobus, machine-networks, can-termination, can-high-low, bus-voltage, connector-corrosion]
level: practitioner
status: gated
description: "Troubleshoot ISOBUS and CAN bus faults: termination resistance, voltage levels, connector corrosion, wiring faults and node count, with multimeter and CAN-analyser steps."
sources:
  - "CAN bus, Wikipedia (https://en.wikipedia.org/wiki/CAN_bus)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CAN bus wiring and termination troubleshooting

**Goal:** find the wiring problem behind intermittent or dead ISOBUS and CAN communication.

## Facts
- ISO 11898-2 high-speed CAN uses a linear bus of twisted pair (CAN-H and CAN-L) terminated at each end with a 120 ohm resistor. ISO 11783 networks run at 250 kbit/s (gated: unconfirmed, source is paywalled or blocked).
- With power off, the resistance between CAN-H and CAN-L should read about 60 ohms (two 120 ohm resistors in parallel).
- With power on and the bus idle (recessive), CAN-H and CAN-L sit near 2.5 V (recessive level, typical transceiver value (gated: unconfirmed, source is paywalled or blocked)); during active communication CAN-H is driven toward 3.5 V and CAN-L toward 1.5 V when a node transmits a dominant bit (ISO 11898-2).

## Steps
1. **Visual**: check connectors for water, corrosion, bent or pushed-back pins, damaged cable, and chafed harness.
2. **Power and ground**: measure supply voltage (12 V or 24 V as applicable) and ground at the node; voltage drops indicate bad connections.
3. **Resistance test** with power off: about 60 ohms; about 120 ohms means one terminator missing; much lower means a short or an extra terminator; open means a break.
4. **Voltage test** with power on: both lines near 2.5 V idle; CAN-H or CAN-L stuck near 0 V or supply voltage indicates a short.
5. **Isolate** by disconnecting nodes one by one and re-measuring.
6. **CAN analyser or oscilloscope**: view waveforms and error frames; confirm bit timing and look for noise from alternators or poorly shielded devices.
7. **Node count and stub length**: too many nodes or long stubs degrade signal.

## Gotchas
- Aftermarket devices spliced into the bus can create reflections.
- Terminators are in specific connectors (tractor and implement end); do not add random ones.

## Verify
- [ ] After repair, bus voltage and resistance readings are as expected and error counters stay at zero.
