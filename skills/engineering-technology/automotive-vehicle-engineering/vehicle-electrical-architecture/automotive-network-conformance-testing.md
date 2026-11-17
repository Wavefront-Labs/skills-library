---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.automotive-network-conformance-testing
name: automotive-network-conformance-testing
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [network-testing, conformance-testing, can-conformance, iso-16845, opena-tc8, ethernet-tc8, restbus-simulation, canoe, bit-timing, sample-point, bus-off, physical-layer-test]
level: practitioner
status: gated
description: "Test in-vehicle networks: CAN and CAN FD physical and protocol conformance, Ethernet TC8-style tests, restbus simulation, timing and network management verification."
sources:
  - "ISO 11898 series and ISO 16845 CAN conformance test standards (confirm parts); OPEN Alliance automotive Ethernet test specifications (https://opensig.org); ISO 17987 (LIN); confirm current editions"
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Automotive network conformance testing

## 1. Layers to test
1. **Physical layer:** bus voltage levels, bit timing and sample point, edge shape and ringing, termination (about 60 ohm between CAN-H and CAN-L when unpowered with two 120 ohm terminators: two 120 ohm in parallel, computed), loop delay for CAN FD transmitter delay compensation, common-mode noise, wake-up behaviour. Use oscilloscope with CAN decode and eye diagram (especially for CAN FD data-phase at higher rates) and network analyser for Ethernet.
2. **Data link and protocol conformance:** test that a node's controller follows the protocol: error handling, arbitration, bus-off and recovery behaviour. Standardised test suites exist (ISO 16845 parts for CAN controllers (part numbers (gated: unconfirmed, source is paywalled or blocked)); LIN conformance for LIN nodes; confirm which parts apply). Ethernet ECUs use test specifications from industry groups (such as OPEN Alliance TC8 for ECU and switch tests: IP stack, PHY, switch behaviour, SOME/IP service discovery).
3. **Network layer and application:** transport protocols (ISO-TP), diagnostics (UDS), network management (sleep, wake, NM timeouts), signal timing and plausibility.

## 2. Restbus simulation
Simulate all missing ECUs from the communication database (DBC/ARXML) with tools such as CANoe, so each ECU under test receives realistic traffic including the periods and counters. Add fault cases: missing frame, wrong checksum or counter, babbling node, delayed messages, wrong DLC.

## 3. Timing verification
Measure cycle time and jitter of each message on the bus; compare with the database specification (tolerance, for example plus or minus a small percentage); measure bus load (see bus load analysis) and latency across the gateway; check that low-priority messages meet deadlines under peak load.

## 4. Robustness tests
Error injection (bit errors, dominant stuck), bus-off recovery timing, short to ground or battery on bus lines and system response, termination missing or doubled, EMC injections in combination (see EMC test methods), and temperature and supply voltage extremes.

## 5. Records
Test specification linked to requirements, versioned databases, trace logs (BLF/MDF) stored with reports, defect tracking. Automate regression runs in HIL or bench farms.

## Verify
- [ ] Physical layer measurements include sample point and bit timing at worst case.
- [ ] Applicable conformance test suite identified and passed.
- [ ] Restbus simulation covers faulty and missing messages.
- [ ] Timing and bus load measured against the database.
