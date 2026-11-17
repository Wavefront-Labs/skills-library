---
id: creative-arts.game-design.systems-and-mechanics.battle-pass-design
name: battle-pass-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, battle-pass, monetization-design, free-to-play, season-pass, live-ops, reward-tracks, cosmetics, xp-pacing]
level: advanced
status: draft
description: "Design a seasonal battle pass: free vs premium tracks, tier count and XP pacing against real play time, reward placement, catch-up, and fairness to casual players."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Battle pass design

**Goal:** a seasonal reward track that gives players goals and the game recurring
revenue, completable by the target player in the time they actually play.

## Structure
| Element | Typical options |
|---|---|
| Season length | ~6-12 weeks |
| Tiers | ~50-100 |
| Tracks | free track + premium track; sometimes a premium+ bundle with tier skips |
| XP sources | matches played, challenges (daily/weekly/seasonal), events |
| Rewards | cosmetics, currency, boosts; premium track often refunds enough currency to buy next pass |

## Pacing procedure
1. **Define the target player:** e.g. plays 4 sessions/week of 40 minutes.
2. **Compute their season XP:** sessions x XP per session + challenge XP achievable at
   that rate.
3. **Set tier XP** so the target player finishes around 80-100% of the season, with some
   buffer; heavier players finish early, lighter players can catch up.
4. **Plot tiers vs weeks** for three profiles (light, target, heavy). The light player
   should still reach meaningful rewards.
5. **Catch-up:** weekly challenges that stay available all season, XP boosts late in the
   season.

## Reward placement
- Strong reward at tier 1 of premium (immediate value for buyers).
- Highlights spaced evenly; a marquee reward at the final tier.
- Free track must feel worthwhile (it is the funnel to premium).
- Show the full track upfront; no hidden tiers.

## Gotchas
- Challenge designs that force playing modes or characters players dislike ("win 5
  games as a healer") breed resentment; give choice among challenges.
- Selling tier skips to make the pass completable only by paying, after tuning XP
  against the target player, is a dark pattern (see
  `creative-arts.game-design.systems-and-mechanics.avoiding-dark-patterns`).
- FOMO-exclusive rewards that never return create pressure; some games now let old
  passes be completed later.
- Monitor tier distribution at season end; if most buyers do not finish, retune.

## Verify
- [ ] Target player profile and season XP calculation written.
- [ ] Light/target/heavy tier-vs-week plots produced.
- [ ] Catch-up mechanics in place.
- [ ] End-of-season tier distribution checked against the target.
