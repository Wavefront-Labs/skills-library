---
id: creative-arts.film-live-action.film-editing.matching-cameras-and-audio-in-multicam
name: matching-cameras-and-audio-in-multicam
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, multicam-colour-match, multicam-audio, camera-matching-multicam, multicam-sync, audio-follows-video, multicam-grading, mixed-cameras]
level: practitioner
status: draft
description: "Make multicam angles cut together: matching colour across mismatched cameras before and after the cut, choosing the audio source, audio-follows-video, and sync drift fixes."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve - multicam clips and Color Match)"
  - "https://helpx.adobe.com/premiere-pro/using/edit-multi-camera-sequences.html (Adobe Premiere Pro - multi-camera editing)"
  - "https://www.avid.com/media-composer (Avid - group clips and multicam)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matching cameras and audio in multicam

**Goal:** a multicam edit where switching angles never jumps in colour or sound.

## 1. Before you cut: normalise angles
- If cameras differ (A Venice, B FX6, C GoPro), apply input transforms/LUTs per camera
  so each is in the same display space (Rec.709 or the show LUT).
- Quick match: shoot a **chart on every camera** at the start; in Resolve use **Color
  Match** on the chart, or match by eye with scopes; apply per camera source (in Resolve,
  grade the **source clips** or use **Group** grading by camera so the correction carries
  into the multicam clip).
- Premiere: Lumetri on the source clips (or an adjustment on the multicam source
  sequence angles) so all cuts inherit it.
- Don't grade the cut segments individually before lock - corrections must live at
  source level.

## 2. Audio source
- Decide the **master audio**: usually the multitrack recorder (lavs + boom) synced into
  the multicam as its own angle.
- In multicam settings, choose **audio follows video** (switches audio with angle - rarely
  wanted for drama) or a **fixed audio angle** (most common: the recorder/mix angle).
  Premiere: Multi-Camera source sequence audio settings; Avid: group clip audio from a
  specific source; Resolve: multicam clip audio from a chosen angle.
- Keep camera scratch audio for sync checks only, muted in the cut.

## 3. Sync and drift
- Sync by **timecode** (preferred) or waveform; check the clap on every angle.
- Long continuous recordings (concerts, interviews) can **drift** if cameras weren't
  genlocked or timecode drifted; check sync at the start, middle and end; split the
  multicam clip and re-sync segments where needed.
- Consumer cameras with variable frame rates must be conformed to constant rate first.

## 4. After lock
In the grade, the colourist refines matches per shot; editorial's source-level
normalisation is the starting point (pass LUTs/CDLs, not baked looks).

## Gotchas
- Grading cut segments in multicam; the next re-cut loses the corrections.
- Audio following video; levels jump with every angle change.
- Drift appearing 40 minutes into a concert.
- VFR phone footage breaking sync.

## Verify
- [ ] Per-camera transforms and chart-based matches at source level.
- [ ] Master audio angle fixed; scratch muted.
- [ ] Sync checked at start/middle/end; drift corrected.
- [ ] LUTs/CDLs handed to the grade, not baked.
