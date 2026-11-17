---
id: computing-software.firmware-embedded-development.device-driver-development.can-transceivers-and-termination
name: can-transceivers-and-termination
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-termination, can-bus, can-transceiver, split-termination, stub-length, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Get the CAN physical layer right: 120 Ohm termination at both ends (measure 60 Ohm), split termination, transceiver mode pins, stub lengths and scope levels."
sources:
  - https://www.ti.com/lit/an/slla270/slla270.pdf
  - https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transceivers and bus termination

Most "CAN doesn't work" bring-up problems are physical: missing termination, a transceiver left
in a silent mode, or CANH/CANL swapped.

## Termination
- High-speed CAN (ISO 11898) uses a twisted pair with 120 Ohm characteristic impedance,
  terminated with 120 Ohm resistors at both ends of the bus. ISO 11898 advises against putting the
  terminating resistor on a node, because the bus loses termination if that node is disconnected.
- With power off, measure between CANH and CANL. Two 120 Ohm resistors in parallel read about
  60 Ohm; about 120 Ohm means one terminator is missing; about 40 Ohm means three; open means none.
- Unterminated lines show reflected waves that build up on the signal (TI SLLA270 figure 7).
- **Split termination**: two resistors of about 60 Ohm (matched, 1 percent) with a coupling
  capacitor from the midpoint to ground, which filters high-frequency noise and improves EMC. TI
  gives 4.7 nF as a typical value for high-speed CAN (3 dB point at 1.1 Mbps, rate dependent).
  Transceivers with a Vref or Vsplit pin use it to stabilise the common-mode bus voltage.

## Topology and stubs
ISO 11898 recommends a maximum unterminated stub length of 0.3 m at 1 Mbps (a maximum bus length
of 40 m at 1 Mbps and 30 nodes). TI's rule: keep a stub under one third of the line's critical
length, where critical length is where the down-and-back propagation delay equals the driver
transition time; slower driver slew rate or lower bit rate allows longer stubs.

## Transceiver pins (NXP TJA1051 as the example)
| Pin | Behaviour |
|---|---|
| S | LOW selects Normal mode; HIGH selects Silent mode (transmitter disabled, receiver still works). S has an internal pull-down, so a floating S gives Normal mode |
| EN | TJA1051T/E only: LOW selects Off mode, bus pins floating |
| VIO | TJA1051T/3 and TJA1051TK/3 only: connect to the microcontroller supply so TXD, RXD and S use its logic levels. Versions without VIO tie it to VCC (5 V levels) |
| TXD | internal pull-up to VIO. TXD dominant time-out: if TXD stays LOW longer than tto(dom)TXD (0.3 to 5 ms, 1 ms typical) the transmitter releases the bus |

Other transceivers differ; read your part's data sheet for the mode pins and defaults.

## Bring-up order
1. Controller internal loopback mode, if your controller has one: checks configuration and bit
   timing without a bus.
2. Two nodes, both terminated, same bit rate: send and acknowledge.

## Scope checks (TJA1051 data sheet, VCC 5 V, bus loaded with 50 to 65 Ohm)
Dominant: CANH typically 3.5 V (2.75 to 4.5 V), CANL typically 1.5 V (0.5 to 2.25 V), differential
1.5 to 3 V. Recessive: both lines typically near 0.5 VCC, differential within 50 mV. Rounded
recessive edges or ringing point at termination problems.

## Verify
- [ ] 60 Ohm measured with power off.
- [ ] Transceiver mode pin driven or defaulted to normal mode.
- [ ] Error counters stay at 0 under traffic between at least two nodes.

## Checked
2026-11-09. Read: TI SLLA270 (ISO 11898 120 Ohm termination at both ends, node-mounted RL
warning, split termination with two 60 Ohm resistors and 4.7 nF, 0.3 m stub at 1 Mbps, one-third
critical length rule) and the NXP TJA1051 data sheet Rev 9 (operating modes, S and EN pins,
internal pull-downs, VIO, TXD dominant time-out 0.3 to 5 ms, CANH and CANL levels). Removed: the
ISO 11898-2 and iso.org source (paywalled, not read), stub lengths at 500 kbit/s, CiA 601, CAN FD
sensitivity, TCAN1042V and the claim that many transceivers power up in standby, RXD wiring
advice, loopback register names, the lone-node error counter explanation.
Method: docs-checked 2026-11-09 against TI SLLA270 and the NXP TJA1051 data sheet Rev 9.
