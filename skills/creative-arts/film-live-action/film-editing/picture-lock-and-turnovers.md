---
id: creative-arts.film-live-action.film-editing.picture-lock-and-turnovers
name: picture-lock-and-turnovers
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, editor, assistant-editor, picture-lock, lock, turnover, turnovers, aaf, omf, edl, xml, fcpxml, change-list, change-lists, reel-breaks, reel-balancing, conform, online, finishing, sound-turnover, music-turnover, vfx-turnover, vfx-pull, handles, 2-pop, leader, countdown, slate, reference-movie, qt-ref, burn-ins, timecode, frame-accuracy, track-layout, dialogue-split, mix-track, iso-tracks, consolidate, media-manager, relinking, locked-cut-naming, turnover-prep, reel-breaks-prep, sound-turnover-aaf, aaf-export-settings, reference-quicktime, colour-turnover, edl-export, vfx-pull-list, change-list-generation, reconform-process]
level: practitioner
status: draft
description: "Lock the picture and turn it over cleanly: reels and 2-pops, AAF/OMF for sound and music, EDL/XML for conform and colour, VFX pulls with handles, reference movies, change lists when the lock moves."
sources:
  - "https://www.editorsguild.com/ (Motion Picture Editors Guild - turnover practice)"
  - "https://avid.secure.force.com/pkb/ (Avid - AAF export, change lists, EDL)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Resolve conform from AAF/XML/EDL)"
  - "https://www.netflixstudios.com/ (Netflix post-production turnover guidelines)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Picture lock and turnovers

**Goal:** sound, music, VFX and colour all start from the same frame-accurate cut and
can find every frame of media it uses - and when the lock changes (it will), everyone
updates without re-doing their work.

## 1. Before lock
- Agree **reel structure** (features: reels of ~18-20 min, breaks on hard cuts with no
  music/dialogue across the break; TV: act breaks) and **frame rate/timecode** start
  (01:00:00:00 for reel 1, 02:00:00:00 for reel 2...).
- Sequence hygiene: one video track of the cut (collapse/flatten effects into a V1 cut
  where possible, keep temp VFX on V2 labelled), audio tracks laid out by type.
- All temp items labelled: `TEMP_VFX_`, `TEMP_MUSIC_`, `TEMP_SFX_`; missing shots as
  slugs with text.
- **Leader**: 8 seconds of head leader with a **2-pop** (one frame of 1 kHz tone with
  a flash frame, 2 seconds before first frame of action, FFOA) and a tail pop 2 s after
  LFOA. Sound and colour sync to the pops.
- A picture lock means **no frame changes**; trims after lock are "lock+1" with change lists.

## 2. Reference movie
Export a ProRes/H.264 reference of each reel with **burn-ins**: sequence timecode,
source clip name/timecode, reel/version, and audio (the editor's temp mix). Everyone
checks their work against it. Name: `SHOW_R1_v12_LOCK_2026-10-15.mov`.

## 3. Sound turnover (AAF/OMF)
- **AAF** (preferred; OMF is legacy with a 2 GB limit) with **embedded media**,
  **handles of 48-96 frames (2-4 s)**, all audio tracks, no effects baked (or a note of
  what is). Export from the locked sequence, reel by reel, from first frame of leader.
- Track layout the sound editor expects: dialogue tracks (split by character or by
  mic/ISO), production effects, temp SFX, temp music, VO - each labelled. If the edit
  used the mix track, supply **ISOs**: the assistant relinks the ISO channels to the
  cut (Resolve/Avid can swap channels; or deliver original poly WAVs plus an EDL).
- Also deliver: the reference movie, the **EDL per track** for conform checks, the
  script supervisor's sound reports, and a **cue sheet / notes** of what temp sound the
  director loved (so sound design knows the intent).
- Music: a separate AAF of music tracks and a document of temp cues with timecodes for
  the composer/music editor.

## 4. Picture conform turnover (EDL/XML/AAF)
- For colour/online: **EDL (CMX3600)** per video track with source clip names and
  reel names matching the camera originals, or **XML/FCPXML/AAF** carrying speed
  changes and reframes. Flatten nested sequences; remove effects the conform can't read
  (note them in a list). Resolve: *File > Import Timeline*, check with a **conform
  offline reference** overlay against the reference movie.
- Supply the **camera originals' locations** (drive list) or a consolidated media
  export with handles (Avid consolidate/transcode; Premiere Project Manager; Resolve
  Media Management) - the online needs full-resolution media, not the offline proxies.
- Note reframes, speed ramps, flops, split screens, temp VFX positions and any burned
  LUT in the offline so the colourist can reproduce intent.

## 5. VFX turnover
A **VFX pull list** per shot: shot ID (`SC012_0010`), source clip, source timecode in/out
**with handles (typically 8-24 frames each side)**, cut in/out, plate requirements,
description and the reference frame. VFX vendor pulls plates from originals (EXR/DPX or
RAW) via EDL; returns comps named to the shot ID to be cut in. Lock VFX shot lengths
first; they are the most expensive thing to change.

## 6. When the lock moves: change lists
Any post-lock edit produces a **change list** (Avid Change List tool, Resolve/Premiere via
comparison tools or EDL diff): per reel, insert/delete/move with old and new timecodes
and durations. Send to sound, music, VFX and colour with a new reference movie and
version number. Keep changes bundled (weekly, not hourly); rebalance reels only if the
change crosses a break.

## Gotchas
- Handles too short for sound (dialogue editors need room for fades and alternates).
- AAF with linked media that can't be found at the sound house.
- Reel names in the EDL not matching camera reel names; the conform relinks nothing.
- Picture "locked" but the leader/2-pop missing or at different offsets per reel.
- Change lists sent as "just re-export everything" - every department re-conforms by hand.

## Verify
- [ ] Reels with leaders, 2-pops and consistent start timecodes; reference movie with burn-ins exported.
- [ ] Sound AAF embedded with 2-4 s handles, labelled tracks, ISOs available.
- [ ] Conform EDL/XML relinks to camera originals in a test before sending.
- [ ] VFX pull list with handles; change-list process agreed and version-numbered.
