---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.exporting-and-importing-comic-text-in-csp
name: exporting-and-importing-comic-text-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-text-tool, csp-balloons, csp-text-export, script-import, batch-export, translation-workflow]
level: advanced
status: draft
description: "Move comic text in and out of Clip Studio Paint: paste scripts into the Story Editor, export text with Batch export, keep text editable in PSD and support translation."
sources:
  - https://tips.clip-studio.com/en-us/articles/6683
  - https://tips.clip-studio.com/en-us/articles/849
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting and importing text

## Import a script
- **EX:** Story > Text Management > Open Story Editor, then paste the script (one balloon per paragraph,
  blank lines between); set "Always create new layer" so each paragraph becomes a text layer.
- **PRO:** copy and paste blocks into text layers page by page.

## Export text
- **File > Export multiple pages > Batch export** (EX for multiple pages): the dialog has an option to
  **output text** to a file alongside images, giving a text file of all text layers for proofreading or
  translation.
- **Editable text for other apps:** export to **.psd/.psb** keeps text layers editable (other formats
  rasterise text). Use this when handing pages to a letterer in Photoshop or a localisation team.
- Single page: copy text from the text layer or the Story Editor.

## Translation workflow
1. Export text file and PSDs (or keep the .clip source).
2. Translator returns text matched to page and balloon order.
3. Paste into the Story Editor (EX) or a duplicate story file; reflow balloons.
4. Keep the original-language text layers hidden in the same file, or one story per language.

## Gotchas
- Text layers order in export follows layer order, not reading order; number balloons or name layers
  ("p05_b03") so translations map back.
- Fonts in PSD must be installed on the receiving machine.
- Rasterised text in JPEG/PNG exports cannot be edited later; keep the source.

## Verify
- [ ] Exported text file has every balloon; PSD opens with live text layers.
