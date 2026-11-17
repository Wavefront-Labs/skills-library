---
id: creative-arts.music.ableton-live.sidechain-routing-in-live
name: sidechain-routing-in-live
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-routing, live-sidechain, sidechain-compression, ducking, compressor-sidechain, gate-sidechain, ghost-kick, auto-filter-sidechain, pumping, envelope-follower]
level: practitioner
status: docs-checked
description: "Set up sidechain in Live: Compressor sidechain section and sidechain EQ, Auto Filter external sidechain with tapping point, and how Gain and Dry/Wet behave."
sources:
  - https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidechain routing in Live

**Goal:** duck or trigger one sound from another for pumping, clarity or rhythmic gating.

## 1. Compressor sidechain
1. Put **Compressor** on the track to be ducked.
2. Unfold the Compressor with the toggle in its title bar. The left section holds the
   external controls, the right section the sidechain EQ.
3. Enable the **Sidechain** button, then choose the source from the choosers; the selected
   source acts as the compressor's trigger.
- **Gain** sets the level of the external input; raising it does not make the source louder
  in the mix, and the sidechain signal is never heard directly.
- **Dry/Wet** blends sidechain and original signal for triggering; 100% uses only the sidechain.
- The **sidechain EQ** limits triggering to a frequency band; the headphones button between
  the sections lets you hear only the sidechain input.
- Automatic Makeup is unavailable with an external sidechain.

## 2. Auto Filter sidechain
- Open the Sidechain Section with the toggle in the upper-left corner. Enable **External**,
  pick the External Source, and choose the External Tapping Point (Pre FX, Post FX or
  Post Mixer).
- **Mix** blends external and internal triggering; at 100% only the external source triggers
  the envelope follower. SC Gain sets the input level; Sidechain Listen lets you hear it.
- The SC Filter toggle enables a separate filter for the sidechain; the sidechain is mono by
  default (context-menu option).

## 3. Other sidechains
Corpus and Auto Shift use MIDI from another track as their sidechain rather than audio.
Check each device's page in the manual for its own sidechain controls.

## Verify
- Watch the Compressor's gain-reduction meter: it dips when the source plays.
- Use sidechain listen to confirm the trigger signal is what you intend.

## Checked
2026-11-01. Confirmed in the Live 12 Audio Effect Reference: Compressor sidechain section, Gain, Dry/Wet, sidechain EQ, listen button, Automatic Makeup; Auto Filter External, tapping points, Mix, SC Gain, SC Filter, mono default; Corpus and Auto Shift MIDI sidechain. Removed: ratio, attack, release, threshold and frequency settings, the ghost-kick technique, Gate and other-device sidechain claims, Pre/Post FX tap claims for Compressor, and gotchas (not stated on the page).
Method: documentation only; no commands were run.
