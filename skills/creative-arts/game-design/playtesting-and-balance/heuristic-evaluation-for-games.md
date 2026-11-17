---
id: creative-arts.game-design.playtesting-and-balance.heuristic-evaluation-for-games
name: heuristic-evaluation-for-games
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, heuristic-evaluation, games-user-research, nielsen-heuristics, play-heuristics, expert-review, usability, ux-audit]
level: practitioner
status: draft
description: "Run an expert heuristic evaluation of a game build using Nielsen's heuristics and game-specific heuristic sets, with multiple evaluators and severity-rated findings."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heuristic evaluation for games

**Goal:** a fast, cheap expert review that finds likely usability and experience problems
before (or between) player tests.

Heuristic evaluation (Nielsen and Molich) has a few experts inspect an interface against
a list of principles. Nielsen's ten usability heuristics cover general UI; game-specific
heuristic sets (e.g. Desurvire and colleagues' PLAY heuristics, discussed in *Games User
Research*) add gameplay, narrative and mechanics principles.

## Heuristics to use (examples)
- Nielsen's 10: visibility of system status; match with the real world; user control
  and freedom; consistency and standards; error prevention; recognition rather than
  recall; flexibility and efficiency; aesthetic and minimalist design; help users
  recognise, diagnose and recover from errors; help and documentation.
- Game additions (paraphrased themes from game heuristic sets): the player always knows
  their goal; controls are consistent and customisable; challenge matches skill; the
  game gives immediate, clear feedback; failure is recoverable and explained; the player
  can skip non-playable content; the tutorial teaches by doing.

## Procedure
1. **3-5 evaluators** (Nielsen's guidance: a single evaluator finds a fraction of
   problems; several find many more).
2. Each evaluator plays the build **independently**, ideally twice (once for flow, once
   for detail), noting issues against heuristics.
3. For each issue: location, heuristic violated, description, screenshot, severity
   (0-4 scale as in Nielsen's method).
4. **Merge** findings; deduplicate; agree severity.
5. Report top issues with recommendations; feed into the next player test to confirm.

## Gotchas
- Experts aren't the audience; heuristics predict problems but don't prove them. Confirm
  important findings with players.
- Evaluators who built the game are blind to its problems; use outsiders.
- Fun can't be evaluated by heuristics alone.

## Verify
- [ ] Heuristic list chosen and shared before evaluation.
- [ ] 3+ independent evaluators.
- [ ] Merged findings with severity ratings.
- [ ] Top findings checked in a subsequent player test.
