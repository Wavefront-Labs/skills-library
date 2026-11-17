---
id: creative-arts.music.composition.hit-points-and-tempo-mapping-to-picture
name: hit-points-and-tempo-mapping-to-picture
category: creative-arts
field: music
product: composition
tags: [composition, film-scoring, media-composition, hit-points, tempo-mapping-to-picture, click-track-calculation, frame-rate, sync-to-picture]
level: advanced
status: draft
description: "Catch picture hit points by choosing tempos and meter changes so key frames land on beats, using frame-click math and DAW tempo maps."
sources: ["Fred Karlin and Rayburn Wright, On the Track (2nd ed., Routledge)", "Richard Davis, Complete Guide to Film Scoring (Berklee Press)", "https://cuebase.de/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hit points and tempo mapping to picture

**Goal:** important picture events (cuts, punches, reveals) land on musically strong
places without the music sounding pushed around.

## 1. Mark the hits
- In the DAW, place markers at each hit point from the cue's spotting notes, at the
  exact frame. Note whether the hit is **hard** (must land on the frame) or **soft**
  (anywhere within a few frames is fine).
- Express each hit as seconds from cue start: `t = (hit_TC - start_TC)` in seconds.

## 2. Find a tempo that catches them
Beat number of a hit: `beat = t * BPM / 60`. You want hits near whole (or half) beats.
- Try candidate tempos and check the fractional part of each hit's beat number.
- Classic frame-click method: a click of **n frames per beat** at 24 fps gives
  `BPM = 1440 / n` (e.g. 12-frame click = 120 BPM, 18-frame = 80). Tools like CueBase or
  the DAW's "fit tempo to marker" do this search for you.
- Free-timing cues (no click) use **streamers and punches** for the conductor instead.

## 3. Tempo maps when one tempo cannot catch everything
- Add a **meter change** (a 2/4 or 3/4 bar) before a hit to move it onto a downbeat -
  often less audible than a tempo change.
- Use small tempo changes (a few BPM) at phrase boundaries, or a gradual ramp over
  bars. Large jumps mid-phrase are audible.
- In Logic/Cubase/Pro Tools, lock markers to SMPTE position so moving tempo does not
  move the hit.

## 4. Musical placement
- Land on the beat **just before** a cut as often as on it; anticipation reads as sync.
- A hit does not have to be loud: a harmony change, a new instrument or silence works.

## Gotchas
- Picture at 23.976 vs 24: the difference is 0.1%, about 3.6 s per hour; confirm the
  session rate before calculating.
- Too many hard hits makes music sound like Mickey-Mousing; catch the important ones.
- Re-cuts move hits: keep markers SMPTE-locked and re-check after every new turnover.

## Verify
- [ ] All hard hits land within one frame of a strong beat or event.
- [ ] Tempo changes sit at phrase boundaries and are not audible as lurches.
- [ ] Click track exported with the tempo map for the recording session.
