---
id: creative-arts.animation.principles.walk-timing
name: walk-timing
category: creative-arts
field: animation
product: principles
tags: [animation, walk-cycle, walk-timing, stride, frames-per-step, cadence, walks, tempo, music-sync]
level: intro
status: draft
description: "Pick walk timing in frames per step for mood and size, match stride to speed, and sync walks to music or dialogue beats."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Walk_cycle
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Walk timing

Goal: choose how many frames each step takes so the walk's speed and mood are right.

## Williams' tempo guide at 24 fps (frames per step)
| Frames/step | Reads as |
|---|---|
| 4 | very fast run |
| 6 | run or fast walk |
| 8 | fast walk, cartoon walk |
| 12 | natural, brisk walk ("march time", 2 steps per second) |
| 16 | casual, strolling |
| 20 | slow, old or tired |
| 24 | very slow, deliberate |
A full cycle is two steps (e.g. 24 frames for a 12-frame step).

## Stride vs speed
- Speed = stride length / step time. Faster walks have both shorter step times and longer strides.
- Large characters: longer stride but slower tempo; small characters: short stride, fast tempo.
- Keep feet locked: in a progressive walk the planted foot must not move; in a cycle the
  ground speed equals stride / step frames per frame.

## Music and dialogue sync
- Match steps to the beat: 120 BPM = 2 beats/s = 12 frames per beat at 24 fps, so a 12-frame step
  lands contacts on beats. BPM to frames per beat = 60 * fps / BPM.
- Put contacts on the beat, or put the down (weight) on the beat for a heavier groove.
- In dialogue, align stressed syllables to contacts or downs where possible.

## Failure modes
- Uneven step lengths in a cycle (one step 12 frames, the other 13) - a limp.
- Ground speed mismatch - foot slide.
- Tempo not matching size (giant walking at 8 frames per step).

## Verify
- [ ] Both steps equal frames (unless a limp is intended).
- [ ] Feet locked to the ground at ground speed.
- [ ] Steps land on the music beat if synced.

Related: `creative-arts.animation.principles.walk-key-poses`,
`creative-arts.animation.principles.cycles-and-foot-slip`.
