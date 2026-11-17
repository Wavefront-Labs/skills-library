---
id: creative-arts.animation.blender.cli-argument-parsing
name: cli-argument-parsing
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-argument-parsing, double-dash, argv, argparse]
level: practitioner
status: docs-checked
description: "Pass custom arguments to Blender Python scripts after --, parse them with argparse, and avoid clashes with Blender's own flags."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://docs.python.org/3/library/argparse.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-argument-parsing

Goal: one script used for many shots, with parameters from the command line.

## Pattern

```bash
blender -b shot.blend -P render_shot.py -- --shot sh010 --samples 256 --frames 1001-1100
```
`--` ends Blender's option processing; the following arguments are passed unchanged and can be read from Python's `sys.argv`.

```python
import sys, argparse, bpy
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(prog="render_shot")
ap.add_argument("--shot", required=True)
ap.add_argument("--samples", type=int, default=128)
ap.add_argument("--frames", default=None)
args = ap.parse_args(argv)

sc = bpy.context.scene
sc.cycles.samples = args.samples
if args.frames:
    s, e = map(int, args.frames.split("-")); sc.frame_start, sc.frame_end = s, e
sc.render.filepath = f"//../render/{args.shot}/{args.shot}_####"
bpy.ops.render.render(animation=True)
```

## Rules

- Without `--`, Blender tries to parse your flags as its own (`-s` is the start frame).
- Blender arguments must be separated by white space (`-ba` is an unknown argument), and they run in the order given.
- Do the render inside the script (as above) **or** put `-a` on the command line. Never both, or the animation renders twice.
- Cycles add-on options such as `--cycles-device` also go after `--`. If your script shares that list, use `parse_known_args` so argparse ignores them.

## Gotchas

- argparse calls `sys.exit` on a bad argument or `--help`, which ends the Blender process; check the exit code in your wrapper.
- Windows quoting: avoid spaces in values, or quote them for your shell.

## Verify

Run with `--help` after `--`: the script's argparse help prints. Run with a bad value: the process ends with a non-zero code.

## Checked

2026-10-27 against the Blender 5.2 manual (Command Line Arguments page). Confirmed: `--` meaning and `sys.argv` access, `-s` as start frame, white-space separation, left-to-right argument order, Cycles options after `--`. Removed an unconfirmed claim about the exact exit code. Method: documentation only; no commands were run.
