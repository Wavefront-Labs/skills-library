---
id: computing-software.rpa-and-low-code.uipath.uipath-if-switch-loops
name: uipath-if-switch-loops
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-control-flow, uipath-if-switch-loops]
level: practitioner
status: draft
description: "Control logic with If, Switch, For Each and While."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use If, Switch and loops
**Goal:** Control logic with If, Switch, For Each and While.

- For Each Row in Data Table, For Each File in Folder and Do While cover most loops.
- Use Break and Continue for control; prefer a Switch for multiple conditions.
- Avoid deep nesting by calling child workflows.

## Gotchas
- Infinite loops in unattended bots hold the robot; add exit conditions and timeouts.

## Self-check
Loop logs show each iteration.
