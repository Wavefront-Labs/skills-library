---
id: computing-software.game-programming.game-ai-programming.dynamic-difficulty-adjustment
name: dynamic-difficulty-adjustment
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, ai-difficulty, dynamic-difficulty-adjustment, rubber-banding, difficulty-levels, ai-handicaps, game-programming]
level: practitioner
status: draft
description: "Scale AI difficulty: static difficulty parameters, deliberate AI imperfection (reaction time, aim error, search depth), dynamic adjustment from performance, rubber-banding and fairness."
sources: ["https://www.chessprogramming.org/Playing_Strength", "https://www.gameaipro.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI difficulty scaling

**Goal:** opponents that are beatable and fair at every skill level, using parameters players
cannot easily perceive as cheating.

## Make AI imperfect on purpose
A competent AI is easy; a believable, beatable one is the work. Tunable knobs per difficulty:
- **Reaction time** before responding to a newly seen threat (e.g. 0.6 s easy, 0.25 s hard).
- **Aim error**: cone or offset that shrinks over time while tracking (first shots miss, "warning
  shots"); never perfect tracking on easy.
- **Perception**: view distance, hearing range, peripheral vision angle, time to notice.
- **Decision quality**: utility score noise; chance to choose a suboptimal action; slower
  re-evaluation rate.
- **Aggression**: attack token counts (see `squad-coordination-ai`), grenade cooldowns, flank frequency.
- **Board/strategy games**: search depth or time, evaluation noise, MCTS iteration count, or
  choosing among top-k moves weighted by score (Elo-calibrated levels; see
  `minimax-and-alpha-beta-pruning`, `monte-carlo-tree-search`).
- Avoid raw stat buffs (more HP/damage) as the main lever; they feel cheap.

## Dynamic difficulty adjustment (DDA)
Measure performance (deaths per segment, health on arrival, accuracy, time to clear, win/loss
streak) and nudge parameters within bounds:
```
skill = lerp(skill, observedPerformance, 0.1)     // smoothed
aiAccuracy = baseAccuracy * clamp(1 + (skill - target) * k, 0.7, 1.3)
```
- Small, slow, bounded changes; hidden from the player in single-player; adjust between encounters
  rather than mid-fight.
- Resident Evil 4 style hidden rank and Left 4 Dead's director (see `ai-director-pacing`) are classic
  examples.
- Competitive multiplayer should use matchmaking (MMR), not DDA.

## Rubber-banding (racing/sports)
Speed bonuses for trailing AI and caps for leading AI keep races close; keep effects subtle and
disable or reduce on the hardest settings. Players notice and resent obvious catch-up.

## Fairness rules
AI does not read input, see through walls or know the player's position without perceiving it
(unless the design explicitly says so); difficulty differences come from reaction, accuracy and
choices.

## Verify
- [ ] Automated bot runs: win rate per difficulty matches targets (e.g. 90/60/30%).
- [ ] Playtest telemetry: deaths per segment fall inside the target band after DDA.
- [ ] Testers cannot identify DDA moments in blind playtests.
