---
id: creative-arts.animation.scripting.photoshop-scripting-for-layer-export
name: photoshop-scripting-for-layer-export
category: creative-arts
field: animation
product: scripting
tags: [photoshop-scripting, extendscript, jsx, layer-export, photoshop, batch-export, uxp]
level: practitioner
status: draft
description: "Export Photoshop layers to PNG files with scripts: built-in Export Layers to Files, an ExtendScript loop, trim and naming, UXP and COM alternatives and failure checks."
sources:
  - https://helpx.adobe.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Photoshop scripting for layer export

Layered Photoshop files feed animation (cut-out parts, backgrounds, sprites). Exporting by hand is slow; a script is repeatable.

## Built-in first
- **File > Export > Layers to Files** writes one file per layer in a chosen format. Good enough for simple jobs; it has limited naming and trim options.

## ExtendScript (JSX) loop
```javascript
// export_layers.jsx - run via File > Scripts > Browse
var doc = app.activeDocument;
var out = Folder.selectDialog("Export folder");
if (out) {
  var opts = new PNGSaveOptions();
  for (var i = 0; i < doc.layers.length; i++) { doc.layers[i].visible = false; }
  for (var i = 0; i < doc.layers.length; i++) {
    var layer = doc.layers[i];
    layer.visible = true;
    var tmp = doc.duplicate();
    tmp.trim(TrimType.TRANSPARENT);
    var name = layer.name.replace(/[^A-Za-z0-9_-]/g, "_");
    tmp.saveAs(new File(out + "/" + name + ".png"), opts, true);
    tmp.close(SaveOptions.DONOTSAVECHANGES);
    layer.visible = false;
  }
}
```
Notes:
- Top-level `doc.layers` includes groups (`LayerSet`); recurse into `layerSets` for nested layers.
- Trimming loses position; if the part must reassemble, record each layer's `bounds` offset into a JSON/CSV.
- Sanitise layer names for the file system and detect duplicates.
- Set `app.preferences.rulerUnits = Units.PIXELS` before using bounds.

## Alternatives
- Newer Photoshop versions support **UXP** scripting; Adobe's scripting documentation lists the currently supported options for your version.
- Photoshop can be driven externally (for example Python via Windows COM using `win32com.client.Dispatch("Photoshop.Application")`).

## Verify
- [ ] Output count equals the visible layers expected.
- [ ] Names are unique and safe.
- [ ] Offsets are recorded if trimmed.
