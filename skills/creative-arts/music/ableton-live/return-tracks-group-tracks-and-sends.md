---
id: creative-arts.music.ableton-live.return-tracks-group-tracks-and-sends
name: return-tracks-group-tracks-and-sends
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-routing, return-tracks, group-tracks, sends, pre-fader-send, post-fader-send, main-track, bus-processing, nested-groups, mixer-section]
level: practitioner
status: docs-checked
description: "Organise a Live mix with group tracks and return tracks: grouping and nesting, send levels, the Pre/Post toggle, return-to-return sends, and showing mixer sections."
sources:
  - https://www.ableton.com/en/live-manual/12/mixing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Return tracks, group tracks and sends (Live)

**Goal:** a tidy, efficient Live mixer with shared effects and bus processing.

## 1. Group tracks
- Select the tracks to include and run the Edit menu's **Group Tracks** command. The same command nests an existing group inside a new group.
- Members' Audio To routing is assigned to the group track automatically, so the group can hold devices for bus processing (drum bus compression, music bus EQ).
- A group track's Send control sets how much of its output feeds each return.

## 2. Return tracks and sends
- Create returns with the Create menu's **Insert Return Track** command; you can make several.
- Each Send control sets how much of that track's output feeds the matching return's input. Put fully wet effects on the return and use sends to choose how much each track feeds them.
- Show or hide return tracks with the **Return Tracks** entry in View > Mixer Controls.

## 3. Pre vs post
- Every return has a **Pre/Post** toggle that decides whether a track's send is tapped before or after the mixer stage. Pre keeps the send independent of the track fader (useful for monitor/cue mixes or reverb-only fades).

## 4. Return-to-return and feedback
- The Send controls on return tracks are disabled by default. A return's output can be routed to its own input, which creates feedback, so enable it deliberately.

## 5. Practical layout
- Groups: Drums, Bass, Music, Vocals, FX. Returns: short room, long reverb, tempo delay, parallel compression.
- Colour-code groups and name returns for the effect.

## Gotchas
- A return effect not set fully wet doubles the dry signal and can cause level or phase problems.

## Verify
- Solo a return while a track sends: you hear only the effect.
- Moving a group's fader scales the whole group.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Mixing chapter: Group Tracks command and nesting, automatic Audio To assignment, Insert Return Track, Send controls, Pre/Post toggle, return Send controls disabled by default and feedback, Return Tracks entry in View > Mixer Controls. Removed: keyboard shortcuts, default Returns A/B, Pre/Post default, return deletion behaviour, sends from group members bypassing the group, example return names (not stated on the page).
Method: documentation only; no commands were run.
