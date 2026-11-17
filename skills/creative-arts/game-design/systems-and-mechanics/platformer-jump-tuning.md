---
id: creative-arts.game-design.systems-and-mechanics.platformer-jump-tuning
name: platformer-jump-tuning
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, jump-tuning, coyote-time, jump-buffering, variable-jump-height, game-feel, platformer, gravity, apex-hang, celeste]
level: advanced
status: draft
description: "Tune a platformer jump from designer terms (height, time to apex) instead of raw gravity, plus coyote time, jump buffering, variable height and apex hang."
sources:
  - https://www.youtube.com/watch?v=hG9SzQxaCm8
  - https://maddythorson.medium.com/celeste-and-towerfall-physics-d24bd2ae0fc5
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Platformer jump tuning

**Goal:** a jump that feels precise and forgiving, specified in terms designers can
reason about, with the invisible assists modern platformers use.

## Parameterise by height and time
Kyle Pittman's GDC 2016 talk "Math for Game Programmers: Building a Better Jump" derives
gravity and launch velocity from the designer's desired jump height `h` and time to
apex `t_h`:
```
g  = 2*h / t_h^2          # gravity (downwards)
v0 = 2*h / t_h            # initial jump velocity (upwards)
```
Designers set `h` (e.g. 3 tiles) and `t_h` (e.g. 0.35 s); gravity follows. Use a
**higher gravity on the way down** (e.g. a separate t_h for the fall) for a snappier,
less floaty arc.

## Assists (each typically a few frames)
| Assist | What it does |
|---|---|
| Coyote time | allow jumping for a short window after walking off a ledge |
| Jump buffering | if jump is pressed shortly before landing, jump on landing |
| Variable jump height | releasing jump early cuts upward velocity (e.g. multiply by a factor or apply extra gravity) |
| Apex hang | reduce gravity near the apex for better air control |
| Corner correction | nudge the player around a ceiling corner they barely clip |
| Max fall speed | clamp fall velocity for readability |
Maddy Thorson's write-up of Celeste and TowerFall physics describes several of these
(coyote time, jump buffering, halved gravity at the apex while jump is held, corner
correction). The exact frame values are per-game tuning.

## Procedure
1. Choose `h` and `t_h` from level metrics (gap widths, ledge heights) - see
   `creative-arts.game-design.level-design.player-metrics-and-grid`.
2. Implement height/time-based parameters; expose them in a tuning panel.
3. Add coyote time and buffering first (largest perceived improvement).
4. Add variable height, then apex hang and corner correction.
5. Test: record players failing jumps; if failures happen at ledge edges or on landing
   presses, increase the corresponding window.

## Gotchas
- Assist windows measured in frames change with framerate; use time, fixed timestep.
- Too-large coyote time enables double-jump-like exploits off ledges; keep windows small.
- Changing jump parameters after levels are built breaks level metrics; lock metrics
  early.

## Verify
- [ ] Jump specified as height + time to apex; gravity derived.
- [ ] Coyote time and buffering implemented and tuned.
- [ ] Jump arcs match level metrics (gap and height tables).
- [ ] Playtest edge-failures reduced after assists.
