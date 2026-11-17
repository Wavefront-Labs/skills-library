---
id: creative-arts.film-live-action.color-grading.dailies-colour-and-the-asc-cdl
name: dailies-colour-and-the-asc-cdl
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, colorist, dailies-colourist, dit, cdl, asc-cdl, dailies-grade, dailies-colour, dailies-color, dailies, rushes, slope-offset-power, sop, saturation, ccc, cdl-file, edl-cdl, ale-cdl, look-management, on-set-grade, show-lut, dailies-lut, lut-plus-cdl, livegrade, pomfort-livegrade, silverstack-lab, colorfront, resolve-dailies, dailies-transcode, burn-ins, watermark, dailies-delivery, editorial-dailies, review-dailies, metadata-handoff, colour-notes, color-notes, cdl-to-grade, prelight, look-continuity, cdl-math, slope-offset-power-use, cdl-values, cdl-formats, ccc-files, cdl-in-ale, dailies-pipeline, dailies-deliverables, dailies-design, dailies-software, colorfront-use, resolve-dailies-use, cdl-to-final, cdl-import, cdl-in-grade, live-grading, on-set-cdl, livegrade-use]
level: practitioner
status: draft
description: "Dailies that carry the DP's intent: the ASC CDL (slope/offset/power/saturation) under a show LUT, set live with Livegrade, transcoded with burn-ins, and handed to the final grade as CDL/ALE/EDL."
sources:
  - "https://theasc.com/asc (ASC Color Decision List overview)"
  - "https://pomfort.com/livegrade/ (Pomfort Livegrade documentation)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Resolve - dailies workflows and CDL import)"
  - "https://colorfront.com/ (Colorfront On-Set Dailies)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dailies colour and the ASC CDL

**Goal:** the editor, director and studio watch dailies that look like the film the DP
is making, and the final colourist starts from those decisions instead of guessing -
using a tiny, universal piece of metadata.

## 1. The ASC CDL
Four operations per channel, in order:
`out = (in * slope + offset) ^ power`, then global **saturation**.
- **Slope** (gain, default 1.0), **Offset** (lift, default 0.0), **Power** (gamma,
  default 1.0) - each as R,G,B triplets; **Saturation** default 1.0.
- Designed to be applied **on log footage before the show LUT** (`log -> CDL -> LUT ->
  display`). Applied after a LUT or on Rec.709 it behaves differently; agree the order
  show-wide.
- File forms: `.cdl` (one correction), `.ccc` (colour correction collection, many with
  IDs), embedded in **ALE** columns (`ASC_SOP`, `ASC_SAT`) or **EDL** comments
  (`* ASC_SOP (1.02 0.98 1.00)(-0.01 0.00 0.01)(1.00 1.00 0.98)` / `* ASC_SAT 0.95`),
  or in a **CMX EDL** per event. Every grading tool and dailies system reads them.
Because it's four numbers x three channels, a CDL is an *intent*, not a grade: it
carries exposure, balance and contrast decisions, not secondaries or windows.

## 2. On set: live grading
The DIT runs **Pomfort Livegrade** (or Colorfront Express, Resolve on set) between
camera SDI and the monitors via a LUT box (Teradek Colr, BoxIO, AJA LUT-box):
- Load the **show LUT** (from the prelight/test day) as the fixed look.
- Per setup, adjust **CDL** (and sometimes a per-scene saturation) to the DP's taste on
  a calibrated monitor; the DP approves; the grade is stored per clip with the
  camera's clip name/timecode (Livegrade links to the camera's metadata/ALE).
- Export at wrap: a **`.ccc`/`.cdl` set + ALE/CSV** with clip names, LUT name,
  grade per clip, and reference stills (frame grabs with the grade). This is the
  **look package** that travels with the camera cards to dailies.
Keep CDL adjustments moderate: large offsets or slopes mean the exposure/WB should have
changed on camera.

## 3. Making the dailies
Dailies colourist/lab (Resolve, Colorfront, Silverstack Lab):
1. Ingest camera originals + the look package; match clips to CDLs by clip name/TC
   (Resolve: Media Pool > import ALE/CDL via *Timeline > Import > ... CDL* or use
   `ColorTrace from CDL`; apply the show LUT as a timeline/output LUT or in the node).
2. Sync sound, add **burn-ins** (timecode, clip name, scene/take, date, watermark with
   the viewer's name for secure review), transcode to the editorial codec (DNxHD/ProRes
   Proxy) and a review H.264 (Frame.io/Moxion/PIX).
3. Check scene continuity: shots within a scene should look consistent; trim the CDL
   where the on-set live grade drifted, but don't re-interpret the DP's look. Flag
   problem footage (focus, exposure, flicker) in a **dailies report** to the DP/DIT by
   morning.
4. Deliver: editorial dailies + ALE with the CDL columns so the edit carries the values;
   the review link to the director/producers; archive of the look package.

## 4. Handing off to the final grade
At conform, the colourist imports the **CDLs** (Resolve: *ColorTrace* with the ALE/
EDL CDL values, or *Timeline > Import > ... CDL*; Baselight: CDL import from ALE/EDL)
onto the matching clips, applies the same show LUT, and starts the grade from what
the DP approved - re-balancing from there rather than from zero. Dailies stills in the
Gallery are the reference for "what we loved in rushes".

## 5. Consistency rules
- One show LUT (or one per camera type, mapped to the same look) for the entire
  production; version it (`SHOW_LUT_v3.cube`) and never change it mid-shoot without
  reissuing dailies for continuity.
- Monitors on set and in the dailies suite calibrated to the same target.
- CDL order (log -> CDL -> LUT) stated in the pipeline doc and set identically in
  Livegrade, the dailies system and the finishing suite.

## Gotchas
- CDL applied after the LUT in finishing when it was before on set; dailies don't match the grade start.
- Clip names changed by the offload (renaming cards) so CDLs don't link.
- DP's "live" grade pushed hard to compensate for a bad monitor; dailies look wrong in the suite.
- No stills saved; the look lives only in the DIT's memory.
- Dailies transcoded without the LUT for speed; editorial cuts to flat log for six weeks.

## Verify
- [ ] Show LUT versioned; CDL order documented and identical across set, dailies and grade.
- [ ] Per-clip CDLs exported with ALE/EDL and stills at wrap each day.
- [ ] Dailies matched within scenes, burned-in, delivered with CDL metadata to editorial.
- [ ] Final grade starts from imported CDLs and dailies stills.
