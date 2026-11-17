---
id: computing-software.systems-network-administration.network-design.tia-606-cable-labeling
name: tia-606-cable-labeling
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, tia-606, cable-labeling, structured-cabling, port-map, documentation]
level: practitioner
status: draft
description: "Label cabling infrastructure per ANSI/TIA-606: identifier formats for spaces, racks, panels, ports and cables, label placement, and keeping records in sync."
sources:
  - https://tiaonline.org/products-and-services/standards/
  - https://www.fluke.com/en-us/learn/blog/cable-labeling/tia-606-c
  - https://www.brady.com/en-us/products/wire-and-cable-labels
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TIA-606 cable labelling

ANSI/TIA-606 (C/D) defines the administration standard for telecom infrastructure:
identifiers, labels and records.

## Identifier hierarchy (typical TIA-606 format)
| Element | Example | Meaning |
|---|---|---|
| Telecom space | `1A` | floor 1, room A |
| Rack / cabinet | `1A.AB05` | row AB, position 05 |
| Patch panel | `1A.AB05.22` | panel at U22 |
| Port | `1A.AB05.22:14` | port 14 |
| Horizontal link | `1A.AB05.22:14` printed at both ends | same ID on panel port and outlet |
| Backbone cable | `1A/2B-001` | cable 1 between spaces 1A and 2B |

Use the same identifier at both ends of every link and in the records. Choose a scheme
(class 1-4 by size of site) and apply it everywhere; consistency beats perfection.

## Labels
- Machine-printed, durable (self-laminating wrap-around for cables, flag labels for patch cords).
- Cable labels within 300 mm of each termination, readable without unplugging.
- Faceplates and panels labelled per port.
- Colour codes (TIA-606): orange demarc, green network connections, purple common equipment,
  white first-level backbone, grey second-level backbone, blue horizontal, brown inter-building,
  yellow auxiliary, red key telephone systems.

## Records
- Cable schedule (from/to, type, length, test result), panel maps, outlet maps on floor plans.
- Update in the same change ticket as any move/add/change; audit annually.
- Certification test reports filed by link ID.

## Verify
- [ ] Random audit of 20 links: label at both ends matches each other and the records.
