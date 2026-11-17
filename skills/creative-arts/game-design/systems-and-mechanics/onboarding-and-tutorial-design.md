---
id: creative-arts.game-design.systems-and-mechanics.onboarding-and-tutorial-design
name: onboarding-and-tutorial-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, tutorial-design, onboarding, game-ux, learning-curve, hodent, cognitive-load, contextual-tutorials, teach-by-doing, ftue]
level: practitioner
status: draft
description: "Design onboarding that teaches by doing: sequence mechanics, one concept at a time, contextual prompts, spaced repetition, and measure learning with first-session data."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Onboarding and tutorial design

**Goal:** new players learn what they need, when they need it, by playing, and reach the
fun quickly.

Celia Hodent (*The Gamer's Brain*) applies cognitive psychology to games: limited
attention and working memory mean players learn best by doing, one thing at a time, with
reinforcement spaced over time.

## Principles
1. **Learning by doing:** prompt the action, let the player do it, confirm success.
   Text walls are skimmed or skipped.
2. **One concept at a time:** introduce, practise, then combine.
3. **Context:** teach a mechanic right before it is needed, not in a front-loaded lesson.
4. **Spaced repetition:** reuse the mechanic soon after teaching, then again later.
5. **Meaningful context:** explain *why* (what problem it solves), not only *how*.
6. **Safe space:** first use should be low-risk.
7. **Respect expertise:** let experienced players skip or speed through.

## Procedure
1. **List what a player must know** to play the core loop; order by dependency.
2. **Cut the list:** what can be discovered later, or not taught at all because it is
   conventional for the genre?
3. **Design a teaching beat per item:** trigger, prompt (diegetic if possible), action,
   confirmation, follow-up use.
4. **Keep prompts until performed:** reminders reappear if the player has not done the
   action (e.g. after some seconds idle).
5. **Reference:** a help/codex screen for re-learning, especially after a break.
6. **Measure:** funnel the first session (which step do players fail or quit at?), and
   run usability tests with first-time players (see
   `creative-arts.game-design.playtesting-and-balance.usability-testing-for-games`).

## Gotchas
- "Press X to jump" for a skill everyone knows wastes attention; prefer silent
  affordances for genre conventions.
- Tutorials that cannot be skipped annoy returning players and second playthroughs.
- Developer curse of knowledge: the team cannot unsee the game; only fresh testers
  reveal onboarding gaps.

## Verify
- [ ] Must-know list ordered by dependency, with cuts.
- [ ] Each item has a teaching beat and a follow-up use.
- [ ] First-session funnel shows no step losing a disproportionate share of players.
- [ ] Skip option for experienced players.
