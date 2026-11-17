---
id: engineering-technology.aerospace-engineering.aircraft-structures.structural-compliance-documentation
name: structural-compliance-documentation
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, certification-basis, airworthiness, compliance-reports, certification-plan, stress-report, means-of-compliance, special-conditions]
level: practitioner
status: draft
description: "Prepare structural compliance reports that regulators can accept: certification plan, loads and stress reports, test-analysis correlation and the traceable margin tables."
sources:
  - "14 CFR Part 21 (certification procedures)"
  - "EASA Part 21"
  - "FAA and EASA certification guidance on compliance documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Structural compliance documentation

**Goal:** evidence a certifying authority can review quickly.

## Documents
- **Certification plan (or compliance programme):** certification basis, the paragraph-by-paragraph means of compliance, test plans, schedule.
- **Loads report:** load cases, derivation, tools, validation (flight-loads-model correlation with wind-tunnel or flight data).
- **Stress and strength reports:** methods, materials allowables source (see allowables skills), margins of safety table, critical locations.
- **Test plans and reports:** static test, fatigue test, component tests; deviations documented.
- **Fatigue and damage tolerance report:** inspections, thresholds, intervals, limit of validity.
- **Configuration control:** report references the drawing and model revisions.

## Practice
1. Each report states scope, inputs (with revision), method, results, conclusion and limitations.
2. Use a stable margin table format with load case ID, element, failure mode, margin.
3. Close out issues raised by the authority and record agreements (issue papers or certification review items).
4. Special conditions apply when the regulation lacks adequate standards for a novel feature; the application and rule-making process are under Part 21 and the authority.

## Gotchas
- Late test changes without re-analysis break traceability.
- Different software versions between draft and final analysis produce unexplained deltas.

## Verify
- [ ] Margin tables reproduce from the stated inputs by an independent check.
