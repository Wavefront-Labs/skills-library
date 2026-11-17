---
id: creative-arts.graphic-design.adobe-indesign.object-layer-options-for-psd-and-ai
name: object-layer-options-for-psd-and-ai
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, object-layer-options, psd-layers, layer-comps, placed-psd, placed-ai, update-link-options, language-versions, indesign-graphics]
level: practitioner
status: draft
description: "Show and hide layers and layer comps of placed PSD, AI and PDF files in InDesign with Object Layer Options, and keep visibility overrides when links update."
sources:
  - https://helpx.adobe.com/indesign/using/placing-graphics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Object layer options for placed PSD and AI

**Goal:** one layered source file (photo with alternative backgrounds, a map with language layers,
a product shot with and without shadow) placed several times in InDesign showing different layers.

## On place
- File > Place with **Show Import Options** checked (or Shift-click Open). For PSD: the **Layers** tab lists
  layers and **Layer Comps**; for PDF and AI (saved with PDF compatibility and Create Acrobat Layers):
  the Layers tab lists top-level layers.
- Set visibility, then choose **When Updating Link: Use PSD/PDF's Layer Visibility** or **Keep Layer
  Visibility Overrides**.

## After placing
- Select the image, Object > **Object Layer Options**. Toggle layer eyes or pick a layer comp, with Preview on.
- The Links panel shows the image once per instance; each instance keeps its own visibility.

## Good uses
- **Language versions:** text layers in the AI or PSD per language, toggled per document version (or combine
  with InDesign conditional text and layers).
- **Product variants:** one PSD with colourway layers; each catalogue page shows one.
- **Clipping alternatives:** a shadow layer turned off where the product sits on a coloured background.

## Gotchas
- Only top-level layers in AI/PDF are listed; sublayers are not individually controllable.
- AI files must be saved with **Create PDF Compatible File** on, otherwise InDesign cannot show them.
- If the source designer renames or reorders layers, overrides may break: Keep Layer Visibility Overrides
  matches by name. Agree layer names and freeze them.
- Layer visibility in placed PSDs is ignored by some older RIP workflows if the PDF is flattened badly;
  export PDF/X-4 and check in Acrobat.

## Verify
- [ ] Each instance shows the intended layers in Overprint Preview.
- [ ] After updating the source file, visibility on every instance is unchanged.
