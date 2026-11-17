---
id: creative-arts.game-design.playtesting-and-balance.interpreting-player-feedback
name: interpreting-player-feedback
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, interpreting-feedback, design-iteration, feedback-triage, playtest-analysis, root-cause, player-suggestions, observation-vs-opinion]
level: practitioner
status: draft
description: "Turn raw playtest feedback into design decisions: separate observations from opinions, find root causes behind suggestions, weight by audience fit and frequency, and decide."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Interpreting player feedback

**Goal:** extract the real problems from what players say and do, without either
dismissing feedback or implementing every suggestion literally.

A common designer maxim: players are good at telling you something is wrong and
usually poor at telling you how to fix it. Schell (2nd ed.) ch27 and Fullerton ch9 both stress
watching what players do, not just what they say.

## Procedure
1. **Separate the data types:**
   | Type | Example | Weight |
   |---|---|---|
   | Observation (behaviour) | 4 of 5 testers never used the shield | high |
   | Reported experience | "I felt lost in the forest" | high |
   | Opinion | "The forest is bad" | medium |
   | Suggestion | "Add a minimap" | low as a solution, high as a symptom |
2. **Translate suggestions into problems:** "add a minimap" -> "players lose
   orientation" -> possible fixes: landmarks, lighting, minimap, compass.
3. **Find the root cause:** ask "why" until you reach a design element ("lost" ->
   "paths look alike" -> "no landmarks visible from the junctions").
4. **Weight by audience fit:** feedback from testers outside the target audience
   counts less on taste issues (but still counts on usability).
5. **Weight by frequency and severity:** one passionate tester ≠ a pattern.
6. **Check against pillars:** feedback that pushes against a pillar (e.g. "make it less
   scary" for a horror game) may be a signal about audience, not design.
7. **Decide and log:** act / investigate / reject, with reason.

## Feedback log columns
`date | build | source (n testers) | raw quote/observation | underlying problem | severity | decision | owner`

## Gotchas
- Designers defend their work; have someone else summarise sessions first.
- Loudest feedback (forums, streamers) over-represents engaged players.
- Contradictory feedback often means two audience segments; decide whom you serve.
- Absence of complaints isn't evidence of delight; look for positive behaviours.

## Verify
- [ ] Every suggestion translated into a problem statement.
- [ ] Decisions logged with reasons.
- [ ] Changes re-tested to see whether the underlying problem moved.
