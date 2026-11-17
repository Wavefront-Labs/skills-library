---
id: creative-arts.animation.sound-design.dialogue-gated-loudness-for-streaming
name: dialogue-gated-loudness-for-streaming
category: creative-arts
field: animation
product: sound-design
tags: [dialogue-gated, loudness, streaming-loudness, netflix-audio, bs1770, dialogue-anchor, true-peak]
level: advanced
status: draft
description: "Mix to a dialogue-gated loudness target for streaming platforms: how gating works, the Netflix-style anchor figure, true peak, LRA and checking the whole programme."
sources:
  - https://www.itu.int/
  - https://tech.ebu.ch/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dialogue-gated loudness for streaming

Streaming platforms commonly set a loudness target measured only while dialogue is present, so quiet dialogue-driven programmes are not judged on their loud music or effects alone.

## Concept
- ITU-R BS.1770 defines how to measure loudness: K-weighting, then a gated average. The standard gating blocks (absolute gate at -70 LUFS and a relative gate 10 LU below the ungated level) exclude silence and quiet passages from an **integrated** reading.
- **Dialogue gating** adds a speech detector. Only the passages the detector classes as dialogue contribute to the measurement. The detector is a feature of specific meters. Different meters can return different readings on the same file, so use the meter the platform names.
- The result is an anchor number: the average loudness of speech in the programme.

## Netflix-style target (verify the current spec before delivering)
- Netflix's published audio spec has asked for dialogue-gated programme loudness around **-27 LKFS with a +/- 2 LU tolerance** and a true-peak limit around **-2 dBTP**, with a check of the loudness range. Confirm these numbers in the current Netflix delivery spec; they are revised from time to time and differ by deliverable type.
- Other platforms differ: some do not state dialogue-gated numbers and simply normalise on playback, so deliver to the platform's own document.

## Mixing workflow
1. Mix dialogue to sit consistently. Print the mix.
2. Measure with the specified meter in dialogue-gated mode over the entire programme.
3. Adjust the overall level in one move rather than reshaping dynamics, until the anchor is in tolerance.
4. Check true peak on the final file, and again after any lossy encode used for review.
5. Record the measured numbers on the delivery paperwork.

## Gotchas
- Do not trust the reading of an ungated meter when the spec calls for gated.
- For stereo and 5.1 deliverables, measure each separately. A fold-down is not automatically in tolerance.
- Short-form or promo spots may be measured differently than the long-form programme. Read the spec for each.

## Verify
- [ ] The meter and gating mode match the spec's wording.
- [ ] Integrated dialogue-gated level is within tolerance across the whole programme.
- [ ] True peak is under the ceiling on the delivery file.
