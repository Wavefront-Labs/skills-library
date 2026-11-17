---
id: creative-arts.music.music-production.session-interchange-aaf-midi-and-stems
name: session-interchange-aaf-midi-and-stems
category: creative-arts
field: music
product: music-production
tags: [music-production, logic-pro, pro-tools, daw, aaf, session-interchange, omf, standard-midi-file, tempo-map-export, consolidated-stems, cross-daw-collaboration, dawproject, bwf-timestamp]
level: practitioner
status: draft
description: "Move a project between DAWs: consolidated stems from a common start, AAF/OMF, MIDI files with tempo maps, DAWproject, and an import alignment checklist."
sources: ["https://www.avid.com/pro-tools (Pro Tools Reference Guide - Import/Export AAF, Session Data)", "https://support.apple.com/guide/logicpro/ (Export AAF, MIDI files)", "https://www.bitwig.com/dawproject/ (DAWproject open format)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Session interchange: AAF, MIDI and stems

**Goal:** a collaborator opens your project in another DAW with everything in time.

## 1. Universal method: consolidated audio
- Export every track as a full-length WAV from the **same start point** (bar 1 or a fixed timecode), 24-bit, session sample rate (see bouncing skill).
- BWF timestamps help (files placed at their original time with "spot to original timestamp" in Pro Tools).
- Include the tempo and time signature (and tempo map changes) in a notes file.

## 2. MIDI
- Export **Standard MIDI Files (type 1)** per track or the whole project: includes notes, CC, and the **tempo map** (Logic: File > Export > Selection as MIDI File; Pro Tools: File > Export > MIDI).
- Virtual instrument sounds don't transfer; also print audio of each instrument part.

## 3. AAF/OMF (edit-level interchange)
- **AAF** preserves clip positions, edits, fades (often) and track layout, with embedded or referenced audio. Common for Pro Tools <-> Logic/Nuendo and for post-production (picture editors send AAF to sound).
- Logic: File > Export > Project as AAF; Pro Tools: File > Export > Selected Tracks as AAF/OMF. Choose embedded audio for simplicity or "copy media" folder.
- Plugins, automation (partially), and instrument tracks generally do not transfer.

## 4. DAWproject
- Open XML-based format (Bitwig, Studio One, Cubase 14+ and others) that preserves tracks, clips, some automation and plugin states between supporting DAWs. Check support in both DAWs.

## 5. Checklist
- Same sample rate on both ends; agreed start point; tempo map delivered; files named with numbers for order (`01_Kick.wav`); rough mix included for reference.

## Gotchas
- Exporting from the first clip instead of bar 1: tracks start at different points.
- Tempo-mapped projects without the map: imported MIDI won't line up with audio.
- AAF fades rendered differently in the target DAW: listen through edits.

## Verify
- Re-import your own export into a fresh session (or the target DAW): all tracks align with the rough mix.
