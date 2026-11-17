---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.tailor-powertrain-reference-application
name: tailor-powertrain-reference-application
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [reference-application, powertrain-reference-application, model-reuse, variants, powertrain-blockset]
level: practitioner
status: verified
description: "Adapt a vendor reference application to your vehicle by swapping data, plant fidelity and controllers while keeping the test harness intact."
sources:
  - "https://www.mathworks.com/help/autoblks/powertrain-reference-applications.html"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tailor a reference application

1. Pick the closest reference (Powertrain Blockset lists conventional vehicle, HEV variants such as P0-P4, multimode and input power-split, and full EV applications; names vary by release) and copy to a fresh project; do not edit the shipped copy.
2. Replace parameters through a single data script: vehicle mass, CdA, tyre radius, gear ratios, maps, battery. Keep one `.m`/`.mat` per vehicle variant.
3. Keep plant and controller as separate referenced models so you can swap plant fidelity (mapped vs physics) without touching the controller.
4. Match signal names and units to your controller interface; add a bus object for the vehicle interface.
5. Run the reference's own test cycles first to prove nothing broke; then change one thing at a time.
6. Add logging for the KPIs you report.

**Gotchas:** silent unit mismatches (rpm vs rad/s); lookups that clamp.

## Verify
- [ ] Baseline run before edits reproduced after parameter swap with original data.
- [ ] Each change logged with a before/after KPI.
