---
id: creative-arts.animation.blender.cli-engine-threads
name: cli-engine-threads
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-engine-override, cli-engine, cli-threads, cycles-device]
level: practitioner
status: docs-checked
description: "Override engine, threads and device from the command line: -E engine names, -t threads, --cycles-device after --, and checking which settings took effect."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-engine-threads

Goal: force engine, CPU threads and GPU backend for a render without editing the file.

## Engine

```bash
blender -b f.blend -E CYCLES -a
blender -b f.blend -E BLENDER_WORKBENCH -a
blender -b f.blend -E BLENDER_EEVEE -a
blender -b -E help                               # lists engine identifiers for this build
```
`-E help` lists the engines available in your build. The EEVEE identifier is `BLENDER_EEVEE` in Blender 5.2 (older 4.x releases used a different identifier), so always check with `-E help` on the target version.

## Threads

`-t <threads>` sets the thread count for rendering and other operations (range 1-1024; 0 uses the system's processor count). Use it on shared machines or when running several Blender processes on one node.

## Cycles device

Cycles options must be specified after a double dash:
```bash
blender -b f.blend -E CYCLES -a -- --cycles-device OPTIX
blender -b f.blend -a -- --cycles-device CUDA+CPU
blender -b f.blend -f 1 -- --cycles-print-stats
```
Valid devices: `CPU`, `CUDA`, `OPTIX`, `HIP`, `ONEAPI`, `METAL`. Append `+CPU` to a GPU device to render on both. `--cycles-print-stats` logs render memory and time usage.

## Format and output

`-F OPEN_EXR -o //out/f_####` (see cli-render-flags). Arguments run in order, so these come before `-a`.

## Gotchas

- `-E` changes the engine but not engine-specific settings stored in the file. A file prepared for EEVEE and forced to Cycles keeps whatever Cycles values it holds (samples, denoising). Set them with `--python-expr` before `-a`.
- Confirm the device actually used in the render log, and set `scene.cycles.device = 'GPU'` in a script if the file's scene device is CPU.

## Verify

The render log shows the engine and device in use. Compare render time with a known GPU run.

## Checked

2026-10-27 against the Blender 5.2 manual (Command Line Arguments) and the 5.2 Python API (RenderSettings.engine documents `BLENDER_EEVEE`) and 5.2 engine sources (`BLENDER_WORKBENCH`, `BLENDER_EEVEE` ids). Confirmed: `-E`, `-t` range, `--cycles-device` values and `+CPU`, `--cycles-print-stats`. Removed unconfirmed claims (4096 default sample note, scene-device behaviour of `--cycles-device`, device side effects). Method: documentation only; no commands were run.
