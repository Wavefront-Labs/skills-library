---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.bump-stops-and-jounce-limiting
name: bump-stops-and-jounce-limiting
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [bump-stop, jounce-bumper, rebound-stop, progressive-rate, travel-limit, hydraulic-bump-stop, springs-dampers]
level: practitioner
status: gated
description: "Specify bump stops and travel limits: engagement height, progressive rate, energy absorption, load paths and acoustic behaviour."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "bump-stop supplier documentation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bump stops and jounce limiting

1. Role: limit suspension travel at full jounce and provide a progressive added spring rate so end-stop contact is soft; also absorb energy in large inputs (potholes).
2. Types: microcellular polyurethane bump stops (progressive, quiet, common), rubber stops (cheaper), hydraulic bump stops (dissipate more energy, more complex).
3. Specify: engagement height from the design full-jounce stroke minus the stop's working stroke; the force-deflection curve up to the maximum design load (set by the load case for full compression such as 3-4 g vertical (gated: unconfirmed, source is paywalled or blocked), check with chassis load definition); the force at full compression must remain below the strut tower and arm strength.
4. Rate tuning: the added rate during the final 30-50 mm (gated: unconfirmed, source is paywalled or blocked) influences harshness and handling near the limit; engaging too early hurts ride; too late risks metal-to-metal contact.
5. Rebound stop: inside the damper; set rebound travel and spring seat limit.
6. Noise: surface contact sounds; use cups and shapes; test temperature effects (cold stiffening).
7. Verify with a rig and with durability roads (Belgian block, pothole) while measuring forces.

**Gotchas:** compression set (permanent deformation) over life; heat in repeated hits.

## Verify
- [ ] Measured force-deflection curve within the tolerance of the design curve.
- [ ] Pothole and full-jounce tests show no metal contact and loads below limits.
