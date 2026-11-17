---
id: creative-arts.music.ableton-live.arrangement-editing-locators-and-time-commands
name: arrangement-editing-locators-and-time-commands
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, arrangement-view, arrangement-editing, locators, insert-silence, delete-time, duplicate-time, paste-time, split, consolidate, loop-selection, grid]
level: practitioner
status: docs-checked
description: "Edit songs in Live's Arrangement View: locators, time commands (delete, duplicate, insert silence, paste time), split, consolidate, loop selection, grid shortcuts and zoom."
sources:
  - https://www.ableton.com/en/live-manual/12/arrangement-view/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrangement editing, locators and time commands (Live)

**Goal:** restructure a song fast in the Arrangement View without misaligning tracks.

## 1. Locators
- The **Set Locator** button adds locators during playback or recording. Add Locator is also in the scrub area's context menu and the Create menu.
- Rename with the Edit menu's Rename command (Ctrl+R on Windows, Cmd+R on Mac).
- Jump by clicking a locator or with the Previous and Next Locator buttons. Delete with the Delete key, the Create menu's Delete Locator, or the Delete Locator button.

## 2. Time commands
- **Delete Time**: deletes the selected time across all tracks.
- **Duplicate Time**: places a copy of the selected timespan into the Arrangement.
- **Insert Silence**: inserts a chosen amount of empty time at the insert marker.
- **Paste Time**: lengthens the Arrangement by the length of the copied material.
- The page lists no shortcuts for these; use the Edit menu.

## 3. Clip editing
- **Split**: Ctrl+E / Cmd+E, or the Split context menu option.
- **Consolidate**: Ctrl+J / Cmd+J, the Edit menu, or the context menu.
- **Grid**: Ctrl/Cmd+1 narrows, Ctrl/Cmd+2 widens, Ctrl/Cmd+5 toggles fixed and adaptive grid, Ctrl/Cmd+4 turns snapping on or off.
- Shift+click extends a selection; Shift with the arrow keys extends or shortens it.

## 4. Loop and view
- The **Arrangement Loop** toggle is in the Control Bar. **Loop Selection** (Edit menu, Ctrl+L / Cmd+L) loops the selected clip or time.
- Zoom with + and -, or Ctrl/Cmd with the mouse wheel; Z zooms to the time selection and X reverts the zoom.
- The **Follow** switch in the Control Bar scrolls the view with playback.

## Gotchas
- Time commands act on the selected time across all tracks.
- Set selections on bar lines so Duplicate Time stays musical.

## Verify
- After restructuring, play across each edit point: no cut-off notes or missing automation.
- Locators match the new structure.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Arrangement View: locator commands and rename shortcut, time command names and descriptions, Split, Consolidate, grid shortcuts, Shift selection, Arrangement Loop, Loop Selection, zoom keys, Follow. Removed: time command shortcuts, Cut Time, Duplicate clip shortcut, triplet grid shortcut, snap bypass modifier, fade and crossfade preferences, automation-follows-time claim, warp-baking claim (not stated on the page or not read).
Method: documentation only; no commands were run.
