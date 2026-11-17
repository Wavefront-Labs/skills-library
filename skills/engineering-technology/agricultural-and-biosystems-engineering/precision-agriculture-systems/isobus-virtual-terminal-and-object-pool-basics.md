---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.isobus-virtual-terminal-and-object-pool-basics
name: isobus-virtual-terminal-and-object-pool-basics
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, virtual-terminal, isobus, machine-networks, iso-11783, object-pool, universal-terminal, aef-conformance]
level: practitioner
status: gated
description: "Understand the ISOBUS virtual terminal: universal terminal role, object pool upload, compatibility checks, language and version issues, and basic troubleshooting."
sources:
  - "ISO standards catalogue (https://www.iso.org)"
  - "AEF - Agricultural Industry Electronics Foundation (https://www.aef-online.org)"
  - "Wikipedia, ISO 11783 part list (https://en.wikipedia.org/wiki/ISO_11783)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ISOBUS virtual terminal and object pool basics

**Goal:** make an implement's user interface appear correctly on any compatible tractor display.

## Concepts
- ISO 11783 (Tractors and machinery for agriculture and forestry: serial control and communications data network) defines a common CAN-based network for tractors and implements (ISOBUS). The **Universal Terminal (UT)** or **Virtual Terminal (VT)** in the tractor displays an implement's user interface, which the implement uploads as an **object pool** (a set of defined screens, buttons and data fields) when it connects.
- The tractor display must support the VT version needed by the implement (VT version 3 or 4 and later features; confirm the version numbers in ISO 11783-6 (gated: unconfirmed, source is paywalled or blocked)); older displays may not show all functions.
- Compatibility is tested through the Agricultural Industry Electronics Foundation (AEF) conformance testing and an AEF database of certified products (https://www.aef-online.org); use it to check that a tractor, implement and display work together.

## Practical use
1. Power up the tractor, connect the ISOBUS cable, and wait for the pool to load (first-time upload may take a minute; later loads are cached).
2. Choose the language and units in the implement's setup; the pool may need to be reloaded after changes.
3. If the screen is blank or incomplete: check the VT version, available memory, cable connection and terminators, and update the display or implement software.
4. Auxiliary inputs (joystick or AUX-N assignment) are mapped through the VT; confirm the mapping for each implement.

## Gotchas
- Different manufacturers' displays vary in how they render the same pool.
- Not all implement functions are available through UT only; some need task controller or proprietary tools.

## Verify
- [ ] Implement displays fully, and controls respond; AEF certification of the combination is checked before purchase.
