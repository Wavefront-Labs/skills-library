---
id: creative-arts.music.music-production.drum-editing-and-audio-quantise
name: drum-editing-and-audio-quantise
category: creative-arts
field: music
product: music-production
tags: [music-production, beat-detective, elastic-audio, flex-time, drum-editing, audio-quantize, multitrack-editing, slip-editing, crossfades, phase-locked-quantize, pro-tools, logic-pro, tightening-drums]
level: practitioner
status: draft
description: "Tighten multitrack drums without phase problems: Beat Detective, Elastic Audio, Logic Flex Time with phase-locked groups, manual slice editing, and how tight to go."
sources: ["https://www.avid.com/pro-tools (Pro Tools Reference Guide - Beat Detective, Elastic Audio)", "https://support.apple.com/guide/logicpro/ (Flex Time and quantize-locked groups)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drum editing and audio quantise

**Goal:** tighter drums that still sound like a drummer, with no phase artefacts between mics.

## 1. Decide how tight
- Fix obvious flams and drift; don't quantise the feel out. Many productions only fix fills and big errors; genres like modern metal/pop expect grid-tight.
- Quantise strength 50-90% keeps some human feel.

## 2. Keep phase lock
- All drum mics must be edited **together** (group them) so edits happen at the same sample on every mic. Editing tracks separately = phasey, flammy drums.

## 3. Pro Tools: Beat Detective (slice and crossfade)
1. Group all drum tracks; select the section (whole bars).
2. Beat Detective: **Clip Separation** mode, analyse (High Emphasis or Low Emphasis/Enhanced Resolution), adjust sensitivity so triggers land on kick/snare hits (use kick and snare as the detection source with Collection mode if needed).
3. **Separate**, then **Conform** (strength %, exclude within to leave near-grid hits alone, swing).
4. **Edit Smoothing**: fill gaps and crossfade (e.g. 5 ms).
- **Elastic Audio** (Rhythmic/Polyphonic) is a stretching alternative: warp markers move audio without slicing; quicker but may add artefacts.

## 4. Logic: Flex Time
- Put drum tracks in a group with **Quantize-Locked (Editing Selection)** and Phase-Locked enabled (Group Settings), set Flex mode **Slicing** (cleanest for drums) or Rhythmic.
- Set a quantise value on the group's regions; or manually drag transient markers on the reference track (kick/snare) with phase lock carrying the others.

## 5. Manual editing
- Cut just before transients at a zero crossing, slide the hit, crossfade (2-10 ms), fill gaps with copied ambience if necessary.

## Gotchas
- Double transients where a slice crossfade overlaps a cymbal; adjust crossfade position or length.
- Stretching cymbal decays produces warbling; prefer slicing.
- Quantising a band recorded without a click to a fixed grid: create a tempo map that follows the band first.

## Verify
- Solo overheads: no doubled hits or clicks at edit points.
- Listen to the whole kit in context: tighter but still grooving.
