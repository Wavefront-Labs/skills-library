---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-comfort-locomotion
name: xr-comfort-locomotion
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-comfort-design, xr-comfort-locomotion]
level: practitioner
status: draft
description: "Choose locomotion methods that limit vection and offer options."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design comfortable locomotion
**Goal:** Choose locomotion methods that limit vection and offer options.

- Prefer teleport or snap turn by default; offer smooth locomotion as an opt-in with speed and vignette options.
- Never move or rotate the camera without user input; avoid acceleration, bobbing and camera shake.
- Keep a stable reference frame such as a cockpit or nose cue for vehicle motion.

## Gotchas
- Comfort tolerance varies by person; expose settings rather than one fixed choice.

## Self-check
A playtest group on the shortest and the longest session reports no more than mild discomfort.
