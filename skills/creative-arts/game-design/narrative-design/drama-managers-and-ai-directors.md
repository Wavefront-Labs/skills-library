---
id: creative-arts.game-design.narrative-design.drama-managers-and-ai-directors
name: drama-managers-and-ai-directors
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, drama-manager, ai-director, adaptive-pacing, procedural-narrative, experience-management]
level: practitioner
status: draft
description: "Design a drama manager or AI director: tracking player intensity, build-up/peak/relax phases, storyteller event selection, and authoring content the director can schedule."
sources:
  - https://www.routledge.com/Procedural-Storytelling-in-Game-Design/Short-Adams/p/book/9781138595309
  - https://rimworldwiki.com/wiki/AI_Storytellers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drama managers and AI directors

**Goal:** a system that watches the play session and schedules events so pacing stays
dramatic regardless of what the player does.

## Two families
| Family | Examples | Selects |
|---|---|---|
| Pacing director | Left 4 Dead AI Director, Alien: Isolation's alien director | when and how much threat |
| Story manager | Facade's beat manager, RimWorld storytellers, storylet systems | which story event next |

## Left 4 Dead model (Mike Booth, 2009)
1. **Estimate intensity per player**: rises when damaged, incapacitated, or enemies die
   close by; decays over time.
2. **Adaptive dramatic pacing** cycles: *Build up* (spawn threats until intensity peaks),
   *Sustain peak* (a few seconds), *Peak fade* (stop new major threats), *Relax* (30-45 s
   of low threat, or until players move forward) then build again.
3. **Spawns outside view** along the remaining path (the "active area set").
Result: tension curves without hand-placed encounters.

## Story manager model
- Author **events** with preconditions, weights and cooldowns:
  ```
  event: raid  pre: colony_wealth > 5000, days_since_threat > 6
  weight: 1.0 * wealth_factor  cooldown_days: 5
  ```
- The **storyteller** picks events to match a target tension curve. RimWorld ships
  personalities: Cassandra Classic (steady escalation), Phoebe Chillax (long gaps),
  Randy Random (unweighted).
- Facade's drama manager chose the next dramatic beat to push a story-tension value along
  an Aristotelian arc, given beats' preconditions and tension effects.

## Designing one
1. Define the measurable proxy for drama (intensity, tension, wealth, time since event).
2. Draw the target curve and the rules for each phase.
3. Author content in reusable units with preconditions and effects on the proxy.
4. Expose tuning per difficulty or personality; let players pick a storyteller.
5. Log the proxy and chosen events per session; plot them against the target.

## Gotchas
- Directors that visibly react to the player (spawn right behind) feel like cheating;
  spawn out of sight and keep rules consistent.
- Too much smoothing removes memorable spikes; allow rare outliers.
- Content count bounds the system; a director with 10 events repeats fast.

## Verify
- [ ] Session logs show the proxy following the target curve.
- [ ] No event fires without its preconditions.
- [ ] Playtesters cannot easily predict the next event.
