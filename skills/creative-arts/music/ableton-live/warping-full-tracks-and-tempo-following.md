---
id: creative-arts.music.ableton-live.warping-full-tracks-and-tempo-following
name: warping-full-tracks-and-tempo-following
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, warping, warp-markers, warping-full-tracks, tempo-follower, set-1-1-1-here, warp-from-here, auto-warp, follow-tempo, live-band-sync]
level: practitioner
status: docs-checked
description: "Warp whole songs in Live: Set 1.1.1 Here, the Warp From Here variants, manual warp markers, Auto-Warp Long Samples, and Tempo Follower for following an incoming audio signal."
sources:
  - https://www.ableton.com/en/live-manual/12/audio-clips-tempo-and-warping/
  - https://www.ableton.com/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warping full tracks and tempo following (Live)

**Goal:** a full-length recording locked to Live's grid, and Live following an incoming tempo.

## 1. Warping a full song
1. Turn the clip's **Warp** switch on. Complex Pro may give higher quality than Complex; Beats mode suits audio with a dominant rhythm such as drum loops and most electronic dance music.
2. Move the insert marker to the downbeat and use the context menu's **Set 1.1.1 Here** command to move the start marker there.
3. Right-click a Warp Marker for the **Warp From Here** variants:
   - **Warp From Here** runs Auto-Warp to the right of the selected marker.
   - **Warp From Here (Start At ...)** uses the Set's tempo as the baseline.
   - **Warp From Here (Straight)** works best for samples without tempo variations.
   - **Warp ... BPM From Here** sets a single Warp Marker, assuming the clip has the Set's tempo.
4. Double-click in the upper half of the Sample Editor to add a Warp Marker at that location, then fix drift by hand.
- The **Auto-Warp Long Samples** preference decides whether long samples are warped when loaded; it is enabled by default.

## 2. Tempo automation
- Tempo automation is visible in the Main track but not editable until you use the Unfollow Tempo Automation option.

## 3. Tempo Follower
- It analyses an incoming audio signal in real time and interprets its tempo. Use it when Link or MIDI Clock is not available or you want a less rigid clock.
- In the Tempo & MIDI Settings, under Tempo Follower, set the Input Channel (Ext. In) to the interface input with your source. Turn it on with the **Follow** button; the **Show Tempo Follower Toggle** option reveals the Control Bar button, and Tempo Follower does not run while that button is hidden.
- The manual suggests a drum kit (with a dedicated overhead mic) or turntables, and says the algorithm is optimised for signals with a clear rhythm.
- It is mutually exclusive with External Sync. Live can still send MIDI clock but cannot receive it. If the input cannot be reached, Follow is greyed out.

## Gotchas
- A downbeat set on a pickup note puts everything a beat off.

## Verify
- With the metronome on, the song's downbeats align with the bar lines throughout.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Audio Clips, Tempo and Warping (first 100,000 characters) and Synchronizing with Link, Tempo Follower and MIDI (first 100,000 characters): Set 1.1.1 Here, Warp From Here variants, double-click marker creation, Auto-Warp Long Samples default, mode descriptions, tempo automation note, Tempo Follower description, Input Channel, Follow, toggle, sources, limitations. Removed: step-by-step drift workflow, Live 11+ tag, smoothing claim, Preferences menu path, tempo-automation-as-grid technique (not stated on the pages).
Method: documentation only; no commands were run.
