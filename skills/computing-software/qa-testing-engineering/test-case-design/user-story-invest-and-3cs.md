---
id: computing-software.qa-testing-engineering.test-case-design.user-story-invest-and-3cs
name: user-story-invest-and-3cs
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [invest-criteria, user-story-testing, collaborative-user-story-writing, card-conversation-confirmation, story-splitting, istqb]
level: practitioner
status: docs-checked
description: "Collaborate on user stories using the 3 Cs (card, conversation, confirmation) and INVEST, and split stories so each slice is independently testable."
sources:
  - https://xp123.com/invest-in-good-stories-and-smart-tasks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collaborative user story writing: 3 Cs and INVEST

**Goal:** stories that testers can test as soon as they are built, using Ron Jeffries' three components of an XP story
and Bill Wake's INVEST criteria (xp123.com, 2003).

## 3 Cs
- **Card**: the physical medium of the story, not the whole story.
- **Conversation**: the discussion around it; business, dev and test talk it through (see `example-mapping-three-amigos`).
- **Confirmation**: tests that verify the story (see `writing-testable-acceptance-criteria`).

## INVEST (tester's reading)
I - Independent, N - Negotiable, V - Valuable, E - Estimable, S - Small, T - Testable.
- **Independent**: can be tested without another unfinished story; otherwise sequence or merge.
- **Negotiable**: details are discussed, not fixed upfront.
- **Valuable**: the benefit is observable by a user, so there is something to accept.
- **Estimable**: if no one can estimate the testing, the behaviour is unclear.
- **Small**: testable within the sprint, with time to fix found defects.
- **Testable**: a story carries an implicit promise that you understand it well enough to write a test for it; Wake notes
  that requiring customer tests before implementing a story has made teams more productive.

## Splitting for testability
By workflow step, business rule, data variation, happy path versus error handling, platform, or performance level. Avoid
splitting by layer (UI story, API story, database story): none of them is testable by a user alone.

## Gotchas
- Technical stories without user-visible behaviour still need confirmation criteria.
- Stories marked done with known defects to be "fixed in the next story" break the definition of done.

## Verify
Stories in the next sprint pass an INVEST check in refinement, especially I, S and T.

## Checked
2026-10-28. Confirmed in Bill Wake's "INVEST in Good Stories, and SMART Tasks" (xp123.com): the three components (Cards,
Conversation, Confirmation) attributed to Ron Jeffries, the six INVEST letters, and the Testable passage. Removed as
unconfirmed: the ISTQB CTFL syllabus section reference (the ISTQB page is a certification landing page), the story
template wording, the p95 example. The ISTQB link was dropped from `sources`.
Method: documentation only; no commands were run.
