---
id: creative-arts.film-live-action.production-sound.sound-reports-and-ixml-metadata
name: sound-reports-and-ixml-metadata
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, production-sound-mixer, sound-reports, sound-report, sound-metadata, ixml, bwf, bext, broadcast-wave, track-naming, track-names, scene-take-metadata, circle-take, false-start, wild-track, notes, pdf-sound-report, csv-sound-report, sound-devices-report, wave-agent, sound-report-app, metadata-handoff, editorial, post-handoff, timecode-metadata, ubits, user-bits, file-naming, roll-naming, sound-roll, tape-name, project-name, dailies-sync, avid-ale, resolve-metadata, sound-report-fields, track-naming-conventions, metadata-entry, recorder-metadata, sound-report-delivery, notes-for-post, wild-track-notes]
level: practitioner
status: draft
description: "Record metadata that makes post fast: scene/take/notes in iXML and BEXT at the time of recording, track names and roll numbers, circle/false-start/wild flags, daily PDF/CSV sound reports."
sources:
  - "https://www.sounddevices.com/support/ (Sound Devices - metadata, sound reports, Wave Agent)"
  - "http://www.ixml.info/ (iXML specification)"
  - "https://tech.ebu.ch/publications/tech3285 (EBU Tech 3285 - BWF/bext chunk)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sound reports and iXML metadata

**Goal:** every audio file says what it is - scene, take, which actor is on which track,
what went wrong - so dailies sync is automatic and the dialogue editor never has to
guess which ISO is the boom.

## 1. What lives where
- **BWF/bext chunk**: originator, date/time, **timecode start** (as time reference
  samples), description. Every pro recorder writes it; NLEs read it for sync.
- **iXML chunk**: project, scene, take, **tape/roll**, **track names** per channel,
  circle take, note, user bits, file family (poly/mono), sample rate/bit depth, and the
  *history*. Avid (via ALE), Resolve, Premiere, Pro Tools (field recorder workflow) all
  read iXML - **track names are the single most useful field** for post.
- **File name** should carry it too: `Scene-Take` style (`12A-03.wav`), or the
  recorder's `TapeName_SceneTake` pattern; set the recorder's file-naming scheme so the
  name alone identifies the take if metadata is lost.

## 2. On the recorder, every take
Set at the start of the day: **project** name, **roll/tape** (`SR001`, increment per
card or per day per house style), **track names** (`BOOM`, `MARTA LAV`, `DEV LAV`,
`PLANT TABLE`, `MIX L/R`), timecode frame rate, user bits (date is a common convention).
Per take (from the slate/script supervisor, before or right after rolling):
- **Scene** (`12A`), **take** (auto-increments; correct it when takes are repeated or
  skipped), set **circle** (good take), **false start** (very short, don't waste a
  number), **wild track / wild line** (`WT` / `WL` prefix or the recorder's flag), and
  a **note** ("plane over line 4", "lav rustle Marta", "boom only after cut", "room tone
  30s", "MOS - no sound").
- Many recorders accept scene/take via a Bluetooth/USB keyboard, a tablet app (Sound
  Devices Wingman, Zaxcom ZaxNet, Ambient) or from the smart slate.

## 3. The sound report
Generated from the recorder (Sound Devices: *Reports* menu -> CSV/PDF on the card;
Wave Agent builds/edits reports from the files) or an app (Sound Report Writer, Pomfort
Metadata) and completed by the mixer with the header: production, date, shoot day,
location/set, mixer and boom op names, recorder, sample rate/bit depth, frame rate,
timecode mode, mics per track (model and who wore it), **track layout**.
Per line: file name, scene, take, duration, TC start, circle, notes.
Footer: wild tracks and room tones listed with their scene, any sync caveats (cameras
re-jammed at 14:10), RF hits, and "to post" requests ("line 3 unusable - needs ADR").
Deliver as **PDF + CSV** with the day's media folder (same name as the sound roll),
and email to editorial/post sound and the script supervisor.

## 4. Handoff hygiene
- Folder per roll: `SR001/` with WAVs, the report PDF/CSV, and a copy of the channel
  plan. Checksummed copy by the DIT (MHL) like camera media.
- Keep file names unique across the show (roll prefix); avoid spaces and slashes in
  scene names (`12A` not `12 A/B`).
- If a take is retroactively renamed (slate was wrong), fix it in Wave Agent and note
  it in the report - don't rename only the file.
- Check with editorial on day 1 that their sync tool reads your track names and
  scene/take (Avid: *Import > Audio with metadata > iXML*; Resolve: Metadata panel).

## 5. Why post cares
Dialogue editors sort ISOs by track name across thousands of files; sound reports tell
them where the wild lines and room tones are and which lines were flagged for ADR.
Dailies syncs on timecode and matches scene/take between camera reports and sound. One
wrong roll name or an unnamed `Track 3` costs hours downstream.

## Gotchas
- Track names left as `Ch 1`...`Ch 6`.
- Scene/take entered after the take and forgotten on the next; metadata out of step.
- Wild tracks recorded with the previous scene's metadata; found by nobody.
- Roll name reused on a new day; duplicate file names overwrite on ingest.
- Report written at wrap from memory; notes vague or wrong.

## Verify
- [ ] Project/roll/track names/frame rate set before the first take; file naming includes scene-take.
- [ ] Every take has scene, take, circle/false/wild flags and a note where relevant, entered at the time.
- [ ] PDF + CSV report with header, track layout, wilds/room tones and ADR flags delivered with the media daily.
- [ ] Editorial confirmed on day 1 that iXML fields import correctly.
