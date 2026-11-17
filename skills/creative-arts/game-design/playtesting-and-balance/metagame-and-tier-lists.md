---
id: creative-arts.game-design.playtesting-and-balance.metagame-and-tier-lists
name: metagame-and-tier-lists
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, metagame, tier-lists, pick-rate, win-rate, competitive-balance, card-games]
level: practitioner
status: draft
description: "Read a competitive game's metagame from pick and win rates, build or interpret a tier list, and tell a healthy diverse metagame from a solved one."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metagame and tier lists

**Goal:** understand which strategies, characters or decks players actually choose, and whether the spread is healthy.

## Data to gather
- **Pick (play) rate** of each option, **win rate**, and **ban rate** where bans exist, split by skill bracket and by matchup where sample size allows.
- Tournament results and ladder data separately; they answer different questions (top-level optimum vs. everyday play).

## Procedure
1. **Pull data per patch** so results are not mixed across versions.
2. **Chart pick rate against win rate.** High pick with high win rate is a dominant option; high win with low pick is hidden strength or a hard-to-play option; low win with high pick is a trap or a popular but weak pick.
3. **Check matchup structure:** a healthy metagame has counters in a loose cycle (rock-paper-scissors-like), so no single option beats everything. Look at the matchup matrix, not just overall win rate.
4. **Build tiers** by grouping options by performance with confidence intervals; a tier list is a ranking of expected performance with uncertainty, not a verdict.
5. **Watch for a solved metagame** where a few options crowd out the rest; plan changes that open counters or lift under-used options.

## Gotchas
- Win rate of rarely-picked options is biased by who picks them (experts pick hard characters).
- Pick rates follow social media as much as strength; wait a few days after a patch for settling.
- Player-made tier lists are opinion and differ by skill bracket.

## Verify
- [ ] Data isolated by patch and skill bracket.
- [ ] Matchup matrix examined, with sample sizes shown.
- [ ] Conclusion states uncertainty.
