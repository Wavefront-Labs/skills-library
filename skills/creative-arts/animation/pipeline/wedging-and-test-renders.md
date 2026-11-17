---
id: creative-arts.animation.pipeline.wedging-and-test-renders
name: wedging-and-test-renders
category: creative-arts
field: animation
product: pipeline
tags: [wedging, wedge, test-renders, render-tests, sampling-tests, noise, parameter-sweep]
level: practitioner
status: draft
description: "Use wedges and test renders to choose settings: parameter sweeps, test frames and regions, sample and noise comparisons, recording results and cost per quality."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Wedging and test renders

A **wedge** is a set of renders of the same frame with one parameter changed across the set, so you can compare and choose by eye and by cost.

## Choose test frames
- **Representative**: one simple, one average and one worst-case frame (heavy volumes, glass, hair, motion blur, many lights).
- Include a frame with **fine detail** and one with **flat areas** where noise shows.
- Use **crop/region** renders on the problem area to test quickly at full resolution, and half-resolution renders for composition and lighting.

## What to wedge
- **Samples** (or noise threshold): find the lowest setting that looks clean after denoising.
- **Light intensity, exposure and colour** for look decisions.
- **Ray depth, bounces, volume settings** to see where extra cost stops changing the image.
- **Denoiser** settings or on/off.
- **Resolution and filter** for edge quality.
- Material parameters (roughness, subsurface) for look development.

## Run them
1. Change **one variable at a time**; keep a baseline.
2. Use a script or the DCC's tool: Houdini has wedging nodes (the Wedge TOP and ROP wedge features); in Blender or Maya use a small script to loop values or use render layers; farm managers can submit one job per wedge.
3. Name outputs by parameter value (`noise_0.05_samples_256.exr`), so the sheet is self-documenting.
4. Record **render time and memory** for every wedge.

## Evaluate
- Arrange results in a contact sheet with labels, and compare at 100% zoom.
- Use difference images against the highest-quality reference to see where changes concentrate.
- Compute **cost per quality**: choose the setting where the next step costs a lot but changes little.

## Apply
- Put the chosen settings in a render preset (`render-preflight.md`), and note the reason with the wedge sheet.
- Re-test when scene complexity or the renderer version changes.

## Verify
- [ ] A baseline and a reference render exist.
- [ ] Times and memory are recorded per wedge.
- [ ] The chosen settings are saved as a preset with notes.
