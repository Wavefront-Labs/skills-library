---
id: creative-arts.photography-fine-art.adobe-lightroom.external-editor-settings
name: external-editor-settings
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, external-editor-settings, edit-in-photoshop, round-trip, lightroom-classic]
level: practitioner
status: draft
description: "Configure Lightroom Classic external editing to Photoshop and other editors: file format, colour space, bit depth, resolution, naming and stacking."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/introduction-to-lightroom-classic/setting-preferences-lightroom.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Open and edit Lightroom Classic photos in Photoshop)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# External editor settings

Preferences > **External Editing**.

## Edit in Adobe Photoshop (primary)
- File Format: **TIFF** (ZIP compression) or **PSD**. PSD needs Photoshop's "Maximize PSD and PSB File Compatibility" set to Always for Lightroom to show layered previews.
- Color Space: **ProPhoto RGB** (match Lightroom's working gamut) or Adobe RGB if you prefer smaller files and fewer out-of-gamut surprises.
- Bit Depth: **16 bits/component** (8-bit invites banding with heavy edits).
- Resolution: 300 (metadata only; no resampling).

## Additional external editor
- Choose an application (Affinity Photo, Helicon Focus, a Nik plugin host); set its own format and save as a preset ("Helicon - TIFF 16 ProPhoto").
- Ctrl/Cmd+Alt/Option+E opens the additional editor.

## Stack and naming
- Stack With Original: keeps the edited TIFF/PSD next to the raw.
- Edit Externally File Naming: e.g. `{Filename}-Edit` or a custom template with sequence.

## Round trip
1. Photo > Edit In > Edit in Adobe Photoshop (Ctrl/Cmd+E). Raw files open via Camera Raw with Lightroom settings; Lightroom settings are rendered into the TIFF/PSD.
2. In Photoshop, **Save** (not Save As) returns the file to Lightroom in the same folder.
3. Re-editing the TIFF/PSD: choose **Edit Original** to keep layers.
- Open as Smart Object in Photoshop keeps the raw editable inside the PSD.

## Gotchas
- Camera Raw version must support Lightroom's process version, otherwise Lightroom offers "Render using Lightroom".

## Verify
- [ ] After saving in Photoshop, the `-Edit.tif` appears stacked with the raw in Lightroom with matching colour.
