---
id: creative-arts.animation.blender.cli-logging-debug
name: cli-logging-debug
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-logging, cli-debug, debug-flags, troubleshooting]
level: practitioner
status: docs-checked
description: "Get useful logs from headless Blender: --log categories and named levels, --log-file, debug flags for Python, GPU, depsgraph and Cycles, and detecting failed frames."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#logging-options
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#debug-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-logging-debug

Goal: find out why a farm or background render failed.

## Logging

```bash
blender -b f.blend --log "*" --log-level info --log-file render.log -a
blender -b f.blend --log "render,cycles" --log-level debug -a
blender --log-list-categories
```
- `--log <match>`: enable logging categories, one comma-separated argument. `"*"` is everything, `"event"` every category starting with `event`, `"*mesh*"` every category containing `mesh`, and `^prefix` excludes (`"*,^operator"`).
- `--log-level <level>`: a name, one of `fatal`, `error`, `warning`, `info`, `debug`, `trace` (not a number).
- `--log-file <filepath>`: write the log to a file. Also `--log-show-memory`, `--log-show-source`, and `--log-show-backtrace` (debug builds only).
- `--log-list-categories` lists the categories available to `--log` and exits.
- Settings come first in the argument list; the render (`-a`) runs where it appears.

## Debug flags

- `--debug` (`-d`): memory error detection, no mouse grab, keeps Python's `sys.stdin`.
- `--debug-python`: Python debug messages.
- `--debug-depsgraph` (also `-eval`, `-build`, `-tag`, `-time`, `-no-threads`): dependency graph messages (drivers, slow updates).
- `--debug-gpu`: GPU debug context and information (OpenGL 4.3+).
- `--debug-cycles`: Cycles debug messages. `--debug-ffmpeg`, `--debug-freestyle` and `--debug-io` exist for those subsystems.
- `--debug-memory`: fully guarded memory allocation and debugging.
- `--debug-exit-on-error`: exit immediately when internal errors are detected.
- `--debug-all`: all debug messages. `-q` / `--quiet` suppresses status printing (warnings and errors still print).

## Detecting failures

- Judge a job by the output files on disk and by the log, not only the exit code.
- Missing textures or linked libraries produce warnings, not failures, so a frame can render and look wrong. Check image and library paths in a pre-render script (`bpy.data.images`, `bpy.data.libraries`).
- `--python-exit-code <0-255>` makes an uncaught Python exception in a command-line script return that exit code; use it with validation scripts so failed checks fail the job.

## Verify

Run a failing case on purpose (rename a texture). The log should show the missing file, and your farm wrapper should flag the job.

## Checked

2026-10-27 against the Blender 5.2 manual, Command Line Arguments page (Logging and Debug options). Corrected: `--log-level` takes names (fatal..trace), not numbers; `--debug-memory` description; `--debug-gpu` scope. Removed unconfirmed claims (exact success-line text, crash-log file names and locations, the File menu path for missing files). Method: documentation only; no commands were run.
