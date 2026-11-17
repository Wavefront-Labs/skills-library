---
id: creative-arts.animation.scripting.ae-batch-replace-footage
name: ae-batch-replace-footage
category: creative-arts
field: animation
product: scripting
tags: [batch-replace-footage, ae-scripting, extendscript, after-effects, version-up, replace-with-sequence, comp-versioning, footage-relink, render-queue-scripting]
level: advanced
status: docs-checked
description: "Script version-ups in After Effects: replace footage with newer render versions, relink image sequences, and queue renders with versioned output names."
sources:
  - https://ae-scripting.docsforadobe.dev/item/footageitem/
  - https://ae-scripting.docsforadobe.dev/renderqueue/renderqueueitem/
  - https://ae-scripting.docsforadobe.dev/renderqueue/outputmodule/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch footage replacement and comp versioning

**Goal:** when lighting delivers `v012` renders for 40 shots, every AE comp picks them up and renders
out versioned outputs, with one script run instead of 40 manual relinks.

## Replace footage with the latest version

```javascript
app.beginUndoGroup("Version up renders");
for (var i = 1; i <= app.project.numItems; i++) {
  var it = app.project.item(i);
  if (!(it instanceof FootageItem) || !it.file) continue;
  var next = findLatestVersionFile(it.file);   // your pipeline's lookup: returns a File or null
  if (next) it.replaceWithSequence(next, false);
}
app.endUndoGroup();
```

- `FootageItem.replaceWithSequence(file, forceAlphabetical)` takes the FIRST file of the new image sequence as `file` and sets `mainSource` to a new FileSource, filling `name`, `width`, `height`, `frameDuration` and `duration` from the new files. `forceAlphabetical` true uses the "Force alphabetical order" option.
- `FootageItem.replace(file)` does the same for a single file (a movie or still).
- Both methods preserve interpretation parameters from the previous `mainSource`; if the new file has an unlabeled alpha channel, the alpha interpretation is estimated. Check alpha after replacing.
- Collections (`app.project.item(i)`) are 1-based; `app.project.numItems` counts all items including folders, so test `instanceof FootageItem`.
- Wrap the batch in `app.beginUndoGroup()` / `app.endUndoGroup()`.
- To change a footage item's frame rate, set `conformFrameRate` on its `mainSource` (the item's `frameRate` is read-only).

## Queue versioned renders

```javascript
var comp = /* find comp by name */;
var rq = app.project.renderQueue.items.add(comp);   // RQItemCollection.add(comp)
rq.applyTemplate("<RENDER_SETTINGS_TEMPLATE>");     // RenderQueueItem.applyTemplate(templateName)
var om = rq.outputModule(1);
om.applyTemplate("<OUTPUT_TEMPLATE>");              // OutputModule.applyTemplate(templateName)
om.file = new File("<PROJECT_ROOT>/renders/" + comp.name + "_v012.mov");   // OutputModule.file
app.project.renderQueue.render();                   // RenderQueue.render()
```

Template names are those listed for the item (`RenderQueueItem.templates`) and output module (`OutputModule.templates`) in your install; use those exact strings. Alternatively save the project and render with aerender on the farm (`creative-arts.animation.scripting.aerender-cli`).

## Gotchas

- Parse version numbers from names rather than relying on folder sort order when padding varies.
- A pipeline should record which version each comp uses (write a JSON sidecar or update the tracker) so review knows what was rendered.

## Verify

Dry-run mode that only logs "item -> new version" pairs; compare to the tracker's latest versions, then
run for real and spot-check footage paths in the Project panel.

## Checked

2026-11-09. Confirmed against the After Effects Scripting Guide (docsforadobe markdown on GitHub): `FootageItem.replace()` and `replaceWithSequence()` behaviour and parameters, `FootageItem.file`, `RQItemCollection.add()`, `RenderQueueItem.applyTemplate()`, `OutputModule.applyTemplate()`, `OutputModule.file`, `RenderQueue.render()`, `Project.numItems`, `app.beginUndoGroup()`/`endUndoGroup()`, and `conformFrameRate` on frame rate. Corrected: interpretation is preserved by the replace methods (the earlier claim that it can reset was removed). Removed unconfirmed claims: the folder-scanning ExtendScript file-system code, the "Best Settings" and "ProRes 4444 alpha" template names, and the placeholder colour-bars note.
Method: documentation only; no commands were run.
