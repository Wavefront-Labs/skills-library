---
id: creative-arts.game-design.playtesting-and-balance.usability-testing-for-games
name: usability-testing-for-games
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting, usability-test, games-user-research, task-based-testing, think-aloud, onboarding, ux-research, severity-rating, playtest-script]
level: practitioner
status: draft
description: "Run a game usability test: define tasks and success criteria, recruit fresh players, observe with think-aloud, log issues with severity, and report fixes ranked by impact."
sources:
  - https://www.nngroup.com/articles/usability-testing-101/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Usability testing for games

**Goal:** find where players fail to understand or operate the game (controls, UI,
onboarding, objectives) as distinct from whether they enjoy it.

*Games User Research* (Drachen, Mirza-Babaei, Nacke, eds.) separates usability (can
players do what they intend?) from experience (do they feel what the designer intends?).
Usability testing targets the former.

## Plan
1. **Research questions:** "Can new players complete the first mission without help?"
   "Do players find the crafting menu?"
2. **Tasks and success criteria:** e.g. "equip the new weapon" - success = done within
   2 minutes without help.
3. **Participants:** fresh players matching the target audience (see recruitment);
   around 5 per round finds many major issues (Nielsen's common guidance), then iterate
   and test again.
4. **Setup:** record screen + face + controller/hands if possible; a moderator script.

## Run
- Brief: "We're testing the game, not you. Please think aloud."
- Give tasks only as goals, never as instructions ("You want to change your weapon"
  not "Open the inventory with Tab").
- **Don't help** unless the participant is stuck beyond a threshold; note the stuck
  point, then help and continue.
- Log observations live with timestamps.

## Analyse
1. List issues with: description, frequency (how many participants), severity, evidence
   (timestamp).
2. Severity scale (example): critical (blocks progress), major (significant delay or
   error), minor (annoyance), cosmetic.
3. Rank by severity x frequency; propose fixes.
4. Report concisely: top issues, clips, recommended fixes.

## Gotchas
- Developers watching live tend to explain; keep them in an observation room or muted.
- Experienced testers (internal staff, frequent testers) are not fresh; use new
  participants each round.
- Usability problems found by 1 of 5 participants can still be serious; judge severity.

## Verify
- [ ] Tasks with success criteria written before sessions.
- [ ] Fresh participants matching the audience.
- [ ] Issue log with severity and frequency.
- [ ] Fixes re-tested in a follow-up round.
