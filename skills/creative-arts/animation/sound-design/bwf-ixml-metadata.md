---
id: creative-arts.animation.sound-design.bwf-ixml-metadata
name: bwf-ixml-metadata
category: creative-arts
field: animation
product: sound-design
tags: [bwf, audio-sync, ixml, bext-chunk, timecode-reference, broadcast-wave, metadata, bwfmetaedit, scene-take, vo-recording-metadata]
level: practitioner
status: draft
description: "Read and write Broadcast WAV (bext) and iXML metadata: time reference for sync, scene/take/notes for VO sessions, and tools like BWF MetaEdit and ffprobe."
sources:
  - https://tech.ebu.ch/publications/tech3285
  - http://www.gallery.co.uk/ixml/
  - https://mediaarea.net/BWFMetaEdit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BWF and iXML metadata

**Goal:** audio files that carry their own sync timecode and session info, so dialogue, ADR and field
recordings land in the right place and stay identifiable for years.

## Broadcast WAV (EBU Tech 3285)

A WAV with a `bext` chunk containing:
- **Description** (256 chars), **Originator**, **OriginatorReference**, **OriginationDate/Time**.
- **TimeReference**: samples since midnight of the first sample. At 48 kHz, TC 01:00:00:00 = 172,800,000.
  DAWs use it to "spot to original timestamp".
- **UMID**, loudness fields (version 2: LoudnessValue, MaxTruePeakLevel...).

## iXML

An XML chunk used by recorders and DAWs: project, scene, take, tape, circled flag, notes, track names
(`TRACK_LIST`), speed/frame rate, timecode rate and flag. Essential for multitrack VO and Foley sessions.

## Tools

```bash
ffprobe -v error -show_entries format_tags -of default=nw=1 take.wav   # shows bext fields as tags
bwfmetaedit --out-core=core.csv *.wav                                  # read core metadata to CSV
bwfmetaedit --Description="EP104 MIA line 042 take 3" --OriginatorReference=EP104_042_T3 take.wav
```
BWF MetaEdit (MediaArea) also edits/imports CSV in bulk and verifies MD5 of audio data.

## In a VO session

Set the recorder/DAW to write scene = line ID, take number, circled takes and notes; name files to match
(`creative-arts.animation.voice-tts.vo-file-naming`). The metadata then survives renames.

## Gotchas

- Many tools strip bext/iXML on export ("bounce" or "convert"); check after each step.
- TimeReference depends on sample rate; a resampled file needs it recalculated, which SRC tools may not do.
- ffmpeg can write some bext fields (`-write_bext 1` with metadata) but not iXML; use BWF MetaEdit or the DAW.

## Verify

Import a file into the DAW with "spot to original time": it lands at its recorded timecode; ffprobe/BWF MetaEdit
shows the description and originator reference you set.
