---
id: computing-software.systems-network-administration.backup-and-recovery.dr-tabletop-exercise
name: dr-tabletop-exercise
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [tabletop, tabletop-exercise, dr-exercises, scenario-design, nist-sp-800-84, business-continuity]
level: practitioner
status: docs-checked
description: "Run a disaster recovery tabletop exercise per NIST SP 800-84: objectives, participants, facilitator guide, short scenario, hot wash, after action report."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a tabletop exercise

**Goal:** test the plan's decisions, roles and coordination by walking through a scenario in discussion, without deploying equipment. NIST SP 800-84 describes tabletop exercises as discussion-based events in an informal environment where a facilitator guides participants through a discussion designed to meet pre-defined objectives.

## Design (start at least one month ahead, three for large exercises)
1. **Topic and scope**: set from the target audience. Senior-level and operational-level personnel initially take part in separate tabletops because their roles differ.
2. **Objectives**: validate the content of the plan and related policies and procedures, participants' roles and responsibilities as documented, and the interdependencies documented in the plan. Some exercises also meet a regulatory requirement (SP 800-84 cites the SP 800-53 requirement for federal agencies to exercise contingency plans at least annually).
3. **Participants**: people with roles in the plan. Invite senior-level personnel when the objective is decision-making and oversight, operational-level personnel when it is operational procedures. Send a written invitation early.
4. **Staff**: a facilitator who leads the discussion and a data collector who records what happens, both thoroughly familiar with the plan and objectives; they meet beforehand and review earlier exercise results.
5. **Logistics**: one person coordinates, starting at least one month ahead (date, room, equipment, invitations, guides, name tents, a backup copy of the files).
6. Duration typically two to eight hours; senior-level exercises usually run two to four hours, and a training session is advised when an exercise exceeds four hours.

## Material
- **Briefing** with agenda and logistics.
- **Facilitator guide**: purpose, scope and objectives, the scenario (a sequential narrative of a hypothetical incident), questions tied to the objectives, and a copy of the plan. Tailor questions: high-level decisions for senior staff, specific procedures for operational staff.
- **Participant guide**: the same without the question list, with a shorter list of orienting questions. Sending it about a week ahead is suggested.
- **After action report** template with evaluation criteria written before the exercise, so data collectors know what to capture.
- Keep the scenario short and concise; long detailed scenarios make participants dissect the scenario instead of meeting the objectives. The facilitator should be able to redirect focus to the objectives.

## Run
Use a classroom-type setting; name tents help, and participants are usually not seated with their own teammates. The facilitator welcomes everyone, has them introduce their roles, presents the briefing and walks through the scenario, then starts with a guide question aimed at decisions or coordination. The facilitator adds further guide questions if discussion stalls until objectives are met, and the data collector records observations.

## Hot wash
Immediately afterwards the facilitator and data collector debrief: which areas participants excelled in, which need more training, and which parts of the plan should be updated.

## After
Capture the debrief comments and the data collector's notes in the after action report: background (purpose, objectives, participants, scenario), observations, and recommendations for the plan. The plan coordinator can assign action items and update the plan, brief managers and update other security documents.

## Verify
Each objective has an assessment in the after action report, and each recommendation has an owner.

## Checked

2026-11-09. Read NIST SP 800-84 sections 4.1 to 4.6 (tabletop exercises). Removed: CISA tabletop exercise packages and FEMA HSEEP sources (not read), the example objectives and timed injects, the 4 to 6 week planning lead, the 20 to 30 minute hot wash length and the "no-fault" wording (not stated). Used the 800-84 durations and lead times instead.

Method: documentation only; no commands were run.
