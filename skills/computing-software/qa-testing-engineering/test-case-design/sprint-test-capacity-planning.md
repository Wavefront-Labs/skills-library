---
id: computing-software.qa-testing-engineering.test-case-design.sprint-test-capacity-planning
name: sprint-test-capacity-planning
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [sprint-test-capacity, agile-testing, capacity-planning, test-estimation, scrum]
level: practitioner
status: docs-checked
description: "Plan testing within sprint capacity: include test tasks in story points, available tester days, automation and regression time, and WIP limits to avoid end-of-sprint crunch."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://scrumguides.org/scrum-guide.html
  - https://agiletester.ca/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing effort in sprint capacity planning

**Goal:** testing fits inside the sprint instead of spilling into the next one or becoming a mini-waterfall at the end.

## Capacity maths
- Available hours per person = sprint days x focus hours per day minus leave, ceremonies and support rota.
- Reserve test capacity for non-story work explicitly: regression run, automation maintenance, exploratory sessions on risky areas, environment issues.

## Estimating stories
- Story points cover the whole team's effort including testing and automation; ask "what would make testing this hard?" during refinement (data setup, third-party sandbox, devices).
- Split stories whose testing alone would not fit: by rule, by data type, by platform.
- Add explicit sub-tasks: test design, automation, exploratory charter, accessibility check.

## Flow practices
- **WIP limits** on "in test" so work does not pile up for one tester at the end.
- **Test early:** developers pair with testers on acceptance tests before code (ATDD); testers test feature-flagged increments mid-sprint.
- **Whole team:** developers pick up test tasks when testing is the bottleneck.
- Track carry-over caused by testing in retrospectives.

## Signals of under-planning
Most stories enter test in the last two days; regression skipped; automation backlog grows every sprint; "done" excludes testing.

## Verify
Over three sprints, stories reach "in test" spread across the sprint, testing-caused carry-over trends to zero, and regression and automation time is planned, not squeezed.

## Checked

2026-10-28. Confirmed: Scrum Guide: planning uses the team's upcoming capacity. Removed: The "5-6 focus hours" and "20-30% of tester time" figures.

Method: documentation only; no commands were run.
