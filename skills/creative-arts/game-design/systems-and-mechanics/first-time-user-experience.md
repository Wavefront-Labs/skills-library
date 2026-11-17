---
id: creative-arts.game-design.systems-and-mechanics.first-time-user-experience
name: first-time-user-experience
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, ftue, first-time-user-experience, interest-curve, onboarding, retention, first-five-minutes, hook, d1-retention, mobile-games]
level: practitioner
status: draft
description: "Design the first-time user experience: reach the core fun within minutes, front-load the hook, defer menus and accounts, and measure the first-session funnel."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First-time user experience (FTUE)

**Goal:** a new player's first session delivers the game's essential experience fast
and makes them want a second session.

## Principles
- **Time to fun:** measure seconds from launch to first meaningful input and to the
  first moment of the core experience. Cut everything in front of it.
- **Hook first** (Schell's interest curve starts with a hook): an exciting,
  representative moment early.
- **Defer friction:** account creation, settings, long intros, store prompts, and
  permission requests until the player is invested (platform rules permitting).
- **Teach only what the first session needs** (see
  `creative-arts.game-design.systems-and-mechanics.onboarding-and-tutorial-design`).
- **End the first session on a promise:** a glimpse of what comes next (new area,
  locked feature, cliffhanger).

## Procedure
1. **Storyboard the first 10 minutes** second by second: what the player sees, does,
   and feels.
2. **Instrument a funnel:** launch -> first input -> tutorial step 1..N -> first win ->
   session end -> return next day. Find the biggest drop.
3. **Usability test with fresh players** (never seen the game), think-aloud.
4. **Cut or move** anything before first input that is not legally or technically
   required.
5. **Iterate** until the funnel's biggest drop is no longer a design problem.

## Common FTUE killers
| Killer | Fix |
|---|---|
| unskippable logos and long intros | shorten, allow skip, play during loading |
| forced login before play | guest play, link later |
| menu maze before play | "Play" as the default focused action |
| giant tutorial | split and contextualise |
| early difficulty spike | gentler first challenge |
| no clear goal | immediate concrete goal |

## Gotchas
- Platform certification may require certain screens (legal, age, health warnings);
  design around them, don't fight them.
- An FTUE optimised only for D1 retention can hide the game's real depth; check later
  retention too.

## Verify
- [ ] First-10-minutes storyboard exists.
- [ ] Time-to-first-input and time-to-core-moment measured.
- [ ] Funnel instrumented; biggest drop identified and addressed.
- [ ] Fresh-player usability sessions run.
