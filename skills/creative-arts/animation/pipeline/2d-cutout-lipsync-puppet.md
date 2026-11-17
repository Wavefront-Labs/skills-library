---
id: creative-arts.animation.pipeline.2d-cutout-lipsync-puppet
name: 2d-cutout-lipsync-puppet
category: creative-arts
field: animation
product: pipeline
tags: [2d, cutout, puppet, lip-sync, rhubarb, mouth-shapes, on-twos, blink, head-bob, pillow, ffmpeg, python, dialogue, talking-head, anime, rick-and-morty, compositing, plate]
level: practitioner
status: verified
description: "Drive a 2D cutout character from Rhubarb cues: 4 mouth shapes, drawings on twos, blink cadence, onset head dip, PIL compositing over a plate, ffmpeg concat with the VO."
sources: [https://github.com/DanielSWolf/rhubarb-lip-sync]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# 2D cutout lip-sync puppet

A talking shot from a drawn character without re-drawing anything per frame.
Verified: 3.3 s line → 40 drawings, identity constant, mouth readable, over a painted
plate, in under 30 s of CPU.

## Inputs
- A character split into **body** (static raster) and **head** (rendered per state by
  `creative-arts.animation.vector-graphics.parametric-features-over-traced-master`).
- The line's WAV and its Rhubarb JSON (`mouthCues` with `start`, `end`, `value`).
- A painted plate (see `creative-arts.animation.pipeline.painted-background-plates`).

## Mouth map (Rhubarb → 4 shapes)
```
X closed  A closed  B small  C open  D wide  E open  F small  G small  H open
```
Four drawn shapes cover TV dialogue; more shapes add flicker, not clarity.

## Timing rules
- **On twos**: render every second frame at 24 fps and hold each drawing 2 frames
  (`duration 0.083333` in the ffmpeg concat list). Mouths read better on twos than on
  ones because each shape is held long enough to register.
- **Blink**: every ~2.8 s, two consecutive frames of `closed` eyes, first blink at
  ~1.4 s so the shot never opens on a blink.
- **Head dip on vowel onsets**: at the start of every C/D/E/H cue, drop the head
  10 px and recover linearly over 6 frames. This is the cheapest "alive" signal and
  it sells the emphasis without animating anything else.
- **Slow settle**: add ~1 px per second of drift to body and head so a held pose is
  never a frozen image.

## Compositing
Cache head rasters per `(mouth, eyes)` state; there are at most 8. Per frame:
`plate.copy()` → `alpha_composite(body, (ox, oy + settle))` →
`alpha_composite(head, (ox + off_x, oy + off_y + dip + settle))` → save RGB PNG.
Framing for a Daima-style CLOSE: head height ≈ 65 % of frame height (700 px at
1080p), face centre at 50 % of width, chin at 90 % of height, hair top near the frame
edge. The 44 %/chin-at-72 % framing read as a webcam. MED: head ≈ 300 px.
After compositing body + head into one RGBA layer, run
`creative-arts.animation.pipeline.2d-character-scene-lighting-pass` before the plate.

## Encode
```
ffmpeg -f concat -safe 0 -i list.txt -i line.wav -map 0:v -map 1:a -t <dur> \
       -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -shortest out.mp4
```
`<dur>` = last cue end + 0.4 s so the mouth closes on screen before the cut.

## Verify
Extract 6 frames across the shot: mouth state changes between frames, eyes close in
exactly one pair, head position varies by ≤ 12 px, nothing else moves. Then play it
beside a benchmark dialogue clip (Rick and Morty, Daima) at the same size and listen
for sync: an open mouth on a consonant means the map or the cue offset is wrong.
