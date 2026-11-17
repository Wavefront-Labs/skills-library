---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.harness-routing-and-protection
name: harness-routing-and-protection
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [harness-routing, wire-harness, cable-protection, grommet, clip-spacing, bend-radius, heat-shield, flex-fatigue, emc-separation, harness-design, corrugated-conduit]
level: practitioner
status: draft
description: "Route and protect a vehicle wiring harness: bend radius, clips, heat and abrasion protection, door pass-through flexing, drip loops, EMC separation and assembly practicality."
sources:
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
  - "Wiring harness design references and OEM routing guidelines (company-specific; confirm)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Harness routing and protection

## 1. Principles
Short, simple paths that avoid hazards, are easy to assemble, can be serviced, and stay put for the vehicle life. The harness is designed as a 2-D form board drawing from the 3-D routing, so the routing must be buildable in branches.

## 2. Mechanical routing
- **Bend radius:** keep a minimum bend radius relative to bundle outer diameter (OEM rule typically a multiple of the diameter; larger for coax, shielded and HV cable per supplier data).
- **Clip spacing and fixation:** clips to body studs or holes at regular intervals (an OEM-specified maximum span) and at both sides of every bend; fixation near connectors to remove load from the terminals.
- **Slack and service loops:** allow for tolerance and engine movement; check full range of movement of engine and suspension.
- **Clearance:** keep away from sharp edges, bolts, moving parts, steering and pedal assemblies, seat tracks; specify minimum distances and use grommets in panel holes.
- **Door and tailgate pass-throughs:** flexing harness section with a defined bend and twist motion, a sleeve or corrugated conduit, and fatigue testing for open-close cycles.

## 3. Environmental protection
- **Heat:** keep distance from exhaust and turbocharger; use heat shields, sleeves or reflective tape in hot zones; choose insulation temperature class for the local ambient.
- **Abrasion:** tape (PET, fabric, PVC with specified wear class), corrugated conduit, or woven sleeves where chafing is possible; felt tape against noise in the cabin.
- **Water and drip loops:** route connectors with the opening downward; add drip loops before connectors and avoid water traps in conduit; use drain holes.
- **Fluids and chemicals:** chemical-resistant sheathing near oil, fuel and brake fluid.

## 4. EMC and safety separation
Separate high-current or noisy lines (inverter phase cables, HV, injectors) from sensitive signals and from antennas; use shielded or twisted pairs; ground shields at defined points; keep HV orange cables in protected channels away from crush zones (see HV post-crash).

## 5. Assembly and service
Define clip and tape instructions, branch lengths, labelling, and connector retention so a worker can install without damage; consider repair access and common service tasks.

## 6. Validation
Digital mock-up swept envelopes; buck or prototype fit; vibration and thermal tests; flex-life tests for doors; chafe and clip pull-out tests.

## Verify
- [ ] Bend radii, clip spacing and clearances checked on digital and physical mock-ups.
- [ ] Hot-zone and abrasion protection specified from measured temperatures.
- [ ] Flex zones validated by cycle testing.
- [ ] EMC and HV separation rules satisfied.
