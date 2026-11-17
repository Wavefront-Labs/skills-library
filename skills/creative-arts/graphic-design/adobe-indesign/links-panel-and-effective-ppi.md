---
id: creative-arts.graphic-design.adobe-indesign.links-panel-and-effective-ppi
name: links-panel-and-effective-ppi
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, links-panel, effective-ppi, actual-ppi, relink, update-links, missing-links, modified-links, indesign-graphics, preflight]
level: practitioner
status: draft
description: "Manage InDesign placed files with the Links panel: missing and modified links, relink to folder, effective vs actual ppi, panel columns, and preflight rules for resolution."
sources:
  - https://helpx.adobe.com/indesign/using/graphics-links.html
  - https://helpx.adobe.com/indesign/using/preflighting-files-handing-off.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Links panel and effective ppi

**Goal:** every placed image and graphic in an InDesign document is present, current, and at enough
resolution for the output, checked before it costs a reprint.

## Status icons (Window > Links, Ctrl/Cmd+Shift+D)
- **Red stop sign (missing):** file moved or renamed. Relink.
- **Yellow triangle (modified):** the file changed since it was placed. Update Link (or double-click the icon).
- **Embedded** icon: the file is stored in the INDD; unembed to edit it.
- Badge on a frame (View > Extras > Show Link Badge) shows status on the page.

## Relinking
- **Relink** (chain button): browse to the new file. Check **Search for Missing Links in This Folder** to fix
  every missing file found in that folder in one go.
- **Relink to Folder** (panel menu): points the selected links to a folder of same-named files, optionally
  with a different extension (swap low-res JPG placeholders for final TIF or PSD).
- **Relink File Extension**: change PSD to TIF across selected links.
- **Copy Link(s) To** copies files to a folder and relinks to the copies.
- Alt/Option-double-click (or Edit Original) opens the file in its app; save and InDesign updates.

## Effective vs actual ppi
- **Actual ppi:** image pixels per inch at 100% placed size.
- **Effective ppi** = actual ppi / scale. A 300 ppi image enlarged to 150% is 200 ppi effective.
- Targets: ~300 ppi effective for offset photos (240 often acceptable), 1200 ppi for 1-bit line art, 72-150
  for screen-only PDFs. Large-format work accepts lower values at viewing distance.
- Panel options (panel menu > Panel Options): show columns for **Effective PPI**, **Actual PPI**, Scale,
  Colour Space, ICC Profile, Page, so you can sort by ppi.

## Preflight
- In a preflight profile, enable Images and Objects > **Image Resolution** with minimums (e.g. colour 250,
  greyscale 250, 1-bit 800) and Links > **Links missing or modified**. Watch the Preflight indicator in the
  status bar while you work.

## Gotchas
- Scaling a frame vs scaling content: only content scale changes effective ppi.
- Linked images on network drives update slowly; package locally before final output.
- Placed PDFs and AI files show no ppi; their raster contents must be checked in their source files.

## Verify
- [ ] No missing or modified links; panel sorted by effective ppi shows nothing under the spec.
- [ ] Preflight panel reports no errors before export or packaging.
