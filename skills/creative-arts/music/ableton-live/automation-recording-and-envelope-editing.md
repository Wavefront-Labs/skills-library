---
id: creative-arts.music.ableton-live.automation-recording-and-envelope-editing
name: automation-recording-and-envelope-editing
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-automation, automation-arm, envelope-editing, automation-lanes, re-enable-automation, breakpoints, curves, arrangement-automation, lock-envelopes, draw-mode]
level: practitioner
status: docs-checked
description: "Record and edit automation in Live: Automation Arm, Arrangement recording, Automation Mode, Draw Mode, breakpoints and curves, shapes, Re-Enable Automation and Lock Envelopes."
sources:
  - https://www.ableton.com/en/live-manual/12/automation-and-editing-envelopes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation recording and envelope editing (Live)

**Goal:** record expressive automation and edit it precisely.

## 1. Recording
- Enable the Control Bar's **Automation Arm** button to prepare for automation recording (Session View).
- In the Arrangement, all control changes made while **Arrangement Record** is on become Arrangement automation.

## 2. Viewing and drawing
- Enable Automation Mode with the toggle above the track headers, or press **A**.
- The **Device** chooser and the **Automation Control** chooser select which parameter's envelope you see.
- **Draw Mode**: click the Control Bar's Draw Mode switch or press **B**. Drawing creates steps as wide as the visible grid.
- Click a breakpoint to delete it.
- Hold **Shift** while dragging a breakpoint vertically for finer resolution; hold **Alt** (Windows) / **Option** (Mac) while dragging horizontally to bypass grid snapping.
- Hold Alt/Option and drag a line segment to curve it; Alt/Option double-click returns it to a straight line.
- Right-click a time selection and choose a shape from the context menu to insert it.

## 3. Overriding and re-enabling
- When you change an automated control manually, the Control Bar's **Re-Enable Automation** button lights up; click it to restore the automation.

## 4. Lock Envelopes
- The **Lock Envelopes** switch locks envelopes to the song position rather than to the clips, so they stay in place when clips move.

## Gotchas
- Forgetting Re-Enable Automation after a manual tweak leaves the automation overridden.

## Verify
- Play back with hands off: moves happen as drawn; the Re-Enable button is not lit.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Automation and Editing Envelopes (first 100,000 characters): Automation Arm, Arrangement Record behaviour, A and B shortcuts, Device and Automation Control choosers, step width, breakpoint deletion, Shift and Alt modifiers, curving and Alt double-click, shape insertion by context menu, Re-Enable Automation, Lock Envelopes. Removed: Simplify Envelope, shape list, Session automation into clips, Show Automation button, clip-envelope comparison, automation targets, device-deletion and macro advice (not stated on the page or not read).
Method: documentation only; no commands were run.
