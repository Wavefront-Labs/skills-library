---
id: creative-arts.animation.voice-tts.vo-file-naming
name: vo-file-naming
category: creative-arts
field: animation
product: voice-tts
tags: [vo-naming, vo-post, line-ids, script-breakdown, dialogue-database, take-numbers, file-naming, recording-script, csv]
level: practitioner
status: draft
description: "Give every dialogue line a permanent ID from the script and name VO files by episode, character, line and take, so recording, TTS, edit and lip sync stay linked."
sources:
  - https://mediaarea.net/BWFMetaEdit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VO line IDs and file naming

**Goal:** any audio file can be traced to its script line, character, take and status, and any script line can
find its audio, through script revisions, pickups and localisation.

## Line IDs

- Assign IDs when the recording script is locked: `EP104_042` (episode + sequential line number), or
  `EP104_SC05_012` if scenes are stable.
- IDs are permanent: a cut line keeps its ID retired; inserted lines get suffixes (`EP104_042A`).
- Keep the script breakdown as data (CSV/sheet): line ID, character, scene, text, direction notes, status.

## File names

```
<SHOW>_<EP>_<LINEID>_<CHARACTER>_T<take>[_<status>].wav
SHOW_EP104_042_MIA_T03_circled.wav
SHOW_EP104_042_MIA_T03_tts-v2.wav          # TTS generation, model/version tag
SHOW_EP104_042_MIA_FR_T01.wav               # localisation: language code
```
- No spaces, ASCII only, fixed field order (sortable).
- Status in metadata or a folder (`selects/`) rather than renaming files many times.

## Metadata

Write line ID, character and text into BWF/iXML description (`creative-arts.animation.sound-design.bwf-ixml-metadata`)
so renamed copies stay identifiable.

## Downstream links

- Editorial uses line IDs as clip names; spotting/ADR lists reference them.
- Lip-sync tools take line ID + audio + text (`creative-arts.animation.pipeline.vo-lipsync-pipeline`).
- Subtitles and dubbing scripts key off the same IDs.

## Gotchas

- Renumbering lines after a script revision breaks every link; never renumber, only insert with suffixes.
- Character names change (working titles); use a stable character code.

## Verify

Pick five random files in the cut: each resolves to a script line in the breakdown sheet with matching text, and
each script line marked recorded has a selected take on disk.
