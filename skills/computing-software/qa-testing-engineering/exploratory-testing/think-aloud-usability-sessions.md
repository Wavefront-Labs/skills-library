---
id: computing-software.qa-testing-engineering.exploratory-testing.think-aloud-usability-sessions
name: think-aloud-usability-sessions
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [think-aloud-protocol, usability-testing, moderated-testing, user-research, task-scenarios]
level: practitioner
status: draft
description: "Run moderated think-aloud usability sessions: recruit five users, write task scenarios, moderate without leading, capture observations and rate severity."
sources:
  - https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
  - https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
  - https://www.iso.org/standard/63500.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moderated think-aloud usability sessions

**Goal:** observe real users attempt real tasks while verbalising their thoughts, to find where the design fails them. ISO 9241-11 usability = effectiveness, efficiency, satisfaction.

## Plan
- 5 participants per round per user group finds most major problems; run several small rounds rather than one big one.
- Recruit representative users (not colleagues). Screener on role, experience, device.
- 4-6 task scenarios, goal-based, no UI words: "You want to send £50 to your sister. Do it." not "Click Transfer".
- Define success criteria per task (completed / with help / failed), time, errors.

## Session (45-60 min)
1. Consent, recording permission, "we are testing the design, not you".
2. Practice think-aloud on a neutral task.
3. Tasks one at a time; participant reads the scenario aloud.
4. Moderator prompts only with neutral probes: "What are you thinking?", "What do you expect to happen?", "Keep talking." Never explain the UI or answer "is this right?" (reflect back: "What do you think?").
5. Post-task: Single Ease Question (1-7). Post-test: SUS questionnaire.
6. Debrief: anything confusing, compare to current tools.

## Capture
- Note-taker (not the moderator) logs timestamped observations: quote, behaviour, task, severity.
- Record screen + face/audio (with consent); remote via video call screen share works.

## Analysis
- Affinity-map observations across participants; count how many participants hit each issue.
- Severity (Nielsen 0-4): frequency x impact x persistence.
- Report top issues with clips/quotes and a recommendation each.

## Gotchas
- Leading questions and helping invalidate the task.
- Observers in the room change behaviour; use a separate observation channel.
- Think-aloud slows users; do not use time on task as a benchmark metric in the same session.

## Verify
Each issue in the report is traced to observed sessions with participant count and severity, and stakeholders saw at least one session live or as clips.
