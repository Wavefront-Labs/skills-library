---
id: creative-arts.game-design.level-design.death-and-path-heatmaps
name: death-and-path-heatmaps
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, level-heatmap, death-heatmap, telemetry, gameplay-analytics, position-tracking, level-iteration, data-visualisation]
level: practitioner
status: draft
description: "Instrument levels to log deaths, positions and events, render heatmaps over the level map, and read them to find difficulty spikes, dead zones and confusing routes."
sources:
  - https://www.gdcvault.com/
  - https://docs.unity3d.com/Manual/UnityAnalytics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Death and path heatmaps

**Goal:** see where players actually go, die, stall and quit in a level, overlaid on the
map, to drive layout and tuning changes with evidence.

## What to log (per event)
| Event | Fields |
|---|---|
| position sample | session id, level id, build, timestamp, x/y/z (every N seconds) |
| death | position, cause (enemy type, hazard, fall), time since checkpoint |
| quit | position, time in level |
| interaction | object id, position |
| objective reached | id, time |
Always log the **build version**; heatmaps across layout changes are meaningless.

## Rendering
1. Export a **top-down orthographic image** of the level with known world-to-pixel
   mapping (bounds and scale).
2. Bin positions into a grid (e.g. 1-2 m cells) and colour by count (log scale helps
   with skewed data).
3. Separate layers: deaths by cause, paths, stall time (time spent per cell), quits.
4. For multi-floor levels, slice by height band.
A notebook with pandas and matplotlib (`hist2d` or `hexbin` over the map image) is
enough; engines and analytics services offer built-in heatmaps too.

## Reading heatmaps
| Pattern | Likely cause |
|---|---|
| death cluster at one spot | spike, unclear hazard, bad checkpoint |
| deaths spread evenly | fine (challenge is distributed) |
| empty area on intended path | players don't find it or skip it |
| high stall time | confusion, missing guidance |
| path loops back and forth | lost players |
| quits near a cluster | frustration point |

## Procedure
1. Add logging before external playtests; verify coordinates with a test session
   (walk known routes).
2. Collect enough sessions to see patterns (a dozen-plus for internal tests; more for
   live data).
3. Generate layers, annotate findings, make changes, compare next build.

## Gotchas
- Small samples mislead; one tester's 30 deaths can dominate.
- Privacy: telemetry from real players needs consent/notice per law and platform rules.
- Heatmaps show *where*, not *why*; pair with observation or video.

## Verify
- [ ] Event schema includes build version and cause fields.
- [ ] Coordinates validated against a known route.
- [ ] Heatmap layers generated per build and reviewed with annotations.
