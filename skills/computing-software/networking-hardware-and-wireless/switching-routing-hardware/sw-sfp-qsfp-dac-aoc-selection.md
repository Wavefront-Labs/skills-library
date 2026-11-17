---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-sfp-qsfp-dac-aoc-selection
name: sw-sfp-qsfp-dac-aoc-selection
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [sfp-qsfp-optics, dac-aoc-cables, third-party-optics, sw-optics]
level: practitioner
status: draft
description: "Select transceivers and direct-attach cables by form factor, reach and platform support and read digital optical monitoring."
sources:
  - https://www.ieee802.org/3/
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Optics selection

- Form factors: SFP (1G), SFP+ (10G), SFP28 (25G), QSFP+ (40G), QSFP28 (100G), QSFP-DD/OSFP (200/400G). Match form factor and speed to the port, and breakout cables to the port group capability.
- DAC (copper) is cheap for under about 5-7 m in the rack; AOC for longer in-row runs; optics for structured cabling.
- Common types: SR (multimode, 850 nm), LR (singlemode, 10 km), ER, ZR (longer). BiDi uses one fibre strand with two wavelengths.
- Many switches check transceiver coding; third-party optics may need vendor-specific compatibility mode or an unsupported-transceiver command, and may affect support.
- DOM/DDM readouts (Tx/Rx power, temperature) diagnose dirty or failing links.

## Verify
- [ ] `show interface transceiver` (or equivalent) reports Rx power within the module's specified range.
