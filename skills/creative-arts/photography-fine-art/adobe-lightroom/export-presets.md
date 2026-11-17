---
id: creative-arts.photography-fine-art.adobe-lightroom.export-presets
name: export-presets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, export-presets, lightroom-export, export-dialog, file-naming-template, lightroom-classic]
level: practitioner
status: draft
description: "Build Lightroom Classic export presets for print masters, web and submissions: location, naming, file settings, sizing, metadata and post-processing."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html", "https://helpx.adobe.com/uk/lightroom-classic/help/export-presets-settings-plug-ins.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Export presets

File > Export (Ctrl/Cmd+Shift+E). The dialog sections: Export Location, File Naming, Video, File Settings, Image Sizing, Output Sharpening, Metadata, Watermarking, Post-Processing.

## Presets worth having
| Preset | Key settings |
|---|---|
| Print master TIFF | TIFF, 16-bit, ProPhoto RGB or Adobe RGB, no resize, no output sharpening (sharpen at print), All metadata |
| Lab JPEG | JPEG Quality 100, sRGB or lab's profile, resize to exact print px at 300 ppi, Output sharpening Glossy/Matte Standard |
| Web/social | JPEG 80, sRGB, Long Edge 2048 px, Screen Standard, Copyright Only, Remove Location |
| Open call | JPEG, sRGB, exact size/limits from call, filename template `Lastname_Title_01` |

## Location and naming
- Export To: Specific folder > `Exports/<preset>` with "Put in Subfolder"; Existing Files: Ask.
- File Naming: custom template e.g. `{Filename}_{Custom Text}` or `Lastname_{Title}`; Add to This Catalog only for masters you will track.

## Save
Preset panel (left) > Add. Right-click Update with Current Settings. Several presets can be ticked at once to export one file per preset in one run.

## Post-processing
After Export: Do nothing, Show in Explorer/Finder, Open in another application (e.g. a compression tool), or Go to Export Actions folder.

## Gotchas
- "Limit File Size To" (JPEG) lowers quality automatically; check results.
- Built-in presets cannot be exported; custom ones can (right-click > Export).

## Verify
- [ ] Open an export: pixel size, colour profile and metadata match the preset's intent.
