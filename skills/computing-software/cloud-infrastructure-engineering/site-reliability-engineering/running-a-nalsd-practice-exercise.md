---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.running-a-nalsd-practice-exercise
name: running-a-nalsd-practice-exercise
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, nalsd, nalsd-exercise, design-training, workshop, interviews]
level: practitioner
status: docs-checked
description: "Run a NALSD practice workshop: pick a problem with scale numbers, walk the Workbook's iterations from one machine to a resilient distributed design, compute resources, debrief."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a NALSD practice exercise

**Goal:** build the team's skill at designing systems with concrete numbers, not boxes and arrows. The Workbook calls
NALSD a learned skill that needs regular practice to maintain proficiency.

## Prepare
- Pick a problem with clear scale. The Workbook uses the AdWords click-through-rate dashboard: join a query log and
  a click log, 500,000 queries per second, 10,000 clicks per second, two SLOs.
- Write a one-page brief: functional requirements, scale numbers, SLOs and constraints.
- Prepare a reference sheet of hardware assumptions (disk IOPS, RAM per machine, network).

## Run (Workbook iteration structure)
1. **Clarify requirements**: groups ask questions; the facilitator answers from the brief.
2. **Is it possible?** Design on one machine ignoring scale limits; compute the numbers.
3. **Can we do better?** Improve the algorithm and data structures.
4. **Is it feasible?** Scale up with a distributed design given limits on money and hardware.
5. **Is it resilient?** What happens when a component fails, and when an entire datacenter fails?
6. **Can we do better?** Revisit simplicity and efficiency.
7. Groups present designs, with arithmetic shown.

## Facilitation tips
- Push for numbers at each step ("how many disks?", "what binds first?").
- Reward sound reasoning and stated assumptions over matching a final value.
- Expect to bounce between questions rather than follow a strict order.

## Debrief
- Compare assumptions and resource totals; discuss which numbers differed most and why.
- Update the brief and reference sheet.

## Verify
- [ ] Each group produced a design with a resource estimate; feedback collected.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": the question sequence, the AdWords problem and its numbers, "NALSD is a learned skill", bouncing between phases, reasoning over final values.
Removed: group sizes, session length, phase timings, alternative problem suggestions with figures, and the on-call training source.
Method: documentation only; no commands were run.
