---
id: creative-arts.game-design.playtesting-and-balance.funnel-and-drop-off-analysis
name: funnel-and-drop-off-analysis
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, funnel-analysis, drop-off, retention, analytics, telemetry, conversion]
level: practitioner
status: draft
description: "Instrument a game's key steps as a funnel, read step-to-step drop-off by cohort, and decide whether a leak is a design, onboarding, or tracking problem before changing anything."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Funnel and drop-off analysis

**Goal:** find where players stop progressing (tutorial, first purchase, level 3, first multiplayer match) and why.

## Procedure
1. **Define an ordered list of steps** that every intended player passes: install, first launch, tutorial start, tutorial end, first level end, and so on. Each step is one logged event with a stable name, a player/session ID, a timestamp, and a build version.
2. **Count unique players reaching each step** within a fixed window per cohort (for example, by install week or build). Step conversion = players at step n / players at step n-1; overall = last step / first.
3. **Compare cohorts** by build, platform, acquisition source and region. A drop that appears only in one cohort usually points to a bug or a channel mismatch, not game design.
4. **Rank leaks** by absolute players lost, not only by percentage; a 40 percent loss of a tiny step matters less than 10 percent at the front door.
5. **Diagnose with qualitative data:** replay sessions, run a usability test on that exact step, read support tickets. The funnel says where, never why.
6. **Change one thing, re-measure** on the next cohort. Where you can randomise, use an A/B test instead of before/after comparison.

## Gotchas
- Missing or double-firing events fake drop-offs; validate events with a dev account before launch.
- Steps that players can skip or reorder break a strict funnel; model them as separate funnels.
- Time windows: players who return the next day are not lost, so state the window.
- Small samples: do not read single-digit-percent changes from a few hundred players.

## Verify
- [ ] Every step event fires exactly once per qualifying player in a test run.
- [ ] Funnel compared across at least two cohorts.
- [ ] Each action taken is tied to a measured leak and a re-measurement.
