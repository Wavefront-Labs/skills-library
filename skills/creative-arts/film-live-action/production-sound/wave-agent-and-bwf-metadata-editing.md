---
id: creative-arts.film-live-action.production-sound.wave-agent-and-bwf-metadata-editing
name: wave-agent-and-bwf-metadata-editing
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, wave-agent-use, metadata-editing, bwf-editing, wave-agent, sound-devices, bwf, bext, ixml, bwf-metaedit, track-names, scene-take, poly-wav, sound-report, metadata-repair]
level: practitioner
status: draft
description: "Fix and finish production audio metadata with Sound Devices Wave Agent: scene/take, track names, notes, combining and splitting poly WAVs and generating sound reports, without breaking the files."
sources:
  - "https://www.sounddevices.com/product/wave-agent/ (Sound Devices - Wave Agent)"
  - "https://mediaarea.net/BWFMetaEdit (MediaArea - BWF MetaEdit)"
  - "https://tech.ebu.ch/publications/tech3285 (EBU Tech 3285 - Broadcast Wave Format)"
  - "http://www.gallery.co.uk/ixml/ (iXML specification)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wave Agent and BWF metadata editing

**Goal:** the files the assistant editor and dialogue editor receive carry correct
scene, take, track names and notes, so sync, AutoConform and dialogue splits work
without anyone listening to every file.

## 1. When to edit
- Slate was wrong on the recorder (scene renumbered, take mis-incremented).
- Track names missing or wrong (a lav swapped between actors mid-day).
- Circle takes and notes added after wrap.
- Files from a recorder that writes poor metadata (small field recorders, phones).

## 2. Work on copies
Edit metadata on the **day's delivery copy**, never on the original card or the
first backup. Log every change in the sound report notes.

## 3. Wave Agent (free, macOS/Windows)
- Open the folder; the grid shows Scene, Take, Tape, Notes, Circled, Track names, TC,
  frame rate, sample rate per file.
- Select multiple rows to batch-edit a column (e.g. set scene `42A` on 12 files).
- Edit track names per file - these land in **iXML** (`TRACK_LIST`) and are what Pro
  Tools/Resolve/Avid show as channel names.
- Play poly files with per-track mute/solo to confirm which mic is which before naming.
- **Combine** mono files from the same take into one poly WAV, or **split** poly to
  monos when post asks for it; check TC is preserved.
- *Export Sound Report* (CSV/PDF) from the edited metadata; the report must match the files.
- Rename files from metadata if the naming convention was broken.

## 4. bext vs iXML
- **bext** chunk (BWF): description, originator, time reference (samples since
  midnight - the timecode), coding history.
- **iXML**: scene, take, tape, notes, circled, track list, speed.
- Some apps read one, some the other. After editing, check both agree - BWF MetaEdit
  shows and edits bext and core fields and can validate files in bulk.
- Never alter the **time reference** unless deliberately fixing TC; it is the sync.

## Gotchas
- Editing on the card from the recorder's dock: a crash corrupts the only copy.
- Renaming files by hand in Finder/Explorer without changing metadata: conform tools
  match on metadata and break.
- Combining files with different lengths or start TC: misaligned tracks.
- Lowercase/extra spaces in scene names ("42a " vs "42A") break auto-sync matching.

## Verify
- [ ] Originals untouched; edits only on delivery copies.
- [ ] Scene/take/track names match the sound report.
- [ ] bext time reference unchanged; files still sync in a test import.
- [ ] Report exported after the final edit.
