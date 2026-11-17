---
id: computing-software.systems-network-administration.backup-and-recovery.multi-year-dr-exercise-program
name: multi-year-dr-exercise-program
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [exercise-program, dr-exercise, testing-calendar, continuous-improvement]
level: practitioner
status: docs-checked
description: "Build a DR test, training and exercise programme per NIST SP 800-84: policy, roles, schedule, four-phase event method and exercise progression."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DR exercise programme

Isolated tests leave gaps. NIST SP 800-84 recommends a programme of test, training and exercise (TT&E) events, because exercises and tests find different problems with plans, procedures and training.

## Programme elements
- A **TT&E plan** setting out the steps to make sure personnel are trained in their roles, plans are exercised to validate viability, and components and systems are tested for operability in the context of the plan. It, with a policy, event methodology and procedures, makes events more consistent and cuts duplication.
- A **policy** stating internal and external requirements, with suggested elements: purpose, effective date, objectives, applicability and scope, authorities and related policies, roles and responsibilities, TT&E requirements, review and approval, enforcement and compliance, points of contact and definitions. Win senior management support first.
- **Roles**: an IT plan coordinator (overall responsibility for the plans) who names a TT&E program coordinator to develop the TT&E plan and coordinate events with event design teams. Many organisations lead it from the Office of the CIO.
- Address **resource and budget** requirements, and a **schedule** that documents the frequency of each type of event. Events should be run as needed too: after organisational changes, plan updates or new guidance. SP 800-53 requires federal agencies to exercise or test contingency plans and incident response capabilities at least annually.

## Progression
Events normally occur in the order training, exercise, test: people are trained before they exercise, and exercises usually precede tests. Do a training event and a tabletop exercise before a functional exercise. Tabletops are discussion-based and deploy no equipment; functional exercises simulate operations and range from specific aspects of a plan to full-scale exercises covering all plan elements. Start functional exercises with operational-level roles and bring senior-level staff in as the programme matures.

## Event method (same four phases for every event)
1. Design: topic, scope, objectives, participants, design team, logistics.
2. Develop the documentation (briefings, guides, scripts, evaluation criteria).
3. Conduct.
4. Evaluate lessons learned: for exercises and tests, a facilitated hot wash and an after action report; use lessons to improve both the plans and the TT&E process.

## Gotchas
Hold a training event or tabletop before the first functional exercise, and keep management informed: their agreement to each scheduled exercise is an essential step.

## Verify
A written TT&E plan with a schedule, each event followed by an after action report, and the plan updated from its recommendations.

## Checked

2026-11-09. Read NIST SP 800-84 sections 2.1 to 2.4, 4.1, 5.1 and 5.2. Removed: FEMA HSEEP and ISO 22301 clause references (not read), the seminar/drill building-block ladder, the monthly, quarterly and annual calendar, Gold/Silver coverage targets, scenario rotation list, metrics and board reporting (none stated in SP 800-84).

Method: documentation only; no commands were run.
