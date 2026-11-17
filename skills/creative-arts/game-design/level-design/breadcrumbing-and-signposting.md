---
id: creative-arts.game-design.level-design.breadcrumbing-and-signposting
name: breadcrumbing-and-signposting
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, breadcrumbing, signposting, player-guidance, wayfinding, landmarks]
level: practitioner
status: draft
description: "Guide players through levels with breadcrumbs and signposts: pickups, light, colour, landmarks, NPC and sound cues, and testing where players get lost."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.gamedeveloper.com/design/level-design-guiding-the-player
  - https://www.gdcvault.com/play/1015515/Level-Design-in-a-Day
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Breadcrumbing and signposting

**Goal:** players always have a next place to go, found by looking, not by a waypoint.

## Toolkit (from subtle to explicit)
| Cue | Example |
|---|---|
| Breadcrumb pickups | coins, ammo, collectibles laid along the path |
| Light | lit doorway in a dark area, light pools on the route |
| Colour language | yellow paint on climbable ledges, consistent accent colour |
| Landmarks (weenies) | tall distant structure visible from many points |
| Leading lines | rails, cables, roads, architecture pointing to the goal |
| Motion | birds taking off, NPCs running, flags flapping |
| Sound | music, voices, machinery from the right direction |
| Framing | doorways and arches that frame the next goal |
| Signposts | diegetic signs, graffiti arrows, maps on walls |
| UI | compass, waypoints, objective markers (last resort, often optional) |

## Procedure
1. Mark every decision point on the map; at each, list the cue that tells the player the way.
2. Use at least two cue types at critical decision points (light + motion).
3. Place a landmark visible from the start of each major area.
4. Keep one visual language across the game; teach it early in a safe space.
5. Test with first-time players; record where they pause or backtrack.

## Gotchas
- Overused yellow paint feels patronising; integrate it into the art.
- Breadcrumbs that also lead to secrets confuse the critical path; separate their look.
- Dark levels hide signposts; check at minimum brightness settings.

## Verify
- [ ] Every decision point has a listed cue.
- [ ] Landmark visible at each area start.
- [ ] Lost-player hotspots from playtests resolved.
