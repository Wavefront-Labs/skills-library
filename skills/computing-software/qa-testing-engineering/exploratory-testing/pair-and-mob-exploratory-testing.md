---
id: computing-software.qa-testing-engineering.exploratory-testing.pair-and-mob-exploratory-testing
name: pair-and-mob-exploratory-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [pair-testing, mob-testing, exploratory-testing, ensemble-testing, collaboration]
level: practitioner
status: draft
description: "Run pair and mob (ensemble) exploratory testing: driver/navigator roles, rotation timers, mixing dev, tester and product perspectives, and capturing findings."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.agilealliance.org/glossary/mob-programming/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pair and mob exploratory testing

**Goal:** combine perspectives in one session to find more varied defects and spread product knowledge.

## Pair testing
- Two people, one keyboard. **Driver** operates; **navigator** suggests ideas, takes notes, watches for oddities.
- Swap roles every 15-20 minutes.
- Useful pairs: tester + developer (developer learns failure modes, tester learns internals), tester + product owner (oracle on the spot), senior + new tester (coaching).
- Use a normal charter and session sheet; navigator owns the notes.

## Mob (ensemble) testing
- 3-8 people, one computer, shared screen.
- Strong-style rule: "for an idea to go from your head into the computer it must go through someone else's hands". Driver only types; the mob navigates.
- Rotate driver every 4 minutes (mob timer such as mobti.me).
- Facilitator keeps the charter in view and parks side discussions.
- Good for: new feature walkthrough before release, onboarding, accessibility sessions with a screen-reader user, cross-team bug bashes.

## Session flow (mob, 60-90 min)
1. Charter and roles (5 min).
2. Explore with rotation (45-70 min).
3. Retrospective: findings, follow-ups, what to change in the format (10 min).

## Capture
One person or a rotating role keeps notes in a shared doc; bugs triaged at the end, not mid-flow.

## Gotchas
- Dominant voices: enforce rotation and invite quieter members to navigate.
- Remote mobs need a fast screen-share and a handover method (git handover or shared remote environment).
- Too large a mob turns into a demo; split above ~8.

## Verify
Session produced notes and follow-ups, every participant drove, and defects found are attributed to the session for later comparison with solo sessions.
