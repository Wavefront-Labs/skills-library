---
id: creative-arts.film-live-action.film-editing.assistant-editing-dailies-and-bins
name: assistant-editing-dailies-and-bins
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, assistant-editor, assistant-editing, dailies, rushes, syncing-dailies, sync, timecode-sync, waveform-sync, pluraleyes, bin-organisation, bin-organization, bins, project-structure, folder-structure, naming-conventions, scene-take-naming, ale, lined-script, script-notes, circle-takes, selects-bins, kem-rolls, string-outs, group-clips, multigroup, subclips, markers, metadata, transcoding, dailies-codec, dnxhd, prores-proxy, lut-dailies, avid-media-composer, premiere-pro, davinci-resolve, backups, project-archiving, edit-project-template, edit-folder-structure, sync-by-timecode, waveform-syncing, string-out, selects-bin, group-clip, dailies-report, missing-footage, edit-backups]
level: practitioner
status: draft
description: "Run the cutting room as an assistant editor: sync dailies by timecode, build the bin structure and naming scheme, enter script notes and circle takes, make string-outs and group clips, keep backups."
sources:
  - "https://www.editorsguild.com/ (Motion Picture Editors Guild - assistant editor craft)"
  - "https://avid.secure.force.com/pkb/ (Avid Media Composer - AutoSync, group clips, ALE import)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Resolve - sync, bins, smart bins)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assistant editing: dailies, sync and bins

**Goal:** the editor opens a project where every take is synced, named by scene and
take, findable in seconds, with the script supervisor's notes attached - and nothing
that arrives from set is ever lost.

## 1. Receiving dailies
- From the DIT/lab: camera originals (or transcoded dailies with the show LUT baked),
  sound files (poly WAV with iXML), camera reports, sound reports, the **script
  supervisor's lined script and daily log**, and an **ALE/CSV** of metadata. Check every
  reel listed on the camera report arrived; count clips; checksum (MHL/xxHash) if you
  receive originals.
- Decide the **edit codec** in prep: DNxHD/HR 36-115 or ProRes Proxy/LT for offline;
  Avid wants MXF, Premiere/Resolve link natively. Transcode with the show LUT burned
  in plus timecode/clip name overlay (burn-ins) if the editor wants them; keep a clean copy.

## 2. Sync
- **Timecode sync** (jam-synced camera and recorder): Avid *AutoSync* by timecode, Resolve
  *Auto Sync Audio > Based on Timecode*, Premiere *Merge Clips* by timecode. Check the
  first few against the slate clap; drift beyond 1-2 frames on long takes means the
  cameras weren't jammed - fall back to waveform sync (Resolve/Premiere) or slate-by-hand.
- Second-system audio replaces camera scratch audio; keep the scratch track muted on
  a separate channel for reference. Verify **channel mapping**: mix track vs ISOs; the
  editor usually cuts with the mix track and keeps ISOs for sound post.
- Name synced clips `SC_TK` (e.g. `12A_3`), with camera letter for multicam (`12A_3_B`),
  and keep scene/take/camera in metadata columns so bins sort correctly.

## 3. Project and bin structure
A conventional layout (Avid style; mirror it in Resolve/Premiere bins):
```
01_DAILIES/        by shoot day: D01_2026-10-15, each with the day's synced clips
02_SCENES/         one bin per scene: all takes for that scene, sorted by take
03_SELECTS/        string-outs / KEM rolls per scene
04_SEQUENCES/      editor's cuts by version: SC12_v03, REEL1_v12, FILM_v07
05_SOUND/          music, SFX, temp VO
06_VFX/            temp comps, plates
07_GFX_TITLES/
08_ARCHIVE/        locked old versions
```
- **Columns**: scene, take, camera, circle (Y/N), shoot day, lens, notes, script page.
  Bin views saved per use (editor's view hides tech columns).
- Enter the **script supervisor's notes** per take (circle takes, "NG sound", "best for
  Marta", "pick-up from line X") - this is the editor's map.
- **Markers** on takes for the script notes' key moments speed up selects.

## 4. String-outs and group clips
- **String-out / KEM roll**: every take of a scene end to end in slate order, or a
  selects string-out of circled takes - the editor scrubs one sequence instead of forty clips.
- **Multicam**: Avid *group clips*/*multigroup*, Resolve *multicam clip*, Premiere
  *multi-camera source sequence* - grouped by timecode so the editor switches angles live.
- **Subclips** for long verite or interview takes, named by content.
- Lined script with scene/take coverage marked (the "lines" per take) scanned into the
  project (ScriptSync in Avid) if used.

## 5. Daily hygiene
- Project versions saved per day; the editor's bins locked when they're in them (Avid
  bin locking in shared storage; Premiere Productions; Resolve collaborative projects).
- **Backups**: media on RAID + a second copy; project files to a cloud/offsite nightly.
  Drive naming and a media log with what's where.
- A **missing/problem list** sent to the production each morning: reels not received,
  sync problems, takes missing from reports.
- Turnover prep is the assistant's job later (see picture lock and turnovers); keep
  naming and metadata clean from day one so it's possible.

## Gotchas
- Transcoding dailies without the show LUT - the director judges flat log for weeks.
- Scene/take typed inconsistently (`12a` vs `12A`); bins won't sort; ScriptSync breaks.
- ISOs dropped on transcode; sound post asks for them at the mix.
- Sync checked by eye on one take; day 3 reels drift 4 frames.
- Deleting "unused" originals to free space before picture lock.

## Verify
- [ ] Every reel and sound roll received, counted and checksummed against the reports.
- [ ] Sync verified on multiple takes per day; channel mapping documented.
- [ ] Scene bins complete with script notes and circle takes; string-outs for the editor's current scenes.
- [ ] Nightly backup of media index and project; missing list sent each morning.
