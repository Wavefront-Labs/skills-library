---
id: creative-arts.film-live-action.davinci-resolve.vfx-pulls-and-timeline-export
name: vfx-pulls-and-timeline-export
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, individual-clips-render, vfx-handoff-render, exr-render, timeline-export, aaf-export-resolve, xml-export-resolve, edl-export, vfx-pulls, handles, otio]
level: practitioner
status: draft
description: "Hand work out of Resolve: render individual clips (EXR/DPX/ProRes) with handles for VFX, and export timelines as AAF, XML, EDL or OTIO for sound, other NLEs and the online."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Deliver page individual clips; Export Timeline AAF/XML/EDL)"
  - "https://www.vesglobal.org (VES Handbook - plate delivery to VFX vendors)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VFX pulls and timeline export

**Goal:** VFX vendors get exactly the frames they need in the right format, and other
departments get timelines that relink and conform without surprises.

## 1. Individual clips render (VFX pulls)
Deliver page > **Render: Individual clips**:
- Select the VFX timeline/track (or tag VFX clips with a colour/flag and filter).
- **Format**: OpenEXR (16-bit half float, PIZ/ DWAA compression) or DPX 10-bit log for
  vendors; ProRes 4444 for simpler work.
- **Colour**: usually **ungraded** camera-native log/ ACES (AP0 for ACES EXR) - set the
  render's output colour space/ disable grades (*Bypass re-sizing/ Disable grading*
  options vary - or render from a timeline with grades off). Supply the show LUT/ CDL for
  viewing separately.
- **Handles**: Add X frame handles (8-12 typical) in *File > Render at source resolution
  / Add handles* options.
- **Naming**: Use **Custom name** tokens (e.g. `%{VFX ID}` via clip metadata or the
  timeline clip name) so files are named by shot ID: `CHS_0040_plate_v001.####.exr`.
- Render at source resolution (no reframes baked) unless the vendor asked for a crop.
Include an EDL/list of shot IDs, frame ranges and handles.

## 2. Timeline export
*File > Export > Timeline* (or right-click the timeline in the Media Pool):
- **AAF**: for Avid and Pro Tools (audio turnover) - export with audio embedded or
  linked; audio handles; sound often prefers AAF from the editor's NLE.
- **FCP 7 XML / FCPXML**: Premiere (FCP 7 XML) and Final Cut Pro (FCPXML).
- **EDL** (CMX 3600): one video track per EDL; simple, robust for conforms and VFX lists.
- **OTIO** (OpenTimelineIO, recent versions): interchange with pipelines/tools.
- Check: reel/tape names in source metadata (EDLs need them), speed effects, transforms,
  and multicam (flatten before export).

## 3. Test the round trip
Import the exported file into a scratch project (or ask the receiver to) and compare with
a reference movie (burn-in TC) before declaring the turnover done.

## Gotchas
- Graded or LUT-baked plates sent to VFX.
- Handles missing - vendors can't extend shots.
- Generic filenames (clip names) - vendors can't match shots to IDs.
- XML/AAF dropping speed ramps and transforms; no reference movie to catch it.

## Verify
- [ ] Plates in agreed format/colour, at source resolution, with handles.
- [ ] Files named by VFX ID; shot list sent.
- [ ] Timeline exported in the receiver's format with correct metadata.
- [ ] Round trip tested against a reference movie.
