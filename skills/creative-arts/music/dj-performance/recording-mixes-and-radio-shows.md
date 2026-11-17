---
id: creative-arts.music.dj-performance.recording-mixes-and-radio-shows
name: recording-mixes-and-radio-shows
category: creative-arts
field: music
product: dj-performance
tags: [dj-performance, set-programming, crowd-reading, mix-recording, radio-mix, podcast-mix, mixcloud, record-output, recording-levels, loudness-normalisation, tracklist, cue-sheet, voice-breaks, radio-show]
level: practitioner
status: draft
description: "Record DJ mixes and radio shows: recording levels from the mixer, avoiding limiter crunch, editing and mastering lightly, loudness for platforms, tracklists, and voice breaks."
sources: ["https://www.mixcloud.com/ (upload and licensing guidance)", "https://www.pioneerdj.com/ (DJM mixer manuals - REC OUT and booth/master levels)", "https://tech.ebu.ch/publications/r128"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recording mixes and radio shows

**Goal:** a clean, well-levelled mix recording ready for streaming platforms or broadcast.

## 1. Signal and levels
- Record from the mixer's **REC OUT** or a dedicated record output (independent of master volume), into an interface or the DJ software's recorder.
- Keep channel meters peaking around 0 dB on the mixer (not in the red); record at **-12 to -6 dBFS** peaks, 24-bit.
- The mixer's master limiter or software auto-limiter clipping audibly = levels too hot. Gain-stage tracks to equal loudness with trims, not by pushing channel faders.

## 2. Performance
- Plan the arc (see energy-curve skill) and tracklist; rehearse tricky transitions.
- For radio: include **station IDs/voice breaks** where required; script short links (artist, title, upcoming).

## 3. Post-processing
- Trim start/end, fix any obvious level jumps (clip gain), light compression/limiting for consistency: target around **-14 LUFS integrated, -1 dBTP** for streaming; broadcasters supply their own spec (EBU R128: -23 LUFS).
- Export WAV for archive; MP3 320 or AAC for upload.

## 4. Metadata and rights
- Tracklist with timestamps (artist - title - label); some platforms (Mixcloud) require tracklists and handle licensing; YouTube and others may block copyrighted mixes.
- Artwork, description, genre tags.

## Gotchas
- Recording the booth output (affected by booth EQ/level) instead of the master/rec out.
- Software recording through a laptop's internal sound card while performing from an external one.
- Normalising a clipped recording doesn't remove the distortion.

## Verify
- Loudness meter on the final file: within target, true peak under -1 dBTP.
- Listen through transitions in the recording: no clipping or level jumps.
