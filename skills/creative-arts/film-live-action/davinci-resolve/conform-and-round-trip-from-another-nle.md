---
id: creative-arts.film-live-action.davinci-resolve.conform-and-round-trip-from-another-nle
name: conform-and-round-trip-from-another-nle
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, colorist, assistant-editor, conform, round-trip, roundtrip, xml-import, fcpxml, aaf-import, edl-import, cmx3600, relink-media, relink, reconform, import-timeline, offline-reference, offline-reference-comparison, timeline-comparison, source-timecode, reel-names, reel-name-extraction, mixed-frame-rates, speed-changes, retime-import, nested-sequences, flatten, premiere-to-resolve, avid-to-resolve, fcp-to-resolve, resolve-to-premiere, export-xml, export-aaf, render-individual-clips, round-trip-render, handles, color-trace, colortrace, remote-grades, scene-cut-detection, conform-lock, import-options, timeline-import-settings, import-aaf-options, relink-strategies, reel-name-matching, offline-comparison, fixing-mismatches, conform-checking, reconform-changes, timeline-comparison-tool, compare-timelines, avid-conform, premiere-conform, fcp-conform, speed-conform, effects-conform, retime-conform]
level: practitioner
status: draft
description: "Conform an offline cut in Resolve: import AAF/XML/EDL, relink to camera originals by reel name and timecode, fix retimes and nests, verify against the offline reference, render back with handles."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - Conforming chapters)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Conforming and Relinking; Round-trip workflows)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conform and round-trip from another NLE

**Goal:** the colourist grades the editor's exact cut, from full-resolution originals,
and hands back a timeline the editor can drop into their project with nothing shifted.

## 1. Get a clean export from the NLE
Ask the editor for (per reel/episode):
- **Premiere**: `File > Export > Final Cut Pro XML` (FCP7 XML) - flatten nested
  sequences, remove or note unsupported effects, transitions as plain cross-dissolves,
  no multicam (flatten), no audio needed unless the sound is finishing in Resolve.
- **Avid**: **AAF** with *Link to (don't embed)* for picture; consolidate first; reel
  names in *Tape* column; *Video Mixdown* removed; motion effects noted.
- **FCP X**: FCPXML 1.8+; roles flatten to tracks.
- **EDL** (CMX3600): one per video track; the most robust for a simple cut; needs
  reel names ≤ 8 chars or `FROM CLIP NAME` comments.
- Plus a **reference movie** (offline render with burn-in TC) and a drive/path list of
  camera originals.

## 2. Import the timeline
Media page: add original media locations in Media Storage, then
`File > Import > Timeline` (or drag the XML/AAF into the Media Pool). In the dialog:
- **Automatically import source clips into media pool** - on if the originals are
  reachable; tick *Ignore file extensions when matching* and *Use sizing information*
  (carries scale/position), *Use timeline frame rate*, *Mixed frame rates: Resolve/Cinema Tools*
  per the NLE's conventions.
- Resolve matches by **file name + timecode**, or by **reel name** when enabled in
  `Project Settings > General Options > Assist using reel names from the: Source clip
  file pathname / Embedding in source clip file / Pattern` - set the pattern that
  extracts `A001_C004` style reel names when the NLE used reel names rather than paths.
- After import, offline (unlinked) clips are red. `Media Pool > right-click > Relink
  Selected Clips` to the originals' folder; or *Conform Lock* a clip and *Replace
  Selected Clip* manually.

## 3. Fix the usual breakages
- **Speed changes / retimes**: XML carries constant speed; variable ramps often need
  manual recreation from the reference (Retime Curve). Avid motion effects need checking.
- **Nests/compound clips**: decompose or recreate; multicam must be flattened in the NLE.
- **Scale/position/crop**: compare with the reference; *Use sizing information* handles
  most; Resolve's crop differs from Premiere's - re-set.
- **Mixed frame rates**: 23.976 timeline with 59.94 clips - Clip Attributes frame rate
  then retime; check with the reference.
- **Stills/graphics/titles**: NLE titles don't translate; use the offline render on a
  track above or rebuild.
- **Audio** usually stays with the NLE; if finishing sound in Fairlight, import the AAF
  of the audio separately.
- `Timeline > Reconform from Bins` after new media arrives.

## 4. Verify against the offline
Import the reference movie, add it as *Offline Reference* (right-click clip in Media
Pool > *Add as Offline Reference Clip*; then timeline right-click > *Link Offline
Reference Clip*). In the Edit/Color page viewer, enable **Offline** view
(`View > Reference Wipe Mode` / the Offline toggle on the Color page) with a wipe or
difference to check every cut for the right clip, frame and framing. Mark problem cuts
with markers; walk the whole timeline once before grading. `Timeline > Compare Timeline`
also diffs two timelines (after a re-cut).

## 5. Round trip back
After the grade, Deliver page > **Render Settings**:
- Presets: *Premiere XML Round-Trip*, *Avid AAF Round-Trip*, *Final Cut Pro X Round-Trip*
  set **Render: Individual clips**, source-name file naming, and **Add X frame handles**
  (8-24). Codec: ProRes 4444/422 HQ or DNxHR 444; *Render at source resolution* if the
  editor finishes at timeline res anyway.
- Render, then `File > Export > Timeline > XML/AAF` (the round-trip presets do this
  automatically). The editor imports the XML/AAF; it links to the new graded files
  with handles, keeping cut points. Keep source timecode (`Use timecode: Source`).
- Alternative: deliver a single flattened master plus an EDL if the editor only needs
  to lay the final back.

## 6. Re-cuts after grading
When the editor changes the cut: export a new XML/EDL; import as a new timeline with
grades carried via **ColorTrace** (`Timelines > right-click new timeline > ColorTrace`
from the graded timeline; automatic for matching source TC, manual for changed clips)
or copy grades via *Remote versions* if the same source clips.

## Gotchas
- Reel-name assist off: every clip from a camera with the same clip names (`C0001`) relinks wrong.
- XML with handles baked by the editor's export: in/out points off by the handle length.
- Not checking the first and last frame of every clip against the reference; a flop or a reframe missed.
- Round-trip render without handles; the editor can't trim a frame.
- Rendering individual clips with timeline timecode; the NLE can't relink.

## Verify
- [ ] Timeline imported with all clips linked (no red) and reel-name assist configured.
- [ ] Offline reference wipe checked at every cut; retimes/sizing corrected.
- [ ] Round-trip preset used: individual clips, source names, handles, XML/AAF exported.
- [ ] Re-cut handled with ColorTrace, not a regrade.
