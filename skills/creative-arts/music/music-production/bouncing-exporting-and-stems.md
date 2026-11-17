---
id: creative-arts.music.music-production.bouncing-exporting-and-stems
name: bouncing-exporting-and-stems
category: creative-arts
field: music
product: music-production
tags: [music-production, logic-pro, pro-tools, daw, bounce, stem-export, bounce-mix, export-all-tracks, track-bounce, offline-bounce, dither, file-formats, deliverables, consolidated-files]
level: practitioner
status: draft
description: "Bounce mixes and export stems or multitracks from Logic Pro and Pro Tools: ranges, offline vs real-time, formats, dither, and delivery checks."
sources: ["https://support.apple.com/guide/logicpro/ (Bounce your project; Export tracks as audio files)", "https://www.avid.com/pro-tools (Pro Tools Reference Guide - Bounce Mix, Track Bounce)", "https://www.grammy.com/ (Recording Academy P&E Wing delivery recommendations)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bouncing, exporting and stems (Logic, Pro Tools)

**Goal:** correct deliverables first time: mixes, stems and multitrack exports that line up.

## 1. Mix bounce
- **Logic**: set the cycle range (start at bar 1 or the song start, include tails), File > Bounce > Project or Section (Cmd+B). Choose PCM WAV, resolution 24-bit, project sample rate, **Offline** (faster) unless hardware/external instruments require Realtime. Normalize off. Dither only when reducing to 16-bit.
- **Pro Tools**: select the range on the timeline, File > Bounce Mix (Cmd+Opt+B): source = main output, WAV, interleaved, 24-bit, session rate, **Offline** option. Add MP3 only if needed.

## 2. Stems (with processing)
- Logic: File > Export > **All Tracks as Audio Files** (or selected; options for including effects, volume/pan automation, and bounce tails); or solo each bus and bounce. Pro Tools: **Track Bounce** (select buses or tracks, right-click > Bounce) to bounce several sources in one pass offline.
- Decide and label: with or without master-bus processing; with or without send effects included (bus-based stems include returns if routed).

## 3. Multitrack (consolidated) exports for another engineer
- Every track rendered as a full-length file from the same start point (bar 1 or 1:00:00:00), no fades/gaps; dry unless instructed; MIDI exported as audio **and** MIDI files.
- Include tempo map info (tempo/key in file names or a notes file) and a rough mix.

## 4. File naming
`Artist_Song_MixV3_48k24b.wav`, stems `Artist_Song_STEM_Drums.wav`, multitracks `01_Kick_In.wav`...

## Gotchas
- Cycle/selection ending too early: reverb tail cut off.
- Hidden muted regions or bypassed plugins included unexpectedly; double-check soloed/muted states.
- Offline bounce with external hardware inserts produces silence on those tracks.

## Verify
- Import all stems into a new session at zero with faders at unity: the sum matches the mix (null test if master processing excluded).
- Spot-check files for start alignment, length, format and clipping.
