---
id: creative-arts.animation.blender.cli-render-flags
name: cli-render-flags
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, background-rendering, cli-render-flags, cli-render-animation]
level: practitioner
status: docs-checked
description: "Render from the Blender command line: -b, -a, -f with lists and ranges, -s/-e/-j, -o output paths and -F formats, and why argument order matters."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-render-flags

Goal: render stills and animations without the UI, reliably.

## Core flags

```bash
blender -b shot.blend -a                         # render the animation with the file's settings
blender -b shot.blend -f 101                     # one frame
blender -b shot.blend -f 1,12,24                 # comma separated list (no spaces)
blender -b shot.blend -f 50..60                  # range with .. separator (inclusive)
blender -b shot.blend -s 1001 -e 1100 -a         # override start/end
blender -b shot.blend -s 1 -e 100 -j 4 -a        # step forward 4 frames after each render
blender -b shot.blend -o //out/sh010_#### -F OPEN_EXR -x 1 -a
blender -b shot.blend -S ShotScene -a            # pick a scene
```
- `-b` / `--background` runs without the UI (audio is disabled by default; re-enable with `-setaudio Default` afterwards).
- `-f <frame>`: `+<frame>` is start-frame relative and `-<frame>` end-frame relative; `-s`/`-e` also support relative frames.
- `-o <path>`: `//` at the start is relative to the blend-file; `#` characters become the zero-padded frame number; without `#`, `####` is added. Path templates such as `{blend_name}` are supported.
- `-x <bool>` adds the file extension.
- `-F` format: `TGA RAWTGA JPEG IRIS PNG BMP HDR TIFF` always; `OPEN_EXR OPEN_EXR_MULTILAYER FFMPEG CINEON DPX JP2 WEBP` only if compiled in.
- `-a` renders frames from start to end (inclusive).

## Order matters

Arguments run left to right, and loading the blend-file overwrites a render output set before it:
- `blender -b f.blend -f 1 -o //out/` renders to the file's path, then sets the path.
- `blender -b -o //out/ f.blend -f 1` loses the path when the file loads.
- Right: `blender -b f.blend -o //out/ -a`.
Python scripts run with `-P` that change settings also need to come before `-a`.

## Windows

Use the full path to blender.exe or add it to PATH. Quote paths with spaces. In PowerShell, call it with `&` when the path is quoted.

## Verify

Run `blender -b shot.blend -f 1`, then check that the output file exists with the expected name. Check the log (see cli-logging-debug) and the files on disk rather than the exit code alone.

## Checked

2026-10-27 against the Blender 5.2 manual, Command Line Arguments page (Render, Format options, Argument Order). Confirmed every flag above. Removed unconfirmed claims (that `-b` must come first, exit-code behaviour, `Saved:` log line text). Method: documentation only; no commands were run.
