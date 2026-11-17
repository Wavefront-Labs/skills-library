---
id: creative-arts.animation.editing.match-frame-and-reverse-match
name: match-frame-and-reverse-match
category: creative-arts
field: animation
product: editing
tags: [match-frame, reverse-match-frame, find-in-timeline, source-monitor, trimming, premiere-pro, resolve, avid, version-swap]
level: practitioner
status: draft
description: "Use match frame and reverse match frame to jump between a timeline frame and its source, swap shot versions frame-accurately and find where a frame is used."
sources:
  - https://helpx.adobe.com/premiere-pro/using/keyboard-shortcuts.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://kb.avid.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Match frame and reverse match frame

**Goal:** move instantly between "this frame in the cut" and "this frame in the source clip", in both directions.

## Keys

| NLE | Match frame (timeline to source) | Reverse match (source to timeline) |
|---|---|---|
| Premiere Pro | **F** (loads source at the same frame, with in/out marked) | **Shift+R** |
| Resolve | **F** (loads source in the Source viewer) | Shift+F in the Source viewer finds the frame in the timeline |
| Avid | Match Frame button (assign to a key); Alt/Option+Match Frame matches without marks | Reverse Match Frame button |

Track targeting matters: the match uses the topmost selected/targeted track at the playhead, so a title on V2 matches
the title, not the shot under it.

## Animation uses

- **Version swap at an exact frame:** match frame the old shot, open the new version in the source monitor at the
  same timecode (renders carry shot-relative timecode), and overwrite with marks to replace it frame-accurately.
- **Recovering a trimmed action:** match frame, then extend the source out point to see what frames exist past the
  cut, which tells you whether a trim request needs new animation.
- **Where else is this used:** reverse match frame from a board or a stock element to find each use in the cut
  before replacing it.
- **Notes back to departments:** match frame gives the shot's own frame number for a note (shot frame 1042) rather
  than episode timecode.

## Gotchas

- Clips with speed changes or nested sequences match into the nest or to a remapped frame; check the source
  frame shown versus the expected one (see `creative-arts.animation.editing.time-remap-speed-changes`).
- Renders without embedded timecode all start at 00:00:00:00 and frame-accurate swaps silently drift; insist that
  renders carry timecode.

## Verify

After a version swap via match frame, toggle between old and new on the same frame: animation poses line up and the
following edit has not moved.
