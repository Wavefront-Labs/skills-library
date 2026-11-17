---
id: creative-arts.game-design.puzzle-design.puzzle-skip-and-solve-options
name: puzzle-skip-and-solve-options
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-skip, accessibility, hint-systems, difficulty-options]
level: practitioner
status: draft
description: "Design puzzle skip and auto-solve options: when to offer them, cost or no cost, preserving the aha with a reveal, accessibility needs and tracking skip rates as a design signal."
sources:
  - https://gameaccessibilityguidelines.com/
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Puzzle skip and solve options

**Goal:** no player is permanently blocked by a single puzzle, while players who want the
challenge can ignore the option. Schell's ninth principle: *give the answer*.

## Options
| Option | Example | Notes |
|---|---|---|
| Skip | Uncharted / Tomb Raider style "skip puzzle" assist; many mobile puzzlers | progress without seeing the answer |
| Auto-solve with reveal | the game shows the solution step by step | aha preserved as "oh, of course" |
| Paid skip (currency) | hint coins | monetisation risk; avoid pay-to-progress pressure |
| Earned skips | token per N puzzles solved | rewards play; limited supply |
| Leave and come back | open hubs, parallel puzzles | soft skip by structure |

## Design procedure
1. **Decide default availability:** from the start in settings (accessibility), or after
   a stuck threshold (time or attempts) with an offer.
2. **Phrase the offer neutrally:** "Skip this puzzle?" not "Too hard for you?". No penalty
   messages.
3. **Prefer reveal over silent skip** for puzzles that teach a rule used later; otherwise
   the player hits the next puzzle without the lesson. Alternatively, skip only optional puzzles.
4. **Rewards:** decide whether skipped puzzles still give completion credit; achievements
   for no-skip runs are fine, removing story content is not.
5. **Track skip rate per puzzle** in telemetry; high rates show a puzzle out of place in
   the ramp.

## Accessibility
Cognitive and motor disabilities make some puzzles impassable; the Xbox Accessibility
Guidelines and Game Accessibility Guidelines both recommend skip or assist options for
challenging content.

## Gotchas
- An always-visible skip button tempts players who would have enjoyed solving; delay the offer.
- Skipping a puzzle that sets world state must apply that state (doors open, items given).
- Speedrun exploits through skip options; decide if acceptable.

## Verify
- [ ] Every mandatory puzzle can be skipped or revealed.
- [ ] Skip correctly applies all puzzle outcomes.
- [ ] Skip rate per puzzle logged and reviewed.
