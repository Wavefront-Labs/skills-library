---
id: creative-arts.animation.scripting.ae-object-model
name: ae-object-model
category: creative-arts
field: animation
product: scripting
tags: [ae-object-model, extendscript, ae-scripting, after-effects, jsx, app-project, compitem, layer, property-tree, undo-group]
level: advanced
status: docs-checked
description: "Script After Effects with ExtendScript: navigating app.project, CompItem, layers and the property tree, undo groups, matchNames, 0- vs 1-based collections."
sources:
  - https://ae-scripting.docsforadobe.dev/
  - https://ae-scripting.docsforadobe.dev/general/project/
  - https://ae-scripting.docsforadobe.dev/property/propertybase/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The After Effects object model

**Goal:** automate repetitive AE work (renaming, building comps, setting properties across hundreds
of layers) with `.jsx` scripts.

## Hierarchy

```
app
 └ project (Project)
    ├ items (ItemCollection, 1-based)  -> CompItem | FootageItem | FolderItem
    ├ renderQueue
    └ activeItem
CompItem
 └ layers (LayerCollection, 1-based) -> AVLayer | TextLayer | ShapeLayer | CameraLayer | LightLayer
Layer
 └ property groups and properties (Transform > Position ...)
```

## Core patterns

```javascript
app.beginUndoGroup("Offset selected layers");
var comp = app.project.activeItem;
if (!(comp instanceof CompItem)) { alert("Select a comp"); }
else {
  var sel = comp.selectedLayers;                    // 0-based array
  for (var i = 0; i < sel.length; i++) {
    var pos = sel[i].property("ADBE Transform Group").property("ADBE Position");
    var v = pos.value;
    pos.setValue([v[0] + 10 * i, v[1]]);            // 2D layer; a 3D layer needs three values
  }
}
app.endUndoGroup();
```

- Collections (`app.project.items`, `comp.layers`) are **1-based**: `comp.layer(1)`, `app.project.item(1)`. The exceptions are plain arrays such as `CompItem.selectedLayers` and `selectedProperties`, which are **0-based**.
- Use **matchNames** (`ADBE Transform Group`, `ADBE Position`, `ADBE Text Properties`) rather than
  display names. A matchName is not displayed, not localized, and stays stable from version to version regardless of the display name.
- Keyframes: `prop.setValueAtTime(t, v)`, `prop.numKeys`, `prop.keyValue(k)`, `prop.setInterpolationTypeAtKey`.
- Find items: loop `app.project.numItems` and test `item.name` and `instanceof`.
- Add things: `app.project.items.addComp(name, width, height, pixelAspect, duration, frameRate)` (width and height 4..30000 px, duration 0..10800 s, frame rate 1..99), `comp.layers.addText("Hello")` (optional string or TextDocument), `comp.layers.addSolid(color, name, width, height, pixelAspect[, duration])` with color `[R, G, B]` in 0..1.

## Text

```javascript
var tl = comp.layer("Title");
var prop = tl.property("ADBE Text Properties").property("ADBE Text Document");
var td = prop.value;
td.text = "Episode 4"; td.fontSize = 72;
prop.setValue(td);
```

## Gotchas

- Wrap edits in `app.beginUndoGroup(undoString)` / `app.endUndoGroup()` so the script is a single undo step. Pairs can be nested (inner names are ignored); `endUndoGroup()` without a begin is an error, and at script end an open group is closed automatically.
- Dumping a property's matchName: select it and run `alert(app.project.activeItem.selectedProperties[0].matchName)`.

## Verify

Run on a copy of the project and undo once: everything returns to the previous state; run again on a
comp with no selection: the script exits with a message, not an error.

## Checked

2026-11-09. Confirmed against the After Effects Scripting Guide (docsforadobe markdown on GitHub): Collection 1-based indexing, `CompItem.selectedLayers` and `selectedProperties` being 0-based, `PropertyBase.matchName`, matchName tables for AVLayer and TextLayer, `ItemCollection.addComp()`, `LayerCollection.addText()` and `addSolid()`, `Property.setValueAtTime()`, `numKeys`, `keyValue()`, `setInterpolationTypeAtKey()`, `Project.numItems`, `app.beginUndoGroup()` and `endUndoGroup()`, TextDocument `text` and `fontSize`. Removed unconfirmed claims: ES3 language restrictions and JSON polyfill note, the "Allow Scripts to Write Files" preference, and the Scripts folder and menu locations.
Method: documentation only; no commands were run.
