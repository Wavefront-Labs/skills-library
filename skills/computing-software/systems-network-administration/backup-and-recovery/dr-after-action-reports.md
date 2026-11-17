---
id: computing-software.systems-network-administration.backup-and-recovery.dr-after-action-reports
name: dr-after-action-reports
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [after-action-report, improvement-plan, hot-wash, dr-exercises, lessons-learned]
level: practitioner
status: docs-checked
description: "Write after action reports for DR exercises per NIST SP 800-84: contents, evaluation criteria, hot wash input, and updating the plan from recommendations."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# After action reports and plan updates

**Goal:** every exercise produces recommendations that are assigned to someone and actually made in the plan.

## Prepare before the exercise
Write the evaluation criteria in advance, tied to the exercise objectives, so data collectors know what to capture. NIST SP 800-84 notes forms for data collectors help: they list specific player actions to look for and act as a roadmap to decide whether objectives were met, how, what improvements the plan needs and where more exercises may be necessary.

## Inputs
Data collectors' observations and notes, forms and material made during play, the hot wash comments, and any participant surveys distributed during the hot wash. At the end of a functional exercise the director asks controllers, data collectors, simulators and participants for their notes and forms.

## Contents
- Introduction with background: purpose or scope, objectives, participants (a participant list) and the scenario.
- Observations made by the facilitator or exercise staff and by participants during the exercise.
- Recommendations for enhancing the plan that was exercised.
- Optionally, results from participant surveys.

## After the report
The plan coordinator may assign action items to named people to update the plan, then updates the plan by implementing the recommendations where appropriate. It may also be necessary to brief managers on the results, update other security-related documents and take other actions.

## Writing tips
State specific observations with measurements ("the restore took X hours against an RTO of Y") instead of vague ones, and keep wording blameless. Track corrective actions with an owner and due date in the same system as other risks, and re-test the weak areas at the next exercise.

## Verify
At the next exercise, the previous report's action items are closed and the related objectives are assessed again.

## Checked

2026-11-09. Read NIST SP 800-84 sections 4.3, 4.5, 5.3 and 5.5 on after action reports. Removed: FEMA HSEEP source (not read) and its four-level rating scale, the improvement-plan matrix with sample row, the draft in 2 weeks and final in 30 days timings, and the 6 hours versus 2 hours example (none stated in SP 800-84). Owner, due date and tracking advice is practice guidance.

Method: documentation only; no commands were run.
