---
id: creative-arts.game-design.systems-and-mechanics.session-length-design
name: session-length-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, session-design, core-loop, gameplay-loop, stopping-points, save-system, mobile-games, pacing, player-respect]
level: practitioner
status: draft
description: "Design a game around its target session length: natural stopping points, save and resume rules, loop sizes that fit the session, and a clean exit with a reason to return."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Session length design

**Goal:** the game fits the time players actually have, so sessions end at satisfying
points rather than when the bus arrives or the parent calls.

## 1. Set the target session
| Context | Typical target |
|---|---|
| mobile commute / casual | 2-10 minutes |
| handheld / roguelite run | 15-45 minutes |
| PC/console evening | 1-3 hours, with breaks every 20-40 min |
| board game | stated on the box; teach time counted separately |
Write the target and the minimum viable session (shortest meaningful play).

## 2. Size loops to fit
- **The core loop must complete several times per minimum session.** If one loop takes
  15 minutes and sessions are 5, players never finish a loop.
- **A meaningful milestone per typical session** (a level, a run, a day in-game).
- **Meta progress visible at session end** (XP bar, unlocked item) so stopping feels
  like banking, not abandoning.

## 3. Build stopping points
- Natural ends: end of level/run/day/chapter, return to hub.
- Signposted by the fiction ("night falls; rest?") or UI (summary screen).
- Put stopping points *after* a resolution and *before* a new hook, so the player
  leaves satisfied and returns curious.

## 4. Save and resume rules
- Mobile: save state continuously; the OS can kill the app at any time. Resume to the
  exact moment, or to a recent point with a recap.
- Long games: autosave at every stopping point; quit anywhere with at most a few minutes
  lost. Show when the game last saved.
- Board games: provide a save/pack-up method for long or campaign games (bags, save
  sheets).

## 5. Test it
Measure real sessions (telemetry or playtest diaries): where do people quit? If quits
cluster mid-loop, the loop is too long or the stopping point is missing.

## Gotchas
- **Artificially extending sessions** (no save mid-level, long unskippable sequences)
  converts frustration into churn.
- Board game box times are notoriously optimistic; time 5 real groups including teach.
- "One more turn" designs are powerful; pair them with explicit stopping cues so players
  do not resent the game.

## Verify
- [ ] Target and minimum session written.
- [ ] Core loop completes multiple times in the minimum session.
- [ ] Stopping points and save behaviour specified.
- [ ] Quit-point data or diaries checked against the plan.
