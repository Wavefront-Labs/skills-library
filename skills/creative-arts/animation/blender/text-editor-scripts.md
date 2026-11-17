---
id: creative-arts.animation.blender.text-editor-scripts
name: text-editor-scripts
category: creative-arts
field: animation
product: blender
tags: [blender, text-editor-scripts, run-script, text-editor-run, text-editor, script-reload, register-text, templates]
level: intro
status: docs-checked
description: "Run and iterate scripts in Blender's Text Editor: Run Script, reload from disk, external editing, Register auto-run on load, templates, and Reload Scripts for add-ons."
sources:
  - https://docs.blender.org/manual/en/latest/editors/text_editor.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
  - https://docs.blender.org/api/current/info_tips_and_tricks.html
  - https://docs.blender.org/manual/en/latest/advanced/scripting/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-editor-scripts

Goal: a fast edit-run loop for one-off and in-file scripts without installing an add-on.

## Run

- Text Editor header *Run Script* (play icon) or `Alt P` executes the text as a Python script.
- If a script fails, check the Console window for the traceback (see the Console window tip in the manual's add-on pages).
- The *Templates* menu contains templates for Python and Open Shading Language scripts; use the Python ones as starting points.

## Edit externally, reload

- *Text → Open* (`Alt O`) a `.py` from disk and edit it in an external editor. When the file is modified by another program, *Resolve Conflict* offers *Reload from Disk*, *Make Text Internal* and *Ignore*; *Text → Reload* (`Alt R`) reopens the current buffer (unsaved changes are lost).
- To skip the reload click, keep a tiny runner text inside the .blend that executes the external file:

```python
import bpy, pathlib
path = pathlib.Path(bpy.path.abspath("//scripts/build_scene.py"))
exec(compile(path.read_text(), str(path), "exec"), {"__name__": "__main__"})
```

## Register (auto-run on file load)

- The text block's *Register* option runs it as a Python script when the blend-file loads.
- It only runs if *Preferences → Save & Load → Auto Run Python Scripts* is on, or you choose *Allow Execution* in the auto-run warning. `blender --enable-autoexec` (`-y`) enables it on the command line.

## Reload Scripts (add-ons and startup modules)

`F3` → *Reload Scripts* (`bpy.ops.script.reload()`) re-imports add-ons and `scripts/startup`. It does not reload a module your add-on imported unless the add-on reloads it itself (`importlib.reload(submodule)` in `__init__` guarded by `if "bpy" in locals()`).

## Gotchas

- Text blocks are data-blocks: an internal script travels with the .blend; an external one is only a path (keep it `//relative`).
- `exec` of an external file keeps module-level state between runs only if you reuse the globals dict; pass a fresh dict for a clean run.
- Running a script that registers the same classes again can fail; unregister first (for example in a `try` block) before re-running (practice).

## Verify

Edit the external file, press `Alt R` then `Alt P` and see the new behaviour; reopen the .blend with Auto Run off and confirm the auto-run warning appears for a registered script.

## Checked

Blender 5.2 manual (blender-v5.2-release), read 2026-10-27.
- Run Script (Alt-P), Open (Alt-O), Reload (Alt-R), Resolve Conflict options, Register option, Templates menu: editors/text_editor page. Auto Run Python Scripts and the Allow Execution / Ignore dialog: save_load and scripting security pages; `-y/--enable-autoexec`: command-line arguments. `bpy.ops.script.reload`: API 5.2.
- Removed as unconfirmed: `__name__ == "__main__"` behaviour, the status-bar report and system-console route, specific template names, the `.py` name requirement for Register and the Rigify example.

Method: documentation only; no commands were run.
