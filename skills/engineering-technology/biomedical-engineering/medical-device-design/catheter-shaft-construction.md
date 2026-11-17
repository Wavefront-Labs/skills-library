---
id: engineering-technology.biomedical-engineering.medical-device-design.catheter-shaft-construction
name: catheter-shaft-construction
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [catheter-shaft, catheter-design, minimally-invasive, braided-shaft, coil-reinforced, extrusion, durometer]
level: advanced
status: gated
description: "Choose catheter shaft construction: single and multi-lumen extrusion, braid and coil reinforcement, durometer zones and tip forming to balance push, torque and kink."
sources: ["https://www.iso.org/standard/76494.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Catheter shaft construction

**Goal:** a shaft that transmits push and torque to the tip, tracks around bends and does not kink, within a small outer diameter.

Engineering guidance. Standards cited should be checked for the current edition and for applicability to your device class.

## Building blocks
- **Extruded polymer tubes** (polyamide, Pebax-type polyether block amide, polyurethane, PTFE liners). Lumen shapes (round, D, crescent) are set by the die and mandrel; multi-lumen extrusions combine guidewire, inflation and fluid paths.
- **Layered build:** inner liner (low friction, often PTFE etched for bonding) / reinforcement / outer jacket. The jacket is reflowed (heat-shrink FEP carrier) over the reinforcement.
- **Reinforcement:** braid (stainless wire or fibre flat or round, PPI sets stiffness and torque), coil (flexibility with crush and kink resistance, less push), or hypotube proximally for pushability.
- **Durometer zones:** proximal stiff (e.g. high Shore D) to distal soft (e.g. Shore 25-35D) with transitions; a blend or step transition should avoid kink points.
- **Tip:** atraumatic soft tip, radiopaque marker band (platinum-iridium or tungsten-filled polymer), laser or heat-bonded.

## Design trade-offs
- Higher braid PPI increases torque transmission and stiffness; low PPI is flexible but may wind up (gated: unconfirmed, source is paywalled or blocked).
- Thin walls help the inner lumen size but reduce kink and burst margin.
- Use stiffness transitions that are long enough to avoid a hinge.

## Verify
- [ ] Kink, torque response and tensile bond to ISO 10555-1:2023 (current edition, iso.org/standard/76494.html; the 2013 edition is withdrawn) and your inputs.
- [ ] Burst or leak tests where lumens carry pressure.
- [ ] Bench tracking in an anatomical model (see trackability-pushability-testing).
