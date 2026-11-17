---
id: creative-arts.animation.blender.render-stats-benchmark
name: render-stats-benchmark
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, render-benchmark, render-stats, benchmark, profiling]
level: practitioner
status: docs-checked
description: "Measure render cost properly: metadata stamps for render time and memory, Cycles --cycles-print-stats, one-change-at-a-time A/B tests, Persistent Data and the Blender Benchmark."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/metadata.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://opendata.blender.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# render-stats-benchmark

Goal: know what costs time and memory before optimising. The method is practice; the tool names below are from the manual.

## Where the numbers are

- Output Properties > **Metadata**: the Include options add **Render Time**, **Memory** (peak memory use), Frame, Frame Range and more to the image metadata (only formats that support metadata store them); **Burn into Image** also draws them as text.
- Command line: `blender -b shot.blend -f 10 -- --cycles-print-stats` logs statistics about render memory and time usage (Cycles argument, after the `--`).
- `--debug-cycles` enables debug messages from Cycles.

## Method

1. Pick 2 to 3 representative frames (busiest, typical, simplest).
2. Render a baseline, then change **one** thing at a time (bounces, samples, a heavy object hidden, texture size, subdivision, volume settings). Record time and peak memory in a table.
3. Separate scene preparation (sync, BVH build) from path tracing and from denoise or compositing, so you know which stage to attack.
4. **Persistent Data** (Render Properties > Performance > Final Render) keeps render data in memory for faster re-renders and animation renders at the cost of memory; with several view layers only one view layer's data is kept. Measure the second frame, not the first.

## Hardware comparison

The Blender Benchmark (results at opendata.blender.org) collects and shares results for standard scenes. Use it to compare hardware, not to tune a shot.

## Gotchas

- First renders include kernel loading and shader compilation (practice); discard them.
- Viewport render time is not the same as F12 time. Measure F12.
- Laptops can throttle under load; benchmark on a stable power and cooling setup (practice).

## Verify

Your table should account for most of the frame time with named causes. Optimise the biggest one first.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): advanced/command_line/arguments.rst (`--cycles-print-stats`, `--debug-cycles`), render/output/properties/metadata.rst (Render Time, Memory, Burn into Image), render/cycles/render_settings/performance.rst (Persistent Data). Removed: render window header field list, Image Editor sidebar claim, samples-per-minute detail, the 20 percent throttling figure and the 80 percent rule. Method: documentation only; no commands were run.
