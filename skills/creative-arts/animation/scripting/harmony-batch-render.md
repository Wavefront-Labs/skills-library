---
id: creative-arts.animation.scripting.harmony-batch-render
name: harmony-batch-render
category: creative-arts
field: animation
product: scripting
tags: [harmony-batch, harmony-scripting, toon-boom, harmony, command-line, batch-render, write-node, render-farm, headless]
level: advanced
status: draft
description: "Render Toon Boom Harmony scenes from the command line: -batch mode, write node outputs, running scripts headless, and farm-friendly frame ranges."
sources:
  - https://docs.toonboom.com/
  - https://docs.toonboom.com/help/harmony-22/scripting/script/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Harmony batch rendering

**Goal:** render Harmony scenes without opening the GUI, for overnight episode renders or farm
submission, using the scene's Write nodes.

## Command line basics (standalone scenes)

```bash
# Windows: HarmonyPremium.exe ; macOS: .../Harmony 22 Premium.app/Contents/MacOS/Harmony Premium
HarmonyPremium -batch <SCENE_DIR>/ep104_sc010.xstage
HarmonyPremium -batch -frames 1 120 <SCENE_DIR>/ep104_sc010.xstage
HarmonyPremium -batch -scene ep104_sc010.xstage -compile <SCRIPT>.js   # run a script headless (version dependent)
```
- `-batch` renders all enabled Write nodes in the scene using their own output settings (path, format,
  drawing type: PNG/TGA/EXR, movie).
- Check `HarmonyPremium -help` on the installed version; flags differ between releases and between
  standalone and database (Harmony Server) modes.

## Prepare scenes for batch

- Write node path relative to the scene (`frames/ep104_sc010-`) so renders go next to the scene, or
  an absolute show path via environment/variables.
- Image sequence formats (PNG/EXR) for farm chunking; movie outputs only in single-task renders.
- Disable preview/test Write nodes or they render too.
- Scene frame rate and resolution set correctly (Scene - Scene Settings).

## Scripted batch tasks

Harmony scripts (QtScript/JavaScript API, `.js` in scripts folders) can be run headless to set Write
node paths, toggle nodes, or export, for example:
```javascript
// set every Write node's output path prefix
var writes = node.getNodes(["WRITE"]);
for (var i = 0; i < writes.length; i++)
  node.setTextAttr(writes[i], "DRAWING_NAME", 1, "frames/" + scene.currentScene() + "_");
scene.saveAll();
```

## Farm

Wrap the command in a Deadline/OpenCue job with frame chunks (`-frames start end`), the same Harmony
version on every node, and fonts/plugins installed. Database (Harmony Server) scenes need the
batch/render queue tools tied to the database instead.

## Gotchas

- Large scenes render slowly with OpenGL preview settings; ensure render uses software/final quality as
  set in Write node and scene settings.
- Missing drawings or palettes render as red/empty; check the log output.

## Verify

Batch render a 10-frame range, compare one frame against an in-GUI render (difference blend), and confirm
frame count and file naming match the Write node settings.
