---
id: creative-arts.animation.scripting.harmony-qtscript-scene-scripting
name: harmony-qtscript-scene-scripting
category: creative-arts
field: animation
product: scripting
tags: [harmony-qtscript, qtscript, toon-boom-harmony, scene-scripting, node-api, automation, scripting]
level: advanced
status: draft
description: "Script Toon Boom Harmony scenes with its Qt Script (JavaScript) API: node, column, frame and scene objects, undo grouping, logging, shelf scripts and safe testing."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Harmony QtScript scene scripting

Harmony embeds a Qt Script (ECMAScript) engine that exposes the scene through global objects: `scene`, `node`, `column`, `frame`, `Action`, `MessageLog` and others. The Harmony scripting reference documents the full API for your version.

## Running scripts
- Open the **Script Editor** window (Windows menu in current versions), write or load a script, and run a function.
- Install scripts into Harmony's user scripts folder and add them to a toolbar as buttons; the documentation lists the folder per OS and version.
- Scripts can also be run in batch or command-line mode for pipelines (`harmony-batch-render.md`).

## Patterns
```javascript
function renameReads() {
  scene.beginUndoRedoAccum("Rename reads");   // one undo step
  var reads = node.getNodes(["READ"]);
  for (var i = 0; i < reads.length; i++) {
    MessageLog.trace(node.getName(reads[i]));
  }
  scene.endUndoRedoAccum();
}
```
- `node.getNodes(["READ"])` lists node paths by type; `node.getName`, `node.type`, `node.parentNode`.
- `node.add(parent, name, type, x, y, z)` creates nodes; `node.link(srcNode, srcPort, dstNode, dstPort)` connects them.
- `node.getAttr`, `node.setTextAttr(node, attrName, frame, value)` read and write attributes; `column.*` and `frame.*` give timing and scene length.
- `MessageLog.trace()` prints to the Message Log; use it instead of dialogs.

## Safe practice
1. Wrap changes in `beginUndoRedoAccum` and `endUndoRedoAccum` so a user can undo.
2. Test on a copy of the scene; scripts can alter hundreds of nodes.
3. Use naming conventions so selection by name works (`harmony-node-view-for-cut-out-rigs.md`).
4. Keep helper functions in a shared include file where the engine supports includes, with version control.

## Gotchas
- API functions differ by version; read the reference for the Harmony version used.
- Script errors appear in the Message Log, not as pop-ups.

## Verify
- [ ] Script runs on a copy and the result is correct.
- [ ] A single undo reverts the whole script's changes.
