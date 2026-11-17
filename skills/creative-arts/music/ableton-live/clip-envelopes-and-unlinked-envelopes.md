---
id: creative-arts.music.ableton-live.clip-envelopes-and-unlinked-envelopes
name: clip-envelopes-and-unlinked-envelopes
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, warping, clip-envelopes, unlinked-envelopes, modulation-envelopes, automation-envelopes, transposition-envelope, sample-offset, polymeter-modulation, clip-view]
level: practitioner
status: docs-checked
description: "Use Live clip envelopes: automation vs modulation, Clip controls (Transposition, Gain, Sample Offset), MIDI Ctrl envelopes and unlinked envelope loops for polymetric movement."
sources:
  - https://www.ableton.com/en/live-manual/12/clip-envelopes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clip envelopes and unlinked envelopes (Live)

**Goal:** add movement that belongs to a clip and travels with it, including envelopes of a different length than the clip.

## 1. Where they are
- Open the **Envelopes** tab in Clip View by clicking its tab header.
- Two choosers pick the envelope: the Device chooser selects a general category of controls, and the Control chooser selects among that item's controls.

## 2. Two envelope kinds
| Kind | What it does |
|---|---|
| **Automation** (red) | sets the absolute value of a control |
| **Modulation** (blue) | only influences the value already defined |
- Session clips have two toggles below the choosers (Automation and Modulation). On Arrangement clips only modulation is possible in Clip View; Arrangement automation lives in the track's automation lane.

## 3. Clip-specific controls
- Audio clips: choose **Clip** in the Device chooser, then **Transposition**, **Gain** or **Sample Offset**. Sample Offset is only available for clips in Beats Warp Mode.
- MIDI clips: choose **MIDI Ctrl** in the Device chooser and pick a controller; Live supports most controller numbers up to 119.
- Draw Mode draws steps along the grid; switch it off to edit breakpoints and segments.

## 4. Unlinked envelopes
- Linked envelopes respond to changes in the clip's Warp Markers. Unlinking gives the envelope its own local loop/region settings, with its own Loop switch separate from the clip's.
- Set the loop length in the leftmost envelope loop-length value box. Any length is allowed, including odd ones such as 3.2.1.
- The manual's examples: an eight-bar fade-out over a one-bar loop, and a filter sweep every four bars.

## Gotchas
- Forgetting a clip envelope exists: parameters will not stay put. Check the Envelopes tab.

## Verify
- Launch the clip: the envelope plays; with the envelope unlinked and a different length its pattern drifts against the clip loop.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Clip Envelopes (first 100,000 characters): Envelopes tab, Device and Control choosers, red/blue kinds, Session vs Arrangement behaviour, Transposition/Gain/Sample Offset with Beats mode condition, Linked vs unlinked, separate Loop switch and loop-length box, odd lengths, example uses, MIDI Ctrl up to 119, Draw Mode. Removed: "E" key, Detune, stacking claim, stutter and vocal-chop uses (not stated on the page).
Method: documentation only; no commands were run.
