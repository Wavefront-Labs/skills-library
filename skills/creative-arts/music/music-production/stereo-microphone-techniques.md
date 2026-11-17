---
id: creative-arts.music.music-production.stereo-microphone-techniques
name: stereo-microphone-techniques
category: creative-arts
field: music
product: music-production
tags: [music-production, recording, microphone-technique, stereo-miking, xy-pair, ortf, spaced-pair, ab-pair, mid-side-recording, blumlein, decca-tree, mono-compatibility, 3-to-1-rule, ensemble-recording]
level: practitioner
status: draft
description: "Choose and set up stereo mic arrays (XY, ORTF, spaced AB, mid-side, Blumlein, Decca tree): exact angles and spacings, how each images, and mono-compatibility checks."
sources: ["https://www.dpamicrophones.com/mic-university/stereo-recording-techniques-and-setups", "https://www.shure.com/en-US/insights/stereo-microphone-techniques", "Berklee Music Production and Engineering core curriculum"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stereo microphone techniques

**Goal:** a stereo recording with a believable image that survives mono playback.

## 1. The arrays
| Technique | Mics and setup | Image | Mono |
|---|---|---|---|
| **XY** | 2 cardioids, capsules coincident (one above the other), **90-135 degrees** apart | level differences only; precise, narrower | excellent |
| **ORTF** | 2 cardioids, **17 cm apart, 110 degrees** | natural width and some air | good |
| NOS | 2 cardioids 30 cm apart, 90 degrees | wider | fair |
| **Spaced pair (AB)** | 2 omnis (usually) 0.5-3 m apart | spacious, less precise centre; time differences | can comb-filter |
| **Mid-side (M/S)** | cardioid (or omni) pointing forward + **figure-8 sideways**, coincident | decode: L = M+S, R = M-S; width adjustable after | perfect (mono = mid) |
| **Blumlein** | 2 figure-8s coincident at 90 degrees | very natural, includes room equally front and back | good |
| Decca tree | 3 omnis in a T (~2 m wide, centre mic ~1-1.5 m forward) | orchestral, big, stable centre | fair |

## 2. Choosing
- Small source, close (acoustic guitar, piano in a pop mix): XY or ORTF.
- Choir, orchestra, good hall: spaced omnis or Decca tree, plus spot mics.
- Unknown final width or broadcast/mono deliverables: **M/S** (adjust side level in mixing).
- Drum overheads: see drum-miking skill (spaced pair or XY variants).

## 3. Decoding M/S in a DAW
- Record M and S to separate mono tracks. Duplicate S, invert polarity of the copy, pan S hard left and inverted-S hard right, M centre. Group S tracks and use their level as a width control. Or use an M/S decoder plugin.

## 4. Placement method
1. Find the best listening position for the ensemble in the room.
2. Put the array there (often at or above head height, slightly behind the conductor for ensembles).
3. Adjust distance: closer = wider image and drier; further = narrower and more room.
4. Monitor on headphones and speakers; walk the array forward/back in 30 cm steps.

## Gotchas
- **3:1 rule** for spot mics vs main pair: other mics at least 3x the distance from each other as from their source.
- Spaced pair too wide = "hole in the middle".
- XY capsule misalignment: capsules must be vertically aligned or you add time differences.

## Verify
- Mono sum check: no thin, phasey tone.
- Sources across the ensemble appear in their actual left-to-right positions on playback.
