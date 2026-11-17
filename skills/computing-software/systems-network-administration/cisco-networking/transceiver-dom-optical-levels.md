---
id: computing-software.systems-network-administration.cisco-networking.transceiver-dom-optical-levels
name: transceiver-dom-optical-levels
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, nx-os, transceiver-dom, digital-optical-monitoring, ddm, optical-power, rx-power, tx-power, dbm, sfp, show-interfaces-transceiver, fiber-optic, light-levels, interface-errors]
level: practitioner
status: draft
description: "Use transceiver DOM/DDM readings to diagnose fibre links: show interfaces transceiver detail, reading dBm against thresholds, power budget maths and dirty vs failing optics."
sources:
  - https://www.cisco.com/c/en/us/support/docs/interfaces-modules/transceiver-modules/213467-understanding-digital-optical-monitoring.html
  - https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/data_sheet_c78-455693.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transceiver DOM optical levels

Most SFP/SFP+/QSFP optics report temperature, voltage, bias current, TX and RX power
(Digital Optical Monitoring, SFF-8472 / SFF-8636). It is the first check on any fibre link
with errors or flaps.

## Read it
```
show interfaces Te1/1/1 transceiver detail     ! IOS XE: values plus alarm/warn thresholds
show interfaces transceiver                    ! all ports, one line each
show inventory | i Te1/1/1 -A 1                ! PID/serial, e.g. SFP-10G-LR
```
NX-OS: `show interface e1/1 transceiver details`. Enable threshold syslogs on IOS XE with
`transceiver type all` then `monitoring`.

## Interpret
- Values are dBm. 0 dBm = 1 mW; -3 dB halves power; -10 dB = one tenth.
- Compare RX against the module's **receiver sensitivity** and the thresholds the switch
  prints (`++` high alarm, `+` high warn, `-` low warn, `--` low alarm).
- Typical ranges (check the datasheet for your PID):
  | Optic | TX dBm | RX sensitivity dBm |
  |---|---|---|
  | 10GBASE-SR | -7.3 to -1 | about -9.9 |
  | 10GBASE-LR | -8.2 to 0.5 | about -14.4 |
  | 1000BASE-LX | -9.5 to -3 | about -19 |
- RX far below expected with the far end's TX normal = loss in the path (dirty connector,
  bad patch, too many joins, wrong fibre type, bend). RX near/above overload on short LR/ER
  links = too hot; add an attenuator.
- TX low or bias current rising toward alarm = the optic is dying; replace it.

## Loss budget check
Expected RX = far-end TX - (fibre km x attenuation) - (connectors x 0.5 dB) - (splices x 0.1 dB).
SMF at 1310 nm is about 0.35 dB/km; MMF at 850 nm about 3 dB/km. If measured RX is 3+ dB
worse than the estimate, inspect and clean.

## Gotchas
- RX power `N/A` or `-40 dBm` = no light: broken strand, TX/RX swapped, far port shut, or
  the far optic is not lit.
- Third-party optics may report wrong thresholds or no DOM; trust the datasheet.
- Mismatched types (SR to LR, SMF optic on MMF) can link at short distances with errors.

## Verify
- [ ] Both ends' RX are inside the warn thresholds with margin (aim for 3 dB).
- [ ] After cleaning, RX improves and CRC stops incrementing.
- [ ] TX and bias are stable over a day in monitoring.
