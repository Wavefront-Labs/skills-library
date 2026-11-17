---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-ui-depth-size
name: xr-ui-depth-size
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-ui-ux-world-space, xr-ui-depth-size]
level: practitioner
status: draft
description: "Put UI at a comfortable distance with legible text."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Place and size world-space UI
**Goal:** Put UI at a comfortable distance with legible text.

- Place panels roughly 1 to 2 metres away, within a comfortable gaze angle, and keep text large (size in degrees of visual angle rather than pixels; check the vendor guideline for the minimum).
- Prefer composition layers for text if the platform provides them (see OpenXR layers).
- Avoid head-locked HUDs; use world-anchored or lazy-follow panels.

## Gotchas
- Head-locked UI close to the face causes eye strain.

## Self-check
Smallest text is readable by a tester at the target distance.
