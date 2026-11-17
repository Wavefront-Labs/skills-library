---
id: engineering-technology.biomedical-engineering.device-verification-validation.design-reviews
name: design-reviews
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [design-review, design-controls, design-and-development-planning, design-reviews, phase-gate, independent-reviewer, action-items]
level: practitioner
status: draft
description: "Run design reviews that find problems: stage-gate timing, agenda, required inputs, independent reviewer rule, actions and closure under ISO 13485 and FDA design controls."
sources: ["ISO 13485 Medical devices - Quality management systems (design and development review clause; confirm edition)", "21 CFR 820.30(e) Design review (as in force before the FDA QMSR transition; confirm current numbering)", "FDA, Design Control Guidance for Medical Device Manufacturers (1997)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Design reviews

**Goal:** a formal, documented evaluation at planned stages that finds design problems early and records decisions.

## Timing (typical gates)
1. User needs and design inputs approved.
2. Concept selection.
3. Design freeze before verification (design outputs).
4. Verification complete.
5. Validation complete and before design transfer or release.
Add reviews for risk, software, usability and manufacturing readiness as the plan requires.

## Preparation
- Circulate a pack in advance: current requirements, risk file summary, trace matrix status, open issues, test results, supplier status, regulatory status.
- Define attendees: functional representatives (design, quality, regulatory, manufacturing, clinical, service) and **at least one reviewer without direct responsibility for the stage** (the FDA rule), plus specialists as needed.

## Agenda
1. Purpose and entry criteria met?
2. Review of outputs against inputs; evidence that each requirement has verification planned or done.
3. Risk: new hazards, residual risk, risk controls verified.
4. Usability, software, manufacturability, serviceability and standards compliance.
5. Open actions from the last review.
6. Decision: proceed, proceed with conditions, or hold.

## Output
Minutes with date, attendees (names and functions), documents reviewed (with versions), findings, owners and due dates, and the decision. File in the design history file.

## Gotchas
- Reviews as presentations without challenge; assign a devil's-advocate reviewer.
- Late invitation of manufacturing and service.
- Actions not tracked to closure; review them at the next gate.

## Verify
- [ ] Independent reviewer recorded in the minutes.
- [ ] Each open item has an owner and date.
- [ ] Documents reviewed are identified by version.
