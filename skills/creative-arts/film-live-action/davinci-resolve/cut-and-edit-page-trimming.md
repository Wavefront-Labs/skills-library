---
id: creative-arts.film-live-action.davinci-resolve.cut-and-edit-page-trimming
name: cut-and-edit-page-trimming
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, edit-page, cut-page, trim-mode, trim-edit-mode, dynamic-trim, dynamic-trimming, ripple-trim, roll-trim, slip, slide, slip-slide, ripple-delete, three-point-edit, insert, overwrite, replace, fit-to-fill, place-on-top, append-at-end, source-tape, sync-bin, smart-insert, close-up-button, boring-detector, source-overwrite, keyboard-shortcuts, jkl, snapping, linked-selection, auto-select, track-destination, timeline-view-options, stacked-timelines, compound-clip, take-selector, speed-editor, markers, flags, audio-trim-view, source-tape-mode, sync-bin-use, smart-insert-use, edit-types, fit-to-fill-edit, place-on-top-edit, trim-editor, numeric-trim, compound-clip-use, nested-timeline, take-selector-use, resolve-speed-effects, optical-flow-retime, resolve-markers, flags-use, timeline-navigation]
level: practitioner
status: draft
description: "Edit fast in Resolve: Cut page source tape, sync bin and smart insert, Edit page three-point edits, trim mode with dynamic JKL trimming, slip/slide, and shortcuts that keep you on the keyboard."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Definitive Guide to DaVinci Resolve - Cut page and Edit page chapters)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cut and Edit page editing and trimming in Resolve

**Goal:** assemble on the Cut page in minutes, refine on the Edit page with trims that
do exactly what you intend, and never reach for the mouse for a routine operation.

## 1. Cut page: assembly speed
- **Source Tape** (icon top-left of Media Pool): plays every clip in the bin as one tape;
  scrub, set in/out, and insert without opening clips.
- **Sync Bin**: for multicam material with timecode, shows every camera angle live at
  the playhead; click an angle to cut it in.
- Edit buttons: **Smart Insert** (inserts at the nearest cut to the playhead), **Append**,
  **Ripple Overwrite**, **Close Up** (auto-creates a punched-in CU from a wide, scaling
  the image - fine for interviews, not for drama), **Place on Top**, **Source Overwrite**
  (multi-cam by TC).
- The upper timeline shows the whole program, the lower shows the playhead zone - use
  both for a rough assembly, then switch pages. **Boring Detector** flags shots too long/
  short. Cut page is ideal with the DaVinci **Speed Editor** hardware.

## 2. Edit page: three-point editing
Set In/Out on the source (`I`/`O`) and one point on the timeline (or vice versa):
- **Insert** (`F9`) ripples everything right; **Overwrite** (`F10`); **Replace** (`F11`)
  aligns the source playhead to the timeline playhead; **Fit to Fill** retimes to the gap;
  **Place on Top** (`F12`); **Append at End** (`Shift+F12`); **Ripple Overwrite**
  (`Shift+F10`).
- Destination controls: the orange **auto-select** and the track destination (`A1`/`V1`
  patches on the left of the timeline header) determine where edits land and whether
  audio comes with video - the number-one source of "my audio didn't come in".
- **Linked selection** (chain icon) and `Alt`-click to break a link temporarily;
  `Ctrl/Cmd+Shift+L` to unlink clips.
- **Markers** (`M`, double-click to annotate; colours for departments), **Flags** on
  clips (`G`), clip colours for scenes.

## 3. Trim edit mode
Press `T` for **Trim Edit mode**: the pointer changes by position on the cut.
| Position | Action | Result |
|---|---|---|
| On the cut, outer edge | **Ripple** | Change clip length, timeline shifts |
| On the cut, inner edge (two bars) | **Roll** | Move the cut point, total length unchanged |
| Middle of clip, top half | **Slip** | Change which part of the source is shown, position fixed |
| Middle of clip, bottom half | **Slide** | Move the clip, neighbours adjust |
Numeric trims: select an edit point (`U` cycles ripple-in/roll/ripple-out) and type
`+5`/`-12` frames, or `,` / `.` for ±1 frame, `Shift+,` / `Shift+.` for ±5.
**Dynamic trim**: select the edit, press `W` (dynamic trim mode), then `J/K/L` to trim
while watching at speed - the cut moves to where you press `K`. Loop playback around
the cut (`/`) to judge.
**Audio trim view** (`Ctrl/Cmd+Shift+A`) expands waveforms to trim J/L cuts on sound.
Trim multiple edit points at once (Ctrl/Cmd-click several) to adjust a whole sequence.

## 4. Timeline hygiene
- Timeline View Options: stacked timelines (multiple tabs) for comparing versions,
  subtitle track visibility, audio waveform size.
- `Shift+Z` fit to window; `Alt+scroll` zoom; **snapping** (`N`) on for assembly,
  off for fine trims; `Ctrl/Cmd+D` duration dialog.
- `Shift+V` select clip under playhead; `Ctrl/Cmd+B` razor; `Backspace` ripple delete;
  `Ctrl/Cmd+Shift+]` / `[` select clips forward/back on a track.
- Compound clips (`Alt+G`) for groups; *Decompose in Place* to unpack.
- **Take Selector** (right-click > Take Selector) to stack alternate takes on one slot.
- Save your keyboard map (`DaVinci Resolve > Keyboard Customization`) and export it; a
  Premiere/Avid/FCP preset is available for migrants.

## 5. Speed and retiming
Right-click > **Change Clip Speed** or `Ctrl/Cmd+R` retime controls; *Retime Process*
in Inspector (Nearest / Frame Blend / Optical Flow), *Speed Warp* for the best
optical flow (slow, cache it). Reverse, freeze frames from the retime menu.

## Gotchas
- Track destination patched to the wrong track; insert lands on V2 silently.
- Ripple trims with auto-select off on an audio track: sync drift between picture and sound.
- Trimming in Selection mode (`A`) instead of Trim mode: edits move instead of trimming.
- Close-Up on the Cut page used on drama footage: a scaled, soft shot in the master.
- Snapping on during a 1-frame trim, snapping to the wrong thing.

## Verify
- [ ] Auto-select and destination patches set before each insert; audio comes with video.
- [ ] Trim mode used for all cut adjustments; dynamic JKL trim used to judge at speed.
- [ ] Versions on stacked timelines; markers/flags carry notes.
- [ ] Keyboard map saved and exported.
