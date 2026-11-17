---
id: creative-arts.game-design.narrative-design.quest-log-and-objective-markers
name: quest-log-and-objective-markers
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, quest-log, objective-markers, journal-design, waypoints, quest-tracking, ui-design]
level: practitioner
status: draft
description: "Design the quest log and objective markers: entry structure, tracked vs untracked quests, marker modes, compass and map pins, and guidance without autopiloting play."
sources:
  - https://gameaccessibilityguidelines.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quest log and objective markers

**Goal:** a player returning after a week can tell in 10 seconds what they were doing and
where to go, without markers turning exploration into following an arrow.

## Quest log entry structure
1. **Title** (memorable, unique).
2. **Current objective** as one imperative line: "Find the miller's daughter at the old mill."
3. **Optional counter / sub-steps**: "Rats cleared 7/12".
4. **Journal summary** of what happened so far, written from the character's perspective
   and updated per step (this is what fixes the "returning player" problem).
5. **Giver, location, recommended level, rewards** if the genre uses them.
6. Categories: main, side, faction, completed, failed. Sort tracked quest to the top.

## Marker modes (pick per game, ideally a player option)
| Mode | Behaviour | Fits |
|---|---|---|
| Full guidance | world marker + distance + map pin | action games, players with low time |
| Region only | map circle, no exact pin | open-world exploration |
| Directions | text cues ("north of the river, past the twin pines") | Morrowind / Elden-style exploration |
| Off | log text only | immersion-focused players |

Breath of the Wild and Ghost of Tsushima show diegetic alternatives: player-placed pins,
wind direction pointing to the tracked objective.

## Procedure
1. Choose a default marker mode from the design pillars; make others options in settings.
2. Write every objective line so it works with markers off (names a landmark, not a coordinate).
3. Place markers on the objective's entrance, not its internal point, for multi-floor interiors.
4. Update the marker the moment the objective changes; stale markers are the top
   source of "where do I go" reports.
5. Provide a single tracked quest on the HUD; allow several on the map.

## Gotchas
- Distance readouts for vertically stacked objectives mislead; show an up/down indicator.
- Markers through walls make players path into dead ends; route to the door or show a path line.
- Journal text written as developer notes ("Talk to NPC_04") breaks immersion and localisation.

## Verify
- [ ] With markers off, a tester can complete three quests from log text alone.
- [ ] Every objective change updates log, HUD and map in the same frame.
- [ ] Returning-player test: tester recalls goal from the journal summary.
