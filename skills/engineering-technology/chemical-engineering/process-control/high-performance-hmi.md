---
id: engineering-technology.chemical-engineering.process-control.high-performance-hmi
name: high-performance-hmi
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-alarms-and-interface, high-performance-hmi, high-performance-hmi, operator-display, situational-awareness]
level: practitioner
status: gated
description: "Design a high-performance operator display: grey-scale base, colour for abnormal only, trends, hierarchy and situational awareness."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
  - "https://www.isa.org/products/ansi-isa-101-01-2015-human-machine-interfaces-for"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High performance hmi

**Goal:** Design a high-performance operator display: grey-scale base, colour for abnormal only, trends, hierarchy and situational awareness.

## Steps
1. Use a display hierarchy: overview of the unit, process area displays, detail and diagnostic displays; the overview shows the key performance and the abnormal conditions.
2. Use a neutral (grey) background with muted equipment and use colour only for abnormal conditions and alarms so it attracts attention.
3. Show analogue values with the context: range bars, targets and short trend sparklines instead of numbers alone.
4. Standardise the symbols and the navigation; avoid decorative graphics.
5. Test with operators and make the changes before the roll-out. ISA-101 (ANSI/ISA-101.01-2015, Human Machine Interfaces for Process Automation Systems) covers HMI; confirm the current edition. The grey-scale and colour-for-abnormal practice follows ISA-101 and high-performance HMI guidance (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Copying the P&ID as a display is the usual poor design.
- Colour blind users should be considered.

## Verify
- [ ] Abnormal states are visible on the overview.
- [ ] Operators have reviewed the displays.
