---
id: creative-arts.animation.sound-design.atsc-a85-broadcast-loudness
name: atsc-a85-broadcast-loudness
category: creative-arts
field: animation
product: sound-design
tags: [atsc-a85, loudness, broadcast-loudness, lkfs, true-peak, calm-act, bs1770]
level: advanced
status: draft
description: "Mix and verify animation to ATSC A/85 broadcast loudness: -24 LKFS dialogue-gated target, the tolerance, true-peak ceiling, measurement method and common failures."
sources:
  - https://www.atsc.org/
  - https://www.itu.int/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ATSC A/85 broadcast loudness

ATSC A/85 (Techniques for Establishing and Maintaining Audio Loudness for Digital Television) is the North American practice document that broadcasters use to meet the US CALM Act requirement. It measures loudness with the ITU-R BS.1770 algorithm.

## Targets (check the current edition and the broadcaster's own spec)
- **Programme loudness target: -24 LKFS**, measured over the entire programme (long-form), commonly with a tolerance of **+/- 2 dB**. A/85 uses dialogue-gated measurement for programmes where dialogue anchors the mix.
- **True-peak ceiling:** a limit of **-2 dBTP** is the figure usually quoted from A/85; confirm against the delivery spec as networks differ.
- A broadcaster's own delivery spec takes precedence over the generic number. Always read it.

## How to measure
1. Use a BS.1770-compliant meter (hardware or plug-in).
2. Measure the **final printed mix** over the whole programme from the first to last programme frame, excluding bars, slates and commercial breaks.
3. If the spec asks for dialogue-gated loudness, the meter must have a speech-detection gate; use the dialogue-anchored reading as the compliance number and keep the other read as a reference.
4. Measure the 5.1 mix and the stereo fold-down (see `surround-mix-and-fold-down.md`) separately, since each file is judged on its own.

## Mixing to the target
- Set the dialogue anchor level first; then balance music and effects to it. In animation, a loud music or SFX-heavy show can push the loudness measure up while dialogue sounds quiet.
- Use compression and limiting sparingly. Aim for the programme to land within tolerance without having to apply a heavy limiter at the end.
- If the mix is off, adjust the overall level of the final mix by a fixed gain rather than re-limiting.

## Common failures
- Measuring a short segment instead of the whole programme.
- Using a meter set to ITU-R BS.1770 without gating, then reading a number that does not match what QC measures.
- True peaks over the ceiling after MP3 or AAC encoding. Check the encoded file as well.

## Verify
- [ ] Integrated loudness is -24 LKFS (+/- 2 dB, or the broadcaster's own figure).
- [ ] True peak is within the ceiling in the final delivery file.
- [ ] Separate readings were logged for 5.1 and stereo versions.
