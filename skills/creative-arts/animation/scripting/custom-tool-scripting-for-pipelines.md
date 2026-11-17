---
id: creative-arts.animation.scripting.custom-tool-scripting-for-pipelines
name: custom-tool-scripting-for-pipelines
category: creative-arts
field: animation
product: scripting
tags: [pyside, pyqt, gui, shelf-tool, maya, blender, cli, pipeline-tool, artist-facing, publish, qt-designer, docking, error-handling, usability]
level: practitioner
status: draft
description: "Building custom pipeline tools (PySide/PyQt GUIs, Maya/Blender shelf tools, CLI utilities) that wrap studio workflows for non-technical artists."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom tool scripting for pipelines

**What it is:** building the clickable/runnable tools that put a pipeline
script in front of someone who won't open a Python console — a shelf button
in Maya/Blender, a standalone PySide window, or a CLI with a clear
`--help`. This is the *delivery layer*: it wraps the logic from
`python-scripting-for-rigging-automation` or `batch-render-scripting-and-farm-submission`
(or any other script) in an interface an artist or coordinator can run
without reading the source. Distinct from those skills — this one owns the
UI/CLI shell and error surfacing, never the underlying technique.

Verified against Maya's `PySide2`/`PySide6` (version depends on Maya
release — 2022 and earlier ship PySide2, 2025+ ships PySide6) and Blender's
native `bpy.types.Operator` + `bpy.types.Panel` UI system, which is NOT Qt
and doesn't share this skill's Qt-specific snippets (noted separately
below).

## 1. Parent Qt tools to the host app, or they vanish behind it
```python
from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

def maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)

class RigBuilderUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)
        self.setWindowTitle("Rig Builder")
```
Without a parent, your window has no `Z`-order relationship to Maya's main
window — alt-tabbing or clicking into the viewport buries it, and artists
report "the tool disappeared" (it didn't; it's behind the app). `shiboken2`
(or `shiboken6` for PySide6) is what converts Maya's raw Qt pointer into a
usable Python widget — the wrap step is mandatory, you cannot construct the
main window object yourself.

## 2. Never block the UI thread with the actual work
```python
def on_build_clicked(self):
    self.build_btn.setEnabled(False)
    self.status.setText("Building...")
    QtWidgets.QApplication.processEvents()   # cheap/crude: flush paint events
    try:
        build_rig(self.get_params())
        self.status.setText("Done.")
    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "Build failed", str(e))
    finally:
        self.build_btn.setEnabled(True)
```
- For anything longer than ~a second, `processEvents()` is a crude patch,
  not a real fix — the UI is still technically frozen between calls. A
  proper fix runs the work on a `QThread`/worker and signals back; this is
  the honest minimum for a quick tool, upgrade when a build takes long
  enough that artists start force-closing it (unverified exact threshold —
  judge by complaint, not a fixed number).
- **Always wrap the call to the underlying pipeline script in try/except and
  show the real exception text in the UI.** A tool that just says "something
  went wrong" with no detail generates a support ping every single failure;
  one that shows the Python traceback (or at least `str(e)`) lets the artist
  self-diagnose a bad file path or missing asset.

## 3. Validate inputs before calling the pipeline function, not after
```python
def get_params(self):
    path = self.path_field.text().strip()
    if not path or not os.path.exists(path):
        raise ValueError(f"Scene file not found: {path!r}")
    return {"scene": path, "chunk": self.chunk_spin.value()}
```
Fail fast in the UI layer with a message naming the exact field that's
wrong (`"Scene file not found: ..."`) rather than letting a bad empty string
travel into the pipeline function and surface as a cryptic stack trace three
calls deep. The UI's whole job is to turn "artist fat-fingered a field" into
a one-line, fixable message instead of a Python exception.

## 4. A CLI version costs little extra and unlocks automation
Build the actual work as a plain function first; the GUI and CLI both call
it — never duplicate logic between them:
```python
import argparse
def main():
    p = argparse.ArgumentParser(description="Build rig from a guide file")
    p.add_argument("guide_json")
    p.add_argument("--chunk", type=int, default=10)
    args = p.parse_args()
    build_rig(json.load(open(args.guide_json)), chunk=args.chunk)
if __name__ == "__main__":
    main()
```
A CLI entry point means the exact same tool a rigger clicks can also run
headless in CI or a farm pre-job hook — the GUI becomes optional sugar, not
the only way in.

## 5. Maya shelf buttons vs. Blender panels — different installation model
- **Maya shelf button**: a shelf `.mel`/Python command string that typically
  just imports your tool module and calls `show()` — keep that string to one
  line (`import mytool; mytool.show()`) and do all real logic inside the
  importable module, never pasted directly into the shelf button itself
  (unrecoverable if the shelf file corrupts, and un-diff-able).
- **Blender**: tools are `bpy.types.Operator` subclasses registered via
  `bpy.utils.register_class`, invoked from a `bpy.types.Panel` drawn in the
  N-panel/properties editor — there is no separate Qt window needed for
  simple tools; Blender's own layout system (`layout.prop`, `layout.operator`)
  replaces PySide widgets entirely. Don't try to embed PySide inside
  Blender's UI — it's a separate windowing system and fighting it is not
  worth it for a simple tool (a standalone PySide *companion* app that
  shells out to `blender -b --python` is fine; an embedded Qt panel inside
  Blender's own UI is not the supported path).

## 6. HARD-WON GOTCHAS
- **A tool left open across a Maya file-new/file-open can hold stale
  references** to nodes from the previous scene — guard callbacks with
  `cmds.objExists()` before acting on a cached name, or close/refresh the
  tool on scene-change callbacks (`OpenMaya.MSceneMessage`).
- **Re-running a tool's module via `import` during development does NOT
  reload changed code** — Python caches the module. Use
  `importlib.reload(mytool)` (or close/reopen the window after each save)
  while iterating, or you'll debug a "fix" that was never actually loaded.
- **PySide2 vs PySide6 API drift** (e.g. `exec_()` vs `exec()`,
  `QRegExp` vs `QRegularExpression`) breaks a tool silently moved between
  Maya versions — pin to whichever the target Maya ships and don't assume
  forward/backward compatibility (unverified which exact version introduced
  which break; treat every cross-version port as needing a smoke test).

## Verify
- [ ] Tool window stays in front of the host app through normal
      clicking/alt-tabbing (correct parenting).
- [ ] A deliberately bad input (missing file, empty field) shows a specific,
      actionable message — not a raw traceback or silent no-op.
- [ ] The same underlying function is callable from both the GUI and a CLI
      entry point with identical results.
- [ ] Closing and reopening the tool after editing its source picks up the
      change (reload tested), so dev iteration isn't debugging stale code.
- [ ] Tool survives a scene file-new/open without holding a stale reference
      that throws on next use.

See also: `python-scripting-for-rigging-automation`,
`batch-render-scripting-and-farm-submission` (two scripts this skill is
commonly used to wrap), `scripting-basics` (the headless scripting this
sits on top of).
