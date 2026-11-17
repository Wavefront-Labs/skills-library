---
id: creative-arts.animation.sound-design.whoosh-and-impact-design
name: whoosh-and-impact-design
category: creative-arts
field: animation
product: sound-design
tags: [whoosh-impact, whoosh, designed-sfx, swish, transitions, pass-by, sound-design, doppler, ffmpeg, sox]
level: practitioner
status: draft
description: "Design whooshes and swishes for fast animated motion and transitions: sources, shaping the envelope to the move, pitch/doppler, stereo movement and syncing the peak."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html
  - https://sox.sourceforge.net/sox.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designed whooshes

**Goal:** a whoosh whose shape matches the motion it accompanies: a fast arm swing, a whip pan, a character
zipping off-screen, a title flying in.

## Anatomy

A whoosh has a rise, a **peak** (the moment of fastest motion or closest pass) and a fall. The peak syncs to the
fastest frame (often the smear frame in animation) or the cut point in a whip-pan transition.

## Sources

- Recorded: a thin stick or cane swung past the mic, a cloth flick, a fast breath past a mic, a pass-by recorded
  with a moving mic.
- Synthesised: filtered noise with a moving band-pass (sweep), works for stylised shows.

## Building with ffmpeg / sox

```
# 0.6 s pink-noise whoosh: fade in to a peak at 0.35 s, fade out, band-passed
ffmpeg -f lavfi -i "anoisesrc=d=0.6:c=pink:a=0.5" -af "afade=t=in:st=0:d=0.35:curve=exp,afade=t=out:st=0.35:d=0.25,bandpass=f=1200:w=900" whoosh.wav
# rising pitch flavour for a zip-off (sox): pitch bend up
sox whoosh.wav zip.wav bend 0,600,0.5
```
For a sweep, automate a band-pass centre frequency upward to the peak and down after (in the DAW or with ffmpeg's
`sendcmd` to change `bandpass` frequency).

## Shaping to picture

- Duration equals the visible motion; the peak lands on the fastest frame.
- **Doppler:** pitch higher approaching, lower leaving, for pass-bys.
- Stereo: pan following screen motion, left to right with the object.
- Layer a low "sub whoosh" for heavy objects, a high "air" layer for light ones.
- Variation: never the same whoosh for consecutive swings; vary pitch and length.

## Gotchas

Too many whooshes makes a cartoon tiring; spot them deliberately and let some motion be silent. Transitions
whooshes in titles must leave room for dialogue.

## Verify

Play against picture at full speed and frame-step around the peak: the loudest point is within one frame of the
fastest motion frame, and panning follows the motion. Related: `creative-arts.animation.sound-design.sfx-design`.
