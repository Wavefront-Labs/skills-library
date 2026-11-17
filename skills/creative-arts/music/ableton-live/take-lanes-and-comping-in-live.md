---
id: creative-arts.music.ableton-live.take-lanes-and-comping-in-live
name: take-lanes-and-comping-in-live
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, arrangement-view, take-lanes, comping, loop-recording, audition, show-take-lanes, comp-lane, vocal-comping, midi-comping]
level: practitioner
status: docs-checked
description: "Comp takes in Live 12 with take lanes: record passes into lanes, show and audition lanes, copy selections to the main lane, swap takes, set crossfades, rename and delete lanes."
sources: ["https://www.ableton.com/en/live-manual/12/comping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Take lanes and comping in Live

**Goal:** build the best composite performance from multiple takes inside Live.

## 1. Record takes
- Recording over existing clips, including with a loop, adds a new take lane for each pass. Existing lanes are reused when no other clip exists after the punch-in point.
- Armed audio and MIDI tracks get take lanes when recording; MIDI files can be dragged onto take lanes.

## 2. Show and audition
- Use **Show Take Lanes** in the track header context menu, the Show/Hide Take Lanes toggle on the track, or Ctrl+Alt+U (Win) / Cmd+Option+U (Mac).
- Audition a lane with the speaker button in its header or the T key. Only one lane per track can be auditioned at a time.

## 3. Comp
- Select material in a take lane and press Enter to copy it to the main lane.
- Hold Ctrl (Win) / Cmd (Mac) and press Up or Down to replace the main-lane clips with the next or previous take.
- The "Create Fades on Clip Edges" option in Record, Warp & Launch Settings creates 4 ms crossfades for adjacent clips. For manual crossfades, select several clips and press Ctrl+Alt+F (Win) / Cmd+Option+F (Mac).

## 4. Tidy
- Rename a lane via the Edit menu, its context menu, or Ctrl+R / Cmd+R; Tab and Shift+Tab move between lanes.
- Delete All Unused Take Lanes removes lanes holding no material used in the comp; Delete All Take Lanes removes every lane.
- Insert a lane with Shift+Alt+T (Win) / Shift+Option+T (Mac); duplicate with Ctrl+D / Cmd+D.

## Verify
- Play the main lane: seamless performance, no clicks at boundaries.
- Lane names document your comp decisions so you can revisit them.

## Checked
2026-11-01. Confirmed against the Live 12 manual Comping chapter (the arrangement-view page only links to it): lane creation per pass, show/audition/Enter/Ctrl-Cmd+arrows shortcuts, 4 ms edge fades, rename/delete/insert/duplicate commands. Removed: the "Live 11+" claim, lane ordering, Draw Mode shortcut, consolidate step and the gotchas, none of which the page states. The last 3337 characters of the page were not read.
Method: documentation only; no commands were run.
