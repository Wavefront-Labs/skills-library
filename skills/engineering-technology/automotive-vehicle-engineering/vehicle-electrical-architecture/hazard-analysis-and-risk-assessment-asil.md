---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.hazard-analysis-and-risk-assessment-asil
name: hazard-analysis-and-risk-assessment-asil
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [hara, asil, iso-26262, severity-exposure-controllability, hazard-analysis, safety-goal]
level: practitioner
status: gated
description: "Perform HARA under ISO 26262: situations, hazardous events, S/E/C ratings, ASIL determination, safety goals, and the review practice around ratings."
sources:
  - "ISO 26262-3:2018 clause on hazard analysis and risk assessment; confirm the edition and the OEM's rating guidelines"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hazard analysis and risk assessment (ASIL)

This is professional practice guidance; the functional safety process is defined by ISO 26262 and the assessor/safety manager of your organisation. It does not replace them.

1. Item definition: functions, interfaces, operating modes, known hazards, assumptions.
2. Situation analysis: list operating scenarios (speed, road, traffic, driver state) and combine with malfunctioning behaviours (loss, unintended, too much/too little, wrong timing, wrong direction) from the item's functions to build hazardous events.
3. Rate each hazardous event: **Severity** S0-S3 (injuries, using the AIS scale (gated: unconfirmed, source is paywalled or blocked)), **Exposure** E0-E4 (probability of the situation), **Controllability** C0-C3 (gated: unconfirmed, source is paywalled or blocked) (ability of the driver or others to avoid harm).
4. ASIL from the table in ISO 26262-3 (gated: unconfirmed, source is paywalled or blocked): in practice, S3/E4/C3 = ASIL D; summing the class numbers works: sum of 10 = D, 9 = C, 8 = B, 7 = A, lower = QM. Example: S3, E4, C2 gives ASIL C; S3, E3, C3 gives ASIL C.
5. Safety goals: one for each hazardous event or grouped events, with the ASIL of the highest event and a safe state.
6. Review: use consistent rating guidelines across the company; independent review; record rationale for E and C choices.
7. Update when the item changes.

**Gotchas:** rating exposure from the wrong scenario sample; under-rating controllability for a system that fails silently.

## Verify
- [ ] Each hazardous event has S, E and C with a written rationale and the correct ASIL.
- [ ] Safety goals traced to events and reviewed by an independent person.
