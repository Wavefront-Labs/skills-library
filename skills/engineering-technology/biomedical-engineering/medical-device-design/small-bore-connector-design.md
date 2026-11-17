---
id: engineering-technology.biomedical-engineering.medical-device-design.small-bore-connector-design
name: small-bore-connector-design
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [iso-80369, small-bore-connector, misconnection, luer, enteral-connector]
level: practitioner
status: gated
description: "Design fluid connectors to prevent misconnection using the ISO 80369 small-bore series: application-specific connectors, tests and transition strategy."
sources: ["ISO 80369-1:2018 Small-bore connectors for liquids and gases in healthcare applications - General requirements", "ISO 80369-20:2015 Common test methods", "FDA, Additional Resources: Medical Device Connectors, https://www.fda.gov/medical-devices/medical-device-connectors/additional-resources-medical-device-connectors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Small-bore connector misconnection prevention

**Goal:** make wrong-route connections (for example enteral feed into an intravenous line) physically impossible by using application-specific connector designs.

## Concept
- ISO 80369 defines a family of dissimilar small-bore connectors, one design per application, so a connector for one use cannot mate with another. Examples include dedicated connectors for intravascular and hypodermic use (the Luer-compatible design), enteral, neuraxial, respiratory and limb-cuff inflation. Confirm part numbers and current editions before citing.
- Part 1 (ISO 80369-1:2018) sets general requirements; the common test methods (leakage, stress cracking, separation by axial load, unscrewing, overriding, non-interconnectability) are in Part 20 (ISO 80369-20:2015) and the requirement list is (gated: unconfirmed, source is paywalled or blocked). Parts named on the FDA connector resources page: -3:2016 enteral, IEC 80369-5:2016 limb cuff inflation, -6:2016 neuraxial, -7:2021 intravascular or hypodermic. The respiratory part (-2) was not on that page (gated: unconfirmed, source is paywalled or blocked).

## Design work
1. Identify each fluid path in the device and its clinical application, and pick the matching connector.
2. Dimensional control of mating features is tight; use gauges from the standard in design and incoming inspection.
3. Avoid adapters that defeat the safety purpose; if needed for transition, control them and label.
4. Materials: stress cracking with alcohol, lipids and solvents is a known risk; test.
5. Document in the risk file the misconnection hazard and design control.

## Verify
- [ ] Connector design conforms for the application, with test evidence.
- [ ] Mating counterparts in the intended system confirmed.
- [ ] Residual adapter and legacy-connector risks assessed.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
