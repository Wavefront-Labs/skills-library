---
id: creative-arts.animation.editorial.animatic-shot-breakdown
name: animatic-shot-breakdown
category: creative-arts
field: animation
product: editorial
tags: [shot-breakdown, editorial-department, editorial-workflow, shot-numbering, frame-counts, handles, shotlist, edl-to-shotlist, animatic]
level: practitioner
status: draft
description: "Break a locked animatic into numbered shots with frame counts, handles and descriptions, and export the breakdown as the production's shot list."
sources:
  - https://opentimelineio.readthedocs.io/en/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animatic shot breakdown

**Goal:** turn the locked story reel into the list of shots the rest of production builds: every shot
numbered, timed to the frame, with handles and a description, so layout, animation, scheduling and the
tracker all agree.

## Numbering

- Sequence + shot: `sq020_sh010`, increment by 10 (sh010, sh020...) so inserted shots get sh015 without
  renumbering.
- Never reuse a number after a shot is cut; mark it omitted ("OMIT") in the tracker.
- Episode prefix for series: `ep104_sq020_sh010`.

## Per shot record

| Field | Example |
|---|---|
| Shot ID | ep104_sq020_sh010 |
| Cut in / out (record timecode) | 00:02:13:04 - 00:02:16:12 |
| Frame count (cut length) | 80 |
| Handles | 8 head / 8 tail (if the show uses them) |
| Work frame range | 1001-1096 (1001 + head handle start) |
| Description / action | "Mia turns, sees the door open" |
| Dialogue | line IDs in the shot |
| Camera / FX notes | pan left, rain FX |
| Characters, props, set | for asset breakdown and casting |

## Exporting from the NLE

Mark each shot as a separate clip/board segment on one video track, add shot names as clip names or markers,
then export an EDL/XML/OTIO and convert to the shot list:
```python
import opentimelineio as otio
tl = otio.adapters.read_from_file("ep104_animatic_lock.otio")   # or .edl / .xml via adapters
fps = 24
for clip in tl.tracks[0].each_clip():
    r = clip.range_in_parent()
    start = otio.opentime.to_frames(r.start_time, fps)
    dur = otio.opentime.to_frames(r.duration, fps)
    print(f"{clip.name},{start},{dur}")
```
Load into the tracker (`creative-arts.animation.pipeline.production-tracking`) and the shot list JSON.

## Gotchas

- Boards held across a cut in the animatic produce one clip covering two shots; split them in the edit first.
- Frame counts must use the show rate; a 25 fps project exported at 24 changes every count.
- Lock means locked: later edits go through a change list (`creative-arts.animation.editorial.editorial-change-lists`).

## Verify

Sum of shot frame counts equals the sequence length in the edit; every shot in the edit appears once in the
breakdown and in the tracker.
