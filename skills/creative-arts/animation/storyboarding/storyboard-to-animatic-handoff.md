---
id: creative-arts.animation.storyboarding.storyboard-to-animatic-handoff
name: storyboard-to-animatic-handoff
category: creative-arts
field: animation
product: storyboarding
tags: [animation, storyboarding, animatic, editorial-handoff, export, naming-convention, timecode, audio-sync, boardomatic, premiere, avid, shot-numbering, pipeline]
level: practitioner
status: draft
description: "Package a locked board into an animatic editorial can use: export settings, naming, sync, and the handoff checklist."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SKILL: Storyboard-to-animatic handoff

This is the **technical handoff** from a drawn/boarded sequence to the cut editorial
actually works with: file formats, naming, timing data, and the checklist that keeps
the board artist's intent from getting lost or renumbered on the way into an edit
timeline. `creative-arts.animation.storyboarding.storyboarding` names the boardomatic
concept (panels cut to scratch VO); this skill is the concrete export/package step that
makes that boardomatic a real file editorial can cut, retime, and hand back notes
against — and it is the direct input to `story-reel-editorial`. Distinct from the
notes-handling skill (`storyboard-revisions-and-director-notes`), which covers what
happens *after* editorial or the director reacts to this handoff.

## What "handoff" actually means
The board artist's deliverable to editorial is not a folder of panel images — it's a
**timed sequence** (an editable video/XML/EDL, or at minimum numbered stills with an
explicit duration list) plus the source panels, so editorial can retime without asking
the artist to re-export every change. Handing over only a rendered video with no
underlying panel/timing data forces editorial to guess durations by eye when they need
to adjust, which is slower and loses precision.

## Minimum package
Every handoff should include:
1. **Numbered panel images**, one file per panel, named by shot/panel number matching
   the board's own numbering (see Naming below) — not by export order.
2. **A duration list** (per-panel hold time, in frames or timecode at the project's
   frame rate) — this is what actually builds the cut; get the frame rate right before
   building it (23.976/24/25/29.97, matching the show's delivery rate — mixing rates is
   the single most common sync bug at handoff).
3. **The scratch audio/VO track** the panels were timed against, as a separate audio
   file, so editorial can re-sync if they retime panels.
4. **A rendered reference video** (the boardomatic) — convenient for quick review, but
   it is not the editable deliverable; treat it as a preview, not the handoff itself.

## Naming and numbering
- **Match panel numbers to the shot-list numbering editorial/production already
  uses** (e.g. `sq010_sh020_v03.png`), not an internal-only board numbering scheme. If
  the board's numbering and the shot list's numbering diverge, editorial will cut
  against the wrong panel or lose track of which panel is current — this is the most
  common handoff error after frame-rate mismatches.
- **Version the export, not just the source file.** The exported package should carry
  the same `seq_vNN` the source sequence is on (see the parent skill's revision
  workflow), so a question like "is this the v3 export?" is answerable from the
  filename alone.
- **Don't reuse a panel number for a different panel across versions.** If panel 020
  is cut from the sequence, retire the number rather than renumbering everything after
  it — a shifted numbering scheme breaks every outstanding note that referenced a
  panel by number.

## Export mechanics (method-dependent)
- **From a video-editing/NLE-built boardomatic** (panels cut as a timeline): export an
  EDL or XML alongside the rendered video if editorial's tool can read it, so the cut
  points and per-panel durations transfer as data, not just pixels.
- **From a 3D/Grease Pencil tool rendering viewport grabs**: export stills at the
  project's actual delivery resolution (or a documented proxy resolution — note it in
  the handoff so editorial doesn't mistake proxy res for final), plus a separate text
  or spreadsheet duration list keyed to panel number.
- **From a dedicated storyboard/boardomatic app**: use its native timing export if one
  exists rather than hand-building a duration list — hand-built lists are where typos
  creep in. **Unconfirmed**: specific export menus/formats differ by tool version; this
  skill states the data that must survive the export, not a single app's exact menu
  path.

## Sync and the handback
- **Scratch VO frame-aligns to the panels it was timed against — ship them as a pair.**
  If editorial receives panels and audio separately with no shared start timecode, they
  will re-sync by ear, which drifts over a long sequence.
- **Expect editorial notes to come back as timecodes, not panel numbers**, once the
  sequence is in their timeline — keep the panel-number-to-timecode mapping (even a
  simple log) so a note like "tighten the cut at 00:01:12:04" maps back to the right
  panel without guessing.
- **A re-timed cut from editorial is not automatically the new board truth.** If
  editorial trims a hold for pace, that's a note back to the board (does the shortened
  hold still read?), not a silent overwrite of the board's intended timing — route it
  through the revisions workflow (`storyboard-revisions-and-director-notes`) rather
  than treating editorial's cut as final without a look-back.

## Gotchas
- **Frame rate mismatch between the board tool's project and the edit timeline.** Catch
  this before export — a board built at 24fps dropped into a 29.97 timeline will drift
  over a multi-minute sequence even though each individual panel "looks right."
- **Color space / gamma differences** between a 3D-viewport grab and the show's
  delivery color space can make boardomatic stills look wrong in the edit timeline;
  this is a preview-quality issue, not a timing one — don't let it block the handoff,
  but flag it so editorial doesn't mistake it for a lighting note.
- **Shipping only the rendered video and deleting the source panels/project file**
  once "done." Editorial or the director will ask for a retime days later; losing the
  editable source turns a two-minute fix into a redo.

## Verify
- [ ] The package includes numbered stills, a duration list, the scratch audio, and a
      rendered preview — not just the preview video.
- [ ] Panel numbers in the export match the production shot-list numbering, not an
      internal-only scheme.
- [ ] Frame rate in the export matches the edit timeline's project settings.
- [ ] The export is versioned (`seq_vNN`) matching the source sequence's version.
- [ ] A panel-number-to-timecode mapping exists so editorial's timecode notes can be
      traced back to a specific panel.
- [ ] The source project/panel files are retained after handoff, not deleted once the
      render ships.
