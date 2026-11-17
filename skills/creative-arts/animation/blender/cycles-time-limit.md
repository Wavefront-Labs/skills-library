---
id: creative-arts.animation.blender.cycles-time-limit
name: cycles-time-limit
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, time-limit, render-time-limit, samples]
level: practitioner
status: verified
description: "Use the Cycles sampling Time Limit to cap per-frame render time: what it counts, interaction with max samples, preview use, and why it is risky for animation."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# cycles-time-limit

Goal: cap how long each frame samples, for previews, deadline-driven stills and farm budgets.

## Setting

Render Properties > Sampling > Render > **Time Limit** (Python: `scene.cycles.time_limit`). It stops rendering when the time exceeds the limit, even if the desired sample count has not been reached. 0 disables the limit and is the default (float, minimum 0). Measured (Cycles CPU, Blender 4.5.14, 96x96, 200000 samples, adaptive sampling off): a 3 s limit stopped the render after 3.09 s; with limit 0 and 4 samples it finished at once. The limit does not include pre-render processing time, only render time.

## When to use it

- Look development or client previews: a fixed budget gives a steady turnaround however heavy the shot is.
- Stills on a deadline: set Max Samples high and let the time limit be the budget, then denoise.
- Farm safety cap: catches a shot left at extreme settings.

## Why it is risky for animation

The number of samples reached in a fixed time depends on the machine, so frames can end at different sample counts and noise levels, which can show as flicker, especially on a mixed farm. For finals control quality with Noise Threshold and Max Samples (see cycles-noise-threshold), and use the time limit only as a generous safety cap.

## Gotchas

- Denoising a time-limited render can hide the variation in stills, but check frames in sequence.
- If a frame stops on time with far fewer samples than planned, the shot needs optimisation more than a longer limit.

## Verify

Render two frames on the target machine and compare render time, samples reached and noise side by side.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual, Cycles Sampling. Confirmed: Time Limit stops rendering at the limit, 0 disables it, pre-render processing excluded. Removed unconfirmed: statement that denoising and BVH build are extra, the 3x safety multiple, example budgets, stats-line format.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `scene.cycles.time_limit` exists, default 0.0, UI label Time Limit in the Sampling panel source; timed renders as above. Unrun (documentation only): that pre-render processing is excluded, and the flicker/farm remarks.

Method: manual text confirmed from documentation; time limit run headless in Blender 4.5.14.
