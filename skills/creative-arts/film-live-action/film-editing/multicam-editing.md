---
id: creative-arts.film-live-action.film-editing.multicam-editing
name: multicam-editing
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, editor, assistant-editor, multicam, multicam-editing, multi-camera-editing, multicam-sync, multi-camera, group-clips, multigroup, multicam-clip, multi-camera-source-sequence, angle-switching, line-cut, iso-cameras, a-cam-b-cam, timecode-sync, waveform-sync, sync-by-audio, sync-map, camera-angles, flatten-multicam, cutting-live, coverage, two-camera-dialogue, interviews, concerts, sitcom, avid-media-composer, premiere-pro, davinci-resolve, final-cut-pro, multicam-sync-methods, multicam-audio-sync, live-switching, angle-cutting, angle-swap, multicam-refinement, concert-multicam]
level: practitioner
status: draft
description: "Edit multi-camera material: build synced multicam clips by timecode or audio, order angles, cut live by switching then refine, handle A/B dialogue coverage and interviews, flatten for turnover."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Resolve - multicam editing chapter)"
  - "https://helpx.adobe.com/premiere-pro/using/multi-camera-editing-workflow.html (Premiere Pro multi-camera workflow)"
  - "https://avid.secure.force.com/pkb/ (Avid Media Composer - group and multigroup clips)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicam editing

**Goal:** cut a scene shot on two to twelve cameras as if choosing angles live, then
refine with the normal tools - without ever losing sync or the ability to swap an angle.

## 1. Prepare the material
- Each camera's clips named with scene/take/camera (`12A_3_A`, `12A_3_B`); sound as
  separate poly WAV. Jam-synced timecode on all cameras and the recorder is the
  difference between minutes and days.
- Decide the **angle order** (A, B, C... or by position: wide, left, right, tight) and
  keep it the same for every take of the show - muscle memory matters.

## 2. Build the multicam clip
- **Resolve**: select all clips for a take (all cameras + sound) in the Media Pool >
  right-click > *Create Multicam Clip* > sync by *Timecode* (jammed), *Sound* (waveform),
  *In/Out* or *Markers*; angle order by name/camera. Multicam clips show in the viewer's
  *Multicam* mode in the Edit page.
- **Premiere**: select clips > *Create Multi-Camera Source Sequence* > sync by Timecode
  or Audio (waveform); set the sequence preset; "Offset audio" if the recorder starts
  late. Open in the Source Monitor in Multi-Camera view.
- **Avid**: *Group clips* (one take, synced by TC/mark) and *Multigroup* (whole scene,
  many takes). Set the **Multicam view** (4-way, 9-way) in the Composer.
- **FCP**: *New Multicam Clip*, sync by audio/timecode, assign angles.
Verify sync on each take against the slate clap; audio-waveform sync can lock to the
wrong peak on noisy sets - check a line of dialogue 3 minutes in.

## 3. Cutting
1. Lay the multicam clip on the timeline (the *line cut* track). Set the **audio** to the
   sound recorder's mix/ISO rather than any camera's audio; enable "switch video only".
2. Play and **switch live**: number keys (1-9) in Premiere/Resolve/Avid change angle at
   the playhead; each press makes a cut. First pass fast, following performance.
3. Refine: cuts are normal edit points - trim with ripple/roll; **swap** an angle on an
   existing segment (Resolve: right-click > switch angle; Premiere: click the angle in the
   monitor; Avid: Swap Cam Bank/quad split) without touching timing.
4. Combine with single-cam coverage (inserts, pick-ups) on tracks above.
5. Keep the line cut and a copy of the untouched multicam clip for alternate takes.

## 4. Craft notes by genre
- **Two-camera dialogue (A/B)**: both cameras on different sizes of the same side, or
  opposite singles - cut like a normal dialogue scene (reactions, eyelines); multicam just
  guarantees sync between A and B so overlaps are free. Beware mismatched lens heights.
- **Interviews**: wide + tight on one subject - switch to hide edits (jump-cut avoidance),
  or use a single angle and cut-aways for honesty. Keep angle changes on sentence boundaries.
- **Concerts/live events**: tempo-driven switching; cut on phrases and performer moves;
  go wide on transitions. Build a sync map (one multicam per song/segment).
- **Sitcom/studio**: 4-camera line cut usually exists from the gallery; import the
  director's line cut as an EDL and refine against ISOs.

## 5. Finishing
- **Flatten** when picture is locked (Resolve: right-click > *Flatten Multicam Clip*;
  Premiere: *Multi-Camera > Flatten*; Avid: *Commit Multicam Edits*) so EDL/AAF/XML
  export references real source clips - unflattened multicam does not conform.
- Check that each flattened segment points at the right camera reel and timecode
  before turnover; colour needs per-camera matching (A and B cameras rarely match).

## Gotchas
- Syncing by audio with each camera's scratch mic in a loud room - false locks.
- Editing with camera audio then discovering the recorder's mix is 2 frames off.
- Changing the angle order between takes.
- Not flattening before AAF/EDL - the conform returns blanks.
- Mixed frame rates between cameras; the multicam clip drifts over a long take.

## Verify
- [ ] All cameras and sound in each multicam clip; sync verified on the slate and deep in the take.
- [ ] Audio source is the recorder; switching set to video only.
- [ ] Line cut saved separately from refined cut; angles swappable without re-timing.
- [ ] Multicam flattened and EDL/AAF verified before turnover.
