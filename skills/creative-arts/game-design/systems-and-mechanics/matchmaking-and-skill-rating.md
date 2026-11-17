---
id: creative-arts.game-design.systems-and-mechanics.matchmaking-and-skill-rating
name: matchmaking-and-skill-rating
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, matchmaking, elo-rating, glicko, trueskill, mmr, multiplayer-design, ranked-play, competitive-games, rating-systems]
level: advanced
status: draft
description: "Choose and tune a skill rating (Elo, Glicko-2, TrueSkill) and matchmaking rules: K-factor, uncertainty, team games, queue time vs match quality, and visible ranks vs hidden MMR."
sources:
  - https://en.wikipedia.org/wiki/Elo_rating_system
  - http://www.glicko.net/glicko/glicko2.pdf
  - https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matchmaking and skill rating

**Goal:** matches that are close enough to be fun, found quickly enough that players do
not quit the queue, and a rating players trust.

## Rating systems
| System | Key idea | Good for |
|---|---|---|
| Elo | rating updates by K x (actual - expected) | 1v1, simple |
| Glicko / Glicko-2 | adds rating deviation (uncertainty) and volatility | 1v1 with irregular play |
| TrueSkill (Microsoft) | Bayesian mean and sigma; supports teams and free-for-all | team and multiplayer games |
Elo expected score: `E_A = 1 / (1 + 10^((R_B - R_A)/400))`; update
`R_A' = R_A + K * (S_A - E_A)`. A 200-point gap means ~76% expected for the higher-rated.

## Design decisions
1. **New player placement:** high uncertainty/K early so ratings converge fast
   (placement matches); lower later for stability.
2. **Hidden MMR vs visible rank:** many games match on hidden MMR and show a separate,
   more forgiving visible rank (with tiers, promotions, decay). Explain enough to keep
   trust.
3. **Team games:** match on team averages plus spread; parties of friends vs solo
   players need adjustment (parties coordinate better).
4. **Queue time vs quality:** widen the acceptable rating gap the longer a player waits;
   set a maximum gap. Small populations (late night, high ranks, regions) need this most.
5. **Smurfing and boosting:** fast upward convergence for over-performers, account
   linking, behaviour detection.
6. **Inactivity:** increase uncertainty (Glicko does this naturally) rather than
   punishing with decay alone.

## Python Elo check
```python
def expected(ra, rb): return 1 / (1 + 10 ** ((rb - ra) / 400))
assert abs(expected(1700, 1500) - 0.76) < 0.01
```

## Gotchas
- Pure win/loss ratings ignore performance; adding performance metrics invites
  stat-padding instead of winning.
- "Forced 50% win rate" conspiracy perceptions are common; publish how matchmaking works.
- Rating inflation/deflation drifts over seasons; monitor the distribution.

## Verify
- [ ] Rating system chosen with reasons (1v1 vs team, play frequency).
- [ ] Placement, K/uncertainty schedule and max match gap documented.
- [ ] Queue time and match-closeness metrics monitored (e.g. predicted win probability near 50%).
