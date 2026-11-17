---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.frontal-impact-regulations
name: frontal-impact-regulations
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [frontal-regulation, fmvss-208, un-r94, un-r137, offset-deformable-barrier, full-width-barrier, regulatory-crash]
level: practitioner
status: gated
description: "Map frontal-impact regulatory tests (FMVSS 208, UN R94, UN R137): barrier, speed, dummy and measurements, with a reminder to confirm current texts."
sources:
  - "FMVSS 208 (nhtsa.gov), UN Regulations 94 and 137 (unece.org); confirm the current consolidated texts and amendments"
  - "https://www.law.cornell.edu/cfr/text/49/571.208"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Frontal impact regulations

This is a planning map; confirm test speeds, dummies, criteria and applicability in the current regulation text and by market.

- **FMVSS 208 (US):** occupant crash protection. Belted full-width rigid-barrier test at any speed up to and including 56 km/h (35 mph) (S14.4), with 50th-percentile male and 5th-percentile female Hybrid III dummies (checked in 49 CFR 571.208); unbelted and out-of-position provisions for airbag aggressiveness; injury criteria include HIC, chest deflection and acceleration, neck (Nij), and femur load.
- UN R94 and R137 details below are unconfirmed (gated: unconfirmed, source is paywalled or blocked).
- **UN R94 (ECE):** offset frontal test into a deformable barrier at 40% overlap at about 56 km/h with Hybrid III 50th male in the front seats; assesses head, neck, chest, femur and tibia criteria, steering wheel displacement and door opening.
- **UN R137:** full-width frontal impact into a rigid barrier at about 50 km/h with belted dummies, adding restraint-focused load cases; check current text.
- Design implications: the full-width test needs stiff structure and early airbag firing; the offset test needs strong load-path and occupant-compartment integrity; both need belt load limiters tuned to chest deflection.
- Tools: sled tests for restraint tuning, full-vehicle CAE and prototype crashes for homologation.
- Certification is by approved test labs/self-certification regimes (type-approval in ECE, self-certification in US).

**Gotchas:** designing to consumer ratings only; regulatory tests still must pass.

## Verify
- [ ] Applicable regulation list with editions recorded for each target market.
- [ ] Each test configuration mapped to CAE and physical test plans.
