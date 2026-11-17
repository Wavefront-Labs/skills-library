---
id: creative-arts.animation.editorial.cutting-in-shots
name: cutting-in-shots
category: creative-arts
field: animation
product: editorial
tags: [cut-in-shots, editorial-department, editorial-workflow, version-up, layout-cut-in, animation-cut-in, latest-versions, conform-to-latest, progress-reel]
level: practitioner
status: draft
description: "Keep the edit current by cutting in layout, animation and lighting versions over boards as they're approved, tracking department status per shot in the timeline."
sources:
  - https://opentimelineio.readthedocs.io/en/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cutting in shots

**Goal:** the edit always shows the most advanced approved version of every shot, so the director watches
the film as it actually is, and timing problems surface while they are cheap to fix.

## Track layout for a living edit

| Track | Content |
|---|---|
| V1 | boards/animatic (always complete) |
| V2 | layout versions |
| V3 | animation (blocking, then final) |
| V4 | lighting/comp finals |
| V5 | temp graphics, burn-ins |
Higher tracks cover lower ones, so the viewer sees the most advanced department per shot automatically.

## Procedure

1. Department delivers a version with the same frame range as the turnover (`creative-arts.animation.editorial.editorial-turnover`).
2. Editor imports and places it on the department's track, aligned to the shot's cut-in frame (use the burn-in
   frame number or the clip's timecode, set from the work range).
3. Colour-label clips by status (approved, in review, WIP) for screenings.
4. If the shot's animation changed timing (held longer, action earlier), flag it: either trim to fit and send
   notes, or propose a recut.

## Automating version updates

Script the swap: read the tracker for the latest approved version per shot and update clip media references in
an OTIO export of the timeline, then re-import (or use NLE-specific scripting: Resolve's Python API, Avid's
bin relinks via AMA/naming). Many studios generate a "progress reel" nightly this way.

## Gotchas

- A department version longer than the cut (handles included) must be placed so the cut frames line up, not
  the file's first frame.
- Frame rate mismatches between rendered versions and the timeline cause slow drift.
- Don't let unapproved versions into screening reels unless labelled.

## Verify

Play a sequence: each shot shows the latest approved department version, no flash frames between shots, and
the tracker status matches the timeline labels.
