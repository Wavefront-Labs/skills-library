---
id: creative-arts.design-for-form-and-experience.ux-design.writing-user-requirements
name: writing-user-requirements
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [human-centred-design, iso-9241-210, user-requirements, usability-requirements, acceptance-criteria, iso-25065, requirements, ux-design]
level: practitioner
status: draft
description: "Turn research into testable user requirements per ISO 9241-210: user-need statements, usability requirements with measurable criteria, priorities and traceability."
sources:
  - "ISO 9241-210:2019 clause 7.3 Specify the user requirements (iso.org/standard/77520.html)"
  - "ISO/IEC 25065:2019 Common Industry Format - User requirements specification"
  - "ISO 9241-11:2018 Usability - definitions and concepts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# User requirements

**Goal:** requirements that say what users need to be able to do, under which conditions, to what
level of effectiveness, efficiency and satisfaction, so a design can be evaluated against them.

## Three kinds
1. **User needs** (from research): "Field technicians need to log a fault without removing gloves."
2. **User requirements** (what the system must allow): "The user shall be able to record a fault
   with photo and location in under 60 seconds while wearing work gloves."
3. **Usability requirements** (measurable outcome, ISO 9241-11 terms): effectiveness (task
   completion rate), efficiency (time, steps, errors), satisfaction (SUS or rating), each with a
   target and the context it applies in.

## Writing a good one
- Subject + capability + condition + criterion: "First-time users (context: mobile, no training)
  shall complete account setup with 90% success and a median time under 3 minutes."
- One requirement per sentence; avoid "user-friendly", "intuitive", "easy".
- Link to the context-of-use group and research evidence ID.
- Priority (MoSCoW) and verification method (usability test, expert review, analytics).

## Process
1. List needs from synthesis; group by user group and task.
2. Convert each to one or more requirements; mark the critical tasks.
3. Review with product and engineering for feasibility and conflicts (security vs speed).
4. Agree the measurable targets with stakeholders before design starts.
5. Baseline the current product if it exists, so targets are realistic.

## Gotchas
- Writing solutions as requirements ("shall have a dropdown") blocks better designs.
- Targets with no baseline are guesses; mark them provisional.
- Conflicting user groups need explicit priority.

## Verify
Every requirement is testable (you can name the test and the pass mark) and traces back to a need
and forward to an evaluation result.
