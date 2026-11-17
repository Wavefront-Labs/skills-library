---
id: creative-arts.film-live-action.cinema-cameras.slating-protocol-and-smart-slates
name: slating-protocol-and-smart-slates
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, slate-protocol, tail-slate, mos-slate, smart-slate-setup, timecode-slate, slate-display, take-numbering, scene-take-convention, pickup-numbering, clapperboard, second-ac]
level: practitioner
status: draft
description: "Slate like a 2nd AC: what goes on the board, scene/set-up/take numbering (US and UK systems), tail slates, MOS, multi-camera, pickups, and syncing a timecode smart slate."
sources:
  - "https://www.denecke.com (Denecke - timecode slates TS-3/TS-C manuals)"
  - "https://ambient.de (Ambient - Lockit slate and ACN)"
  - "Pat P. Miller, Script Supervising and Film Continuity (scene and take numbering)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slating protocol and smart slates

**Goal:** every take identifiable and syncable - so assistant editors never guess.

## 1. What's on the board
Production title, director, DP, **roll** (camera card/mag, e.g. A012), **scene**,
**take**, date, frame rate, camera letter, MOS/sync, **INT/EXT, DAY/NIGHT**, and filter/
lens if the production wants. Update every take.

## 2. Numbering conventions
- **US (scene-based)**: scene 24, set-ups `24`, `24A`, `24B`... (skip I and O, often S and
  Z to avoid confusion), takes 1, 2, 3. Added scenes from the script (`24A` as a scene)
  are written `A24` by some productions to avoid collision - follow the script
  supervisor.
- **UK (slate-number)**: a running **slate number** for each set-up (e.g. slate 147) and
  takes, with the scene number also written.
- **Pickups**: `PU` added (e.g. 24B take 3 PU) when starting mid-scene; **series**
  (multiple takes without cutting) marked `SER`.
- Agree with the script supervisor on day one; their log and your slate must match.

## 3. Procedure
1. Hold the slate in frame, in focus (or as close as possible), legible; for wide
   shots near the lens and then move.
2. Announce: "Scene twenty-four Bravo, take three, A mark" (and "B mark" for second
   camera). Use phonetic letters.
3. Clap cleanly with the sticks visible; leave frame quickly.
- **Tail slate**: slate held **upside down** at the end of the take (when a head slate was
  impossible), announced "tail slate", clap.
- **MOS**: no sound - hold the sticks open (or fingers between them), no clap; write MOS.
- **Soft sticks**: gentle clap for close-ups near actors.
- **Multi-camera**: one common slate for all cameras if possible, otherwise A mark, B mark
  in sequence; "common mark" if both see it.
- **Second sticks** if the first clap was missed.

## 4. Smart (timecode) slates
- **Jam** the slate's timecode from the master clock (sound recorder or Tentacle/ Lockit)
  - via cable or wireless (Denecke/Ambient support; check frame rate setting matches).
- Display shows running timecode; it **freezes** when the sticks close, so the assistant
  editor can read sync even without audio.
- Re-jam at lunch and after battery changes; check drift against the recorder.
- Brightness settings for day/night; keep the battery fresh.

## Gotchas
- Slate numbering differing from the script supervisor's log.
- Clap out of focus or out of frame.
- Smart slate at 25 fps on a 23.976 shoot.
- Tail slates not announced; editors miss them.

## Verify
- [ ] Numbering system agreed with the script supervisor.
- [ ] Board updated every take; roll matches the card.
- [ ] Tail, MOS and multi-camera procedures followed.
- [ ] Smart slate jammed at the right rate and re-jammed regularly.
