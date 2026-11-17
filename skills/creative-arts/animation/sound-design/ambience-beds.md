---
id: creative-arts.animation.sound-design.ambience-beds
name: ambience-beds
category: creative-arts
field: animation
product: sound-design
tags: [ffmpeg, ambience, room-tone, atmosphere, pad, drone, bed, mix, ducking, sidechain, loudnorm, no-music-tool]
level: advanced
status: verified
description: "Generate atmosphere + pad beds with ffmpeg alone, duck them under dialogue, and master to broadcast loudness - a scored-feeling mix with no music tool or assets."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ambience + pad beds with ffmpeg (fill the silence, no music tool)

A cut with only dialogue over silence feels unfinished and exposes every gap. Before
committing to a real scoring tool, you can give an episode a **present, atmospheric
soundtrack using ffmpeg alone** — a synthesised atmosphere/room-tone bed plus a slow
harmonic pad, ducked under the dialogue and mastered to spec. This is *atmosphere, not
melody* (no themes/hooks — that's the scoring pass), but it's enough to review a cut as
a finished piece and it ships with zero external assets or dependencies.

## The three stems
1. **Dialogue** — the VO already on the cut's timeline. Band-limit + even it out:
   `highpass=f=80, lowpass=f=12000, dynaudnorm` (gentle levelling without pumping).
2. **Atmosphere / room tone** — filtered noise, very low:
   `anoisesrc=color=pink:amplitude=...`, then `highpass~90, lowpass~1800, volume~0.05`.
   Pink noise shaped this way reads as air/room/street hum, not hiss.
3. **Pad** — a slow harmonic drone built from detuned `sine` sources on a chord (e.g. a
   minor triad C3/Eb3/G3 = 130.8/155.6/196.0 Hz for an eerie mood), summed and softened
   with `tremolo` (slow), `aecho` (reverb tail), `lowpass`, and a low `volume~0.06`.
   Pick the chord for the mood; keep it a pad, not a tune.

## The mix (duck the bed under dialogue)
- Sum pad + atmosphere into one **bed**.
- **Sidechain-duck** the bed by the dialogue so speech always sits on top:
  `[bed][dialogueKey]sidechaincompress=threshold=0.06:ratio=8:attack=12:release=320`.
  Split the dialogue with `asplit` so one copy is the sidechain key and one is mixed dry.
- Sum the dry dialogue + ducked bed.
- **Master**: `loudnorm=I=-14:TP=-1.5:LRA=11` (YouTube/stream target). Encode AAC 384k 48k,
  `+faststart`. Keep the video stream copied (`-c:v copy`) — only the audio is rebuilt.

## Per-scene variation
Drive the atmosphere/pad per sequence from the shotlist (one location per sequence is
common): street hum for exteriors, soft room tone for interiors, a darker/low drone for
dread scenes. Match the pad chord + atmosphere filter to the color-script mood of each
sequence, then concatenate the per-sequence beds to the episode length.

## Honest limits
- No melody, motifs, or hits — a real score (scoring skill, e.g. Sonic Pi + a soundfont)
  replaces the pad later. This is the review-cut / temp-track tier.
- Generated noise/sines can sound synthetic if pushed; keep levels low and let dialogue lead.

## Verify
- [ ] The finished cut has continuous sound (no dead silence between lines).
- [ ] Dialogue is always clearly on top; the bed audibly dips under speech and swells in gaps.
- [ ] Integrated loudness measures ~-14 LUFS and true peak ≤ -1.5 dBTP (`ffmpeg ... ebur128`
      / a loudnorm print). 
- [ ] Video is bit-identical (stream-copied); only audio changed.

**Verified (proof):** built as production `build_audio.py` (pad = detuned sines +
tremolo + aecho; pink-noise atmosphere; sidechain duck; loudnorm). Run on the SQ04 cut
it produced a finished mix measuring **-14.4 LUFS integrated**, dialogue sitting on top.

See dialogue-mix-master (dialogue levelling + ducking detail), scoring (the real-music
pass that replaces the pad), sfx-design (spot effects on top), encode-delivery/youtube-master.
