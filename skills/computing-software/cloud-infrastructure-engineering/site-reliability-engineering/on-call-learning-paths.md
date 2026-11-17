---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-learning-paths
name: on-call-learning-paths
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [on-call-learning-path, reverse-engineering-training, on-call-onboarding, shadowing, sre-training]
level: practitioner
status: docs-checked
description: "Build an on-call learning path: cumulative study, a learning checklist, reverse-engineering practice, postmortem reading, then shadow and reverse-shadow on-call."
sources: ["https://sre.google/sre-book/accelerating-sre-on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call learning paths and reverse-engineering training

SRE Book chapter "Accelerating SREs to On-Call and Beyond": favour concrete, sequential, cumulative learning
experiences over "trial by fire" or menial work such as alert and ticket triage, and over training strictly through
procedures, checklists and playbooks. Engineers will meet systems they have never seen, so teach reverse engineering.

## Learning path
- A cumulative, orderly path, with periodic homework questions about how the service works; satisfactory answers
  checked by the student's mentor show learning should continue to the next phase.
- An "on-call learning checklist": an organised reading and comprehension list of the technologies and concepts of
  the system. The student internalises it before being eligible to shadow on-call. It also lets mentors and managers
  observe progress.
- Targeted project work, not menial work.
- Suggested order for your own path (judgement, not from the book): request path, administration tasks, dependencies
  and failure modes, monitoring and alerts, past incidents, shadow, reverse shadow. Sign off on demonstrated tasks.

## Reverse-engineering practice
- The book describes reverse engineers, statistical and comparative thinkers, and improv artists as the targets.
- Example from the book: a new SRE asked to learn part of a service by reverse engineering it herself, with the team
  correcting what she missed, rather than hearing a talk.

## Five practices from the chapter
1. Reading and sharing postmortems, including curated "teachable" ones, postmortem reading clubs and "tales of fail".
2. Disaster role playing.
3. Breaking real things and fixing real things.
4. Documentation as apprenticeship (the learning checklist).
5. Shadowing on-call early and often; the on-caller includes the newcomer as coauthor of any postmortem; optionally
   the experienced on-caller "reverse shadows" while the newcomer is primary and owns escalations, diagnosing
   independently without modifying state and offering help when needed.

## Gotchas
- Do not push students to primary on-call before they understand the service holistically.
- Do not dump postmortem writing on the junior person.

## Verify
- [ ] Each step has concrete demonstrable tasks.
- [ ] A learning checklist exists and a mentor reviews progress.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Accelerating SREs to On-Call and Beyond": do/avoid table, cumulative learning paths with homework checked by a mentor, on-call learning checklist before shadowing, reverse engineering section, five practices, postmortem coauthor tip, reverse shadow description.
Removed: the 4-8 week tier table timings and rotation counts, the "top 10 postmortems" figure, shell commands (kubectl, ss), and the workbook source (not read).
Method: documentation only; no commands were run.
