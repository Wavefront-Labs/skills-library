---
id: computing-software.systems-network-administration.backup-and-recovery.dr-exercise-evaluation-and-observers
name: dr-exercise-evaluation-and-observers
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [exercise-evaluator, dr-exercise, observers, evaluation-guide, after-action]
level: practitioner
status: docs-checked
description: "Evaluate a DR exercise per NIST SP 800-84: objective-based evaluation criteria, data collectors, collection forms, hot wash and the after action report."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DR exercise evaluation and observers

NIST SP 800-84 gives observation to **data collectors**, who record what happens during the exercise, separate from players, and ties what they record to evaluation criteria written beforehand.

## Before
1. **Objectives**: validate the plan's content, roles and responsibilities, and interdependencies. Document them specifically.
2. **Evaluation criteria** closely tied to the objectives, developed during exercise development so data collectors know what to capture.
3. **Collection forms**: forms or tools that instruct data collectors which player actions to look for. They are a roadmap for deciding whether objectives were met, how, what plan improvements are needed and where more exercises are necessary.
4. **Staff**: for a tabletop, a facilitator and a data collector; for a functional exercise, a director, controllers, data collectors and simulators. All should know the plan and objectives thoroughly, and should meet beforehand and review earlier exercise results.

## During
- Data collectors directly observe player actions and refer to the evaluation criteria and their forms.
- For tabletops, the data collector records observations for the after action report.
- Controllers keep to the MSEL and message inject tracking form, which records scheduled and actual times of injects.

## After
- **Hot wash** immediately after play. In a tabletop the facilitator asks which areas participants excelled in, which need more training and which parts of the plan to update. In a functional exercise the director leads it, asks participants, controllers, simulators and data collectors for feedback, and collects their notes and forms.
- The design team or other staff write the **after action report** from those notes, forms and hot wash material: background, observations and recommendations, plus a participant list and any survey results.
- The plan coordinator can assign action items and update the plan.

## Gotchas
Objectives without a specific, documented statement of what should happen cannot be evaluated; write evaluation criteria before the exercise, not afterwards.

## Verify
Every objective has an assessment backed by data collectors' records, and each recommendation has an owner.

## Checked

2026-11-09. Read NIST SP 800-84 sections 4.2.5, 4.3 to 4.5 and 5.2 to 5.5 (staff, evaluation criteria, forms, hot wash, after action report). Removed: FEMA HSEEP and NIST SP 800-34 sources (not read), Exercise Evaluation Guide terminology, the independent-evaluator advice (internal audit or another team), the example measurable objectives, the 30 to 60 minute hot wash and 2 day completion timings, the RTO/RPO measurement list and the "evaluators from the same team grade generously" gotcha (not stated).

Method: documentation only; no commands were run.
