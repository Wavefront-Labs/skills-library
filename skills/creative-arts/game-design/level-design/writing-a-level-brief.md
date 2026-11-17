---
id: creative-arts.game-design.level-design.writing-a-level-brief
name: writing-a-level-brief
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, level-design-document, level-brief, one-pager, level-overview, documentation, preproduction]
level: practitioner
status: draft
description: "Write a level brief (level design one-pager): purpose, player state in and out, mechanics and enemies, beats, setting references, map sketch and success criteria."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a level brief

**Goal:** a short document that aligns design, art, audio, narrative and code on what a
level is for before blockout starts.

## Template
```
LEVEL NAME / ID
PURPOSE            what this level does in the game (teach dash, story turn, climax)
PLAYER IN          abilities, items, level/power expected on entry
PLAYER OUT         what they gain (ability, story knowledge, item)
MECHANICS          new / developed / tested
ENEMIES            types, new introductions
BEATS              short beat list with intensity (see level-beat-charts-and-intensity)
SETTING            location, time of day, mood, 3-5 reference images
NARRATIVE          story beats, characters met, environmental storytelling notes
MAP SKETCH         top-down sketch with critical path, optional areas, checkpoints
METRICS            special metrics (new traversal) if any
LENGTH             target play time (first-time player)
SUCCESS CRITERIA   e.g. 80% of testers use the new mechanic unprompted
RISKS              tech, art, scope concerns
```

## Procedure
1. Fill it from the game-level beat chart and narrative outline.
2. Review with leads (art, narrative, audio, code) in one meeting; capture changes.
3. Keep the brief **current during production**; it becomes the reference for
   playtest goals and bug triage ("does this serve the purpose?").
4. Attach the brief to the blockout review so feedback is judged against it.

## Gotchas
- Briefs that describe only the setting (mood boards) without purpose or mechanics
  leave designers guessing.
- Over-detailed briefs (room-by-room scripts) kill iteration; keep it to one or two
  pages and let blockout answer details.
- Length targets are for first-time players; designers play much faster.

## Verify
- [ ] Brief fits on 1-2 pages with a map sketch.
- [ ] Purpose, player in/out and success criteria stated.
- [ ] Reviewed by each discipline lead.
