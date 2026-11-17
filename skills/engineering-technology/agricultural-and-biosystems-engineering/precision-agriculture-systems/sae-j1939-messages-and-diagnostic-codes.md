---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.sae-j1939-messages-and-diagnostic-codes
name: sae-j1939-messages-and-diagnostic-codes
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, j1939, isobus, machine-networks, pgn, spn, dm1, fmi, diagnostic-trouble-code]
level: practitioner
status: gated
description: "Read SAE J1939 traffic and fault codes: PGN and SPN structure, DM1 and DM2 messages, FMI meanings and a safe logging setup with a CAN adapter and open-source tools."
sources:
  - "SAE J1939 overview, Wikipedia (https://en.wikipedia.org/wiki/SAE_J1939)"
  - "CSS Electronics, J1939 explained (https://www.csselectronics.com/pages/j1939-explained-simple-intro-tutorial)"
  - "SAE J1939 standards family (paywalled; https://www.sae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SAE J1939 messages and diagnostic codes

**Goal:** read machine data and fault codes from engines and controllers on heavy equipment.

## Structure
- J1939 uses 29-bit CAN identifiers carrying a priority, **parameter group number (PGN)** and source address. Signals within a PGN are defined by **suspect parameter numbers (SPN)**; ISO 11783 reuses this for agricultural machines.
- Examples: PGN 61444 (electronic engine controller 1) carries engine speed (SPN 190 (gated: unconfirmed, source is paywalled or blocked)); DM1 (PGN 65226, hex FECA) is the broadcast of active diagnostic trouble codes; DM2 (PGN 65227, hex FECB) lists previously active codes (the hex-to-decimal conversion is computed; the DM1/DM2 assignment is from J1939-73 (gated: unconfirmed, source is paywalled or blocked)).
- A fault code is **SPN + FMI** (failure mode identifier). Examples of FMI: 3 voltage above normal or shorted high, 4 voltage below normal or shorted low, 5 current below normal or open circuit, 31 condition exists (gated: unconfirmed, source is paywalled or blocked). The SPN and FMI meanings are in the standard (SAE J1939-73) and the engine maker's service manual.

## Reading data safely
1. Use a CAN interface adapter and a tool such as python-can, can-utils (candump) or an open-source analyser; connect to the diagnostic connector, listen only (no transmit) to avoid disturbing the machine.
2. Set the bus speed to match the machine (J1939 specifies 250 kbit/s in J1939-11 and -15 and 500 kbit/s in J1939-14; ISO 11783 networks use 250 kbit/s (gated: unconfirmed, source is paywalled or blocked)).
3. Decode the PGNs with a J1939 database file; log engine speed, fuel rate and DM1.
4. Interpret DM1 by SPN/FMI with the manufacturer's service information; clearing codes is done with the maker's tools.

## Gotchas
- Sending messages on a live machine can cause unintended actions or faults: do not transmit unless you know the effect.
- Warranty and safety: read, do not modify, ECU parameters without authorisation.

## Verify
- [ ] Logged engine speed matches the tachometer, and a known fault (such as an unplugged sensor) appears as an expected SPN and FMI.
