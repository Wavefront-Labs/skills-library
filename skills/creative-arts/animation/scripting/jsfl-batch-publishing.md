---
id: creative-arts.animation.scripting.jsfl-batch-publishing
name: jsfl-batch-publishing
category: creative-arts
field: animation
product: scripting
tags: [jsfl-batch, jsfl, adobe-animate, batch-publish, flash-scripting, fla, automation]
level: advanced
status: draft
description: "Batch publish Adobe Animate FLA files with JSFL: openDocument, publish, close, file URIs, FLfile folder listing, logging, running the script and failure handling."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# JSFL batch publishing

JSFL (JavaScript for Flash) is Animate's scripting language: it runs inside the app against the Animate DOM (`fl`, `document`, `FLfile`). Batch publishing opens each FLA and publishes with its saved publish settings.

## Script sketch
```javascript
// publish_all.jsfl
var folder = fl.browseForFolderURL("Choose the folder of FLA files");
if (folder) {
  var files = FLfile.listFolder(folder + "/*.fla", "files");
  for (var i = 0; i < files.length; i++) {
    var uri = folder + "/" + files[i];
    var doc = fl.openDocument(uri);
    fl.outputPanel.trace("Publishing " + files[i]);
    doc.publish();            // uses the document's publish profile
    doc.close(false);         // false = do not save changes
  }
  fl.outputPanel.save(folder + "/publish_log.txt");
}
```

## Notes
- **URIs, not paths**: JSFL uses `file:///` URIs (for example `file:///C|/shows/ep01/scene.fla` on Windows; `file:///Users/...` on macOS). `FLfile.platformPathToURI()` converts a normal path.
- **Publish settings** come from the FLA's active publish profile, so set the target (HTML5 Canvas, WebGL, video export, etc.) and output folder in each file, or import a shared profile using the document's profile methods.
- **Run** the script via Commands > Run Command, or open the .jsfl file with Animate. The object model is documented in the JSFL API reference for your version.
- **Logging**: `fl.outputPanel.trace()` and `.save()`, or write with `FLfile.write()`.
- **Failures**: wrap each file in try/catch, record the error and continue with the next so one bad file does not stop the batch.
- Close documents you open, or the app accumulates tabs and memory.
- Do not run on the only copy of source files until it has been tested on duplicates.

## Gotchas
- Missing fonts or linked assets cause dialogs that block unattended runs; resolve them first.
- Animate versions differ in which methods are available; test on the version used in production.

## Verify
- [ ] Test on a duplicate folder of three files.
- [ ] Output files exist and open correctly; the log lists every file.
