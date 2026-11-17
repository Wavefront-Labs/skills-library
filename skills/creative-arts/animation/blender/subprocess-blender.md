---
id: creative-arts.animation.blender.subprocess-blender
name: subprocess-blender
category: creative-arts
field: animation
product: blender
tags: [blender, pipeline, automation, subprocess-blender, external-python, command-line]
level: practitioner
status: docs-checked
description: "Drive Blender from external Python with subprocess: building the command, passing args after --, timeouts, capturing logs, exit codes and returning results as JSON."
sources:
  - https://docs.python.org/3/library/subprocess.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# subprocess-blender

Goal: call Blender as a worker from pipeline tools (publish tools, web services, CI) and get reliable results back.

## Caller

```python
import json, subprocess, tempfile, pathlib
def run_blender(blend, script, args, blender="blender", timeout=3600):
    out = pathlib.Path(tempfile.mkdtemp()) / "result.json"
    cmd = [blender, "-b", "--factory-startup", str(blend),
           "--python-exit-code", "1", "-P", str(script), "--", "--out", str(out), *args]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(f"blender failed ({p.returncode})\n{p.stdout[-4000:]}\n{p.stderr[-4000:]}")
    return json.loads(out.read_text())
```

## Script side

```python
import sys, json, argparse, bpy
argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser(); ap.add_argument("--out"); a, _ = ap.parse_known_args(argv)
result = {"objects": len(bpy.data.objects), "frames": [bpy.context.scene.frame_start, bpy.context.scene.frame_end]}
json.dump(result, open(a.out, "w"))
```

## Rules

- Return results through a file (JSON), not by parsing stdout. Blender prints its own messages to stdout.
- Always set a **timeout**. Hung renders and dialogs in add-ons happen.
- `--python-exit-code 1` sets the exit code (0-255; zero disables) used when a Python exception is raised in a script run from the command line.
- `--factory-startup` skips reading the user's `startup.blend`; `--addons a,b` (comma-separated, no spaces) enables add-ons in addition to the defaults (see `creative-arts.animation.blender.cli-factory-startup`).
- Run several in parallel with a pool, but watch RAM and GPU (practice).

## Gotchas

- Windows: pass the full path to `blender.exe`. Do not use `shell=True` with user-supplied paths.
- Decoding: pass `errors="replace"` (or capture bytes) if file names in the log might not be valid in the console encoding (practice).
- `capture_output` keeps all output in memory; redirect to a log file for long renders (practice).

## Verify

Call it on a test file: you get the JSON result. Call it with a script that raises: you get a RuntimeError with the traceback in the message.

## Checked

Blender 5.2 manual (command-line arguments) read 2026-10-27; Python subprocess behaviour per the Python standard-library docs (linked in sources).
- `-b`, `--factory-startup`, `-P`, `--python-exit-code <code>` (0-255, zero disables, scripts from the command line only), `--addons` (comma-separated, no spaces, in addition to default add-ons), and the `--` separator for script arguments: manual command-line arguments page.
- Removed as unconfirmed: the non-UTF-8 output claim and the one-render-per-GPU rule are now labelled practice.

Method: documentation only; no commands were run.
