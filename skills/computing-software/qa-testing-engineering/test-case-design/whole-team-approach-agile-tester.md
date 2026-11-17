---
id: computing-software.qa-testing-engineering.test-case-design.whole-team-approach-agile-tester
name: whole-team-approach-agile-tester
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [whole-team-approach, agile-tester, testing-principles, three-amigos, agile-testing, quality-ownership, istqb]
level: practitioner
status: docs-checked
description: "Work as a tester in a whole-team agile setup: shared quality ownership, early involvement in refinement, pairing with developers and coaching rather than gatekeeping."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://agiletester.ca/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Whole-team approach and the agile tester role

**Goal:** testing expertise spread across the team so quality is built in, not inspected in. Gregory & Crispin, *Agile Testing*.

## What the tester does in each ceremony
- **Refinement**: ask "how would we test this?", surface edge cases, push for testable acceptance criteria (see `writing-testable-acceptance-criteria`).
- **Three amigos** before a story starts: business, dev, test agree examples.
- **During the sprint**: pair with developers on unit/integration test design, test each story as soon as a slice is deployable, run short exploratory charters.
- **Definition of done**: own the quality criteria with the team.
- **Retro**: bring escaped-defect data and flaky-test stats.

## Ownership split (typical)
| Activity | Primary | Tester contribution |
|---|---|---|
| Unit tests | Dev | Test idea review |
| API/integration tests | Dev + tester | Design, data, negative cases |
| E2E automation | Shared | Framework, critical journeys |
| Exploratory | Tester | Coaching devs to do it too |

## Gotchas
- A tester who receives stories only when "dev done" is a mini-waterfall inside the sprint. Insist on testing slices.
- Whole-team does not mean no testing specialists; it means no hand-off wall.

## Verify
Stories enter the sprint with agreed examples, and few story defects are found after the story is marked done.

## Checked

2026-10-28. Confirmed: agiletester.ca lists the book Agile Testing by Janet Gregory and Lisa Crispin. Removed: Syllabus section number and the "~20%" threshold.

Method: documentation only; no commands were run.
