---
id: creative-arts.film-live-action.premiere-pro.timeline-tools-and-trimming
name: timeline-tools-and-trimming
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, trimming, timeline-tools, timeline-editing, three-point-editing, insert, overwrite, ripple-edit, rolling-edit, slip-tool, slide-tool, rate-stretch, razor, track-select-forward, source-patching, track-targeting, sync-lock, track-lock, linked-selection, trim-mode, trim-monitor, dynamic-trimming, jkl, keyboard-shortcuts, extract, lift, ripple-delete, nested-sequences, markers, snapping, timeline-display-settings, replace-with-clip, match-frame, reveal-in-project, trim-mode-detail, keyboard-trimming, trim-shortcuts, track-targeting-use, source-patching-use, sync-lock-use, keyboard-customisation, shortcut-presets, replace-with-clip-use, match-frame-use, timeline-display, track-heights]
level: practitioner
status: draft
description: "Edit on the Premiere Pro timeline: source patching and track targeting, three-point insert/overwrite, ripple/roll/slip/slide and Trim mode with JKL, sync lock, lift/extract/match frame shortcuts."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/trimming-clips.html (Adobe - Trimming clips in Premiere Pro)"
  - "https://helpx.adobe.com/premiere-pro/using/editing-sequences.html (Adobe - Editing sequences)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional in Video Design using Premiere Pro - exam objectives, Domain 3)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeline tools and trimming in Premiere Pro

**Goal:** edits land on the right track with the right audio, every trim does what you
meant, and your hands never leave the keyboard for a routine cut.

## 1. Source patching and targeting (why "my audio went to A3")
Left of the timeline header: **source patching** buttons (`V1`, `A1`... in blue on the
left, matching the source clip's tracks) decide *where* an insert/overwrite lands;
**track targeting** (the highlighted `V1/A1` boxes) decide what keyboard navigation,
match frame and copy/paste act on. Drag the source patch to a different track to route
audio to A3; click to disable a source track (video-only edit). `Ctrl/Cmd+Shift+...`
is not needed - just patch deliberately before each edit.

## 2. Three-point editing
Mark In/Out on the source (`I`/`O`) or the timeline; the playhead or In point on the
other side completes the edit:
- **Insert** (`,`) pushes everything after the edit point down on the targeted tracks
  (and all tracks with **sync lock** on - the padlock icon; turn it off on a music track
  you don't want shifted).
- **Overwrite** (`.`) replaces.
- Drag with `Ctrl/Cmd` for insert, plain drag for overwrite. `Alt`-drag copies.
- **Replace with Clip** (`Alt`-drag a source over a timeline clip, or right-click >
  Replace With Clip > From Source Monitor, Match Frame) swaps the clip, keeping position.
- **Lift** (`;`) and **Extract** (`'`) remove In-Out from the targeted tracks (extract
  ripples). **Ripple delete** (`Shift+Delete`/`Shift+Backspace`) closes the gap.
- **Match Frame** (`F`) opens the source at the timeline frame; **Reveal in Project**
  (`Shift+F`... actually right-click) finds the clip in a bin.
- **Fit to fill**: `Rate Stretch` (`R`) tool drags a clip to a duration.

## 3. Trimming tools
| Tool | Key | Does |
|---|---|---|
| **Selection** | `V` | Drag an edge: regular trim (leaves a gap/overwrites) |
| **Ripple edit** | `B` | Trim and close the gap; shifts later clips |
| **Rolling edit** | `N` | Move the cut point; total length constant |
| **Slip** | `Y` | Change source content, keep position/duration |
| **Slide** | `U` | Move the clip, trimming neighbours |
| **Razor** | `C` | Cut at a point (`Ctrl/Cmd+K` cuts at playhead on targeted tracks; `Ctrl/Cmd+Shift+K` all tracks) |
| **Track Select Forward** | `A` | Select everything after a point (`Shift+A` backward) |
With Selection tool, `Ctrl/Cmd`-drag an edge = ripple; `Ctrl/Cmd`-drag the cut = roll.
Numeric: select an edit point (click with Selection; `Ctrl/Cmd+T` to select nearest),
then type `+5`/`-5` and Enter; `Alt+Left/Right` nudges a selected clip by a frame;
`Ctrl/Cmd+Alt+Left/Right` trims the selected edit point by a frame.
`Shift+T` cycles the edit-point type (ripple in / roll / ripple out).

## 4. Trim mode and dynamic trimming
Double-click an edit point (or `T`) to enter **Trim mode** - the Program Monitor shows
the outgoing and incoming sides with large buttons (-5/-1/+1/+5). Press **Space** to loop
around the cut while trimming; **J/K/L** with Trim mode on does *dynamic trimming*: play,
press `K` where you want the cut to be. `Ctrl/Cmd+Shift+T` toggles trim type. Set the
preroll/postroll in `Preferences > Playback`.
**Audio trimming**: `Alt`-click a linked clip's audio to trim it alone (J/L cuts);
`Shift+Ctrl/Cmd+L` unlink; keep **Linked Selection** on otherwise.

## 5. Timeline hygiene and speed
- `Shift+S` snapping; `\` zoom to sequence; `+`/`-` zoom; `Ctrl/Cmd+Shift+H` ... prefer
  the wrench (Timeline Display Settings) to show audio waveforms, names, and
  through-edits (`Show Through Edits` so you can select and `Delete` a razor that
  changed nothing).
- **Markers** `M` (sequence) / `Shift+M` to clip; comment markers for notes; **Clip
  color labels** per scene; **Nest** (right-click > Nest) for sequences you move as one.
- Save a custom keyboard layout (`Premiere Pro > Keyboard Shortcuts`) and sync it via
  Creative Cloud; map ripple trim next/previous (`Q`/`W` = ripple trim to playhead) and
  "Extend selected edit to playhead" (`E`) - the three keys that save the most time.
- Track height presets (`Ctrl/Cmd+Alt+-/+`), `Ctrl/Cmd+Shift+A` deselect all.

## Gotchas
- Sync lock on a track you didn't intend to shift (titles, music) - cuts drift out of sync.
- Source patch unset on A1 - clip comes in silent.
- Trimming with Selection tool and leaving gaps, then wondering why the program has black frames (`Sequence > Go to Gap` finds them).
- Through-edits hidden; a razor cut from an old attempt stays in the exported file as an invisible double cut.
- Dynamic trim preroll too short to judge rhythm.

## Verify
- [ ] Source patches and targets set before every insert; audio lands where intended.
- [ ] Trims done with ripple/roll/slip/slide tools or Trim mode, not by dragging and leaving gaps.
- [ ] Sync lock states deliberate per track.
- [ ] Custom keyboard layout saved with ripple-to-playhead and extend-edit keys.
