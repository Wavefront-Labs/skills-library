---
id: creative-arts.animation.sound-design.clip-gain-levelling
name: clip-gain-levelling
category: creative-arts
field: animation
product: sound-design
tags: [clip-gain, item-gain, dialogue-levelling, dialogue-editing, pro-tools, reaper, pre-compression, loudness, vo]
level: practitioner
status: draft
description: "Level dialogue with clip gain before any compressor so every line hits the processing chain at a similar level, in Pro Tools, Reaper or by script."
sources:
  - https://www.avid.com/pro-tools
  - https://www.reaper.fm/userguide.php
  - https://ffmpeg.org/ffmpeg-filters.html#ebur128-1
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clip gain levelling before compression

**Goal:** lines and syllables arrive at the compressor within a few dB of each other, so it works gently and
consistently instead of squashing loud lines and ignoring quiet ones.

## Why clip gain first

Fader automation and compressors act after the insert chain or on the whole track. Clip (region/item) gain is
pre-insert: it changes what the plug-ins see. Levelling at the clip stage means one compressor setting fits the
whole character.

## How

- **Pro Tools:** Clip Gain line (Ctrl+Shift+- to show), or the clip gain fader on each clip; nudge with
  Ctrl+Shift+Up/Down; *Clip Gain > Render* bakes it.
- **Reaper:** item volume handle at the top of the item, or *Item properties* > volume; take volume envelope for
  syllable-level rides. Normalize items (*Item > Item processing > Normalize items*) to a common LUFS as a start.
- **Script:** measure each line's loudness, then gain to target:

```
ffmpeg -i line.wav -af ebur128=framelog=quiet -f null - 2>&1 | grep "I:"
ffmpeg -i line.wav -af "volume=3.5dB" line_lv.wav
```

## Targets

- Bring each line to about the same short-term loudness for that character (e.g. -20 to -23 LUFS short-term for a
  normal-level read) before the dialogue chain.
- **Keep performance dynamics:** a whisper should stay quieter than a shout, just less extremely (perhaps 6 dB apart
  instead of 20).
- Ride individual loud syllables or a dropped final word inside a line with clip gain breakpoints.

## Gotchas

- Clip gain is invisible to the mixer's automation; document that a track is levelled so nobody re-levels with faders.
- Normalising by peak instead of loudness makes lines with plosives quiet. Use LUFS/RMS.

## Verify

With the dialogue compressor inserted, its gain reduction meter shows a consistent 2-6 dB across lines rather than
0 dB on some and 15 dB on others. Next stage: `creative-arts.animation.sound-design.dialogue-eq-and-compression-chain`.
