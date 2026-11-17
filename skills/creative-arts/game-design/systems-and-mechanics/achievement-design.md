---
id: creative-arts.game-design.systems-and-mechanics.achievement-design
name: achievement-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, achievement-design, achievements, trophies, reward-design, steam-achievements, xbox-gamerscore, playstation-trophies, completionism, discovery]
level: practitioner
status: docs-checked
description: "Design an achievement list that guides discovery, rewards mastery and style, avoids grind and missables, and uses Steam stats and progress features."
sources:
  - https://partner.steamgames.com/doc/features/achievements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Achievement design

**Goal:** an achievement list that extends play in ways the player enjoys: pointing at
hidden content, rewarding skill and creativity, and marking progress, without grind or
frustration.

## Categories (aim for a mix)
| Category | Purpose | Example |
|---|---|---|
| Progress | mark milestones | finish chapter 2 |
| Discovery | point at missable content | find the hidden library |
| Mastery | reward skill | beat the boss without taking damage |
| Style / playful | suggest alternate play | defeat an enemy with a thrown chicken |
| Collection | completionists | collect all 50 relics |
| Social | multiplayer | win a match with a friend |
| Grind (avoid or keep few) | time sink | kill 10,000 enemies |

## Procedure
1. Write the list late in development when content is stable, but plan IDs early.
2. Steam shows global unlock percentages per achievement in the Community and the API
   can request them; use them to see whether special challenges are too hard or too easy.
3. Make descriptions **actionable** except for deliberately hidden/spoiler ones.
4. **Avoid missables** (one chance, no chapter select) or provide chapter select; a
   missable achievement forces full replays.
5. Avoid achievements requiring **dead or unreliable online modes** or co-op partners
   the player may not have.
6. **Difficulty spread:** a few easy ones in the first hour (players learn the system),
   most mid, a few very hard.
7. **Test unlock logic** in all edge cases (save/load, co-op, retroactive unlock for
   patches).

## Platform notes (check current docs; requirements change)
- Steam: achievements and stats are defined on the Steamworks Partner site. For
  achievements with progress bars, call `ISteamUserStats::IndicateAchievementProgress` at
  significant points to show a pop-up (the page's example: 10 of 20 wins).
- Xbox and PlayStation: each has its own achievement or trophy budget and certification
  rules; read the current platform documentation (not covered by the sources here).

## Gotchas
- Grind achievements trade player time for a checkbox; players resent them.
- Achievements that reward self-harming play (die 100 times) are jokes once, not five
  times.
- Difficulty-mode achievements that do not stack (must play on Hard and separately on
  Easy) force pointless replays.

## Checked

2026-11-09. Confirmed against the Steamworks Stats and Achievements page: global completion
percentages (client API and Community page) and `IndicateAchievementProgress`. Removed the
Gamerscore and trophy budget figures, the claim that most players never finish games, and the
Steam list-size remark; none is on the pages read. Category list and design advice are
judgement.
Method: documentation only; no commands were run.

## Verify
- [ ] Category mix covers progress, discovery, mastery and style.
- [ ] No missables without chapter select; no reliance on dead servers.
- [ ] Unlock logic tested including save/load and patches.
- [ ] Platform budget rules checked against current platform docs.
