---
id: creative-arts.graphic-design.adobe-photoshop.layer-comps
name: layer-comps
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, layer-comps, design-variations, client-options, layer-comps-to-files, layer-comps-to-pdf, smart-object-layer-comps]
level: practitioner
status: draft
description: "Present design options from one PSD with layer comps: what they record, updating safely, exporting comps to files or PDF, and smart-object comps."
sources:
  - https://helpx.adobe.com/photoshop/using/layer-comps.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer comps

**Goal:** several design options in one file, each recallable exactly and exportable for review.

## What a comp records
Window > Layer Comps. A comp snapshot stores per layer: **Visibility**, **Position**, and
**Appearance** (layer style and blend mode), plus optionally the Selection for artboards. It does
**not** store pixel content, text content or adjustment settings - those are shared by all comps.

## Workflow
1. Build the base layout. Put variant elements on separate layers/groups (headline A/B,
   colourway 1/2, image options).
2. Set up option 1 (show/hide, move), click **Create New Layer Comp**, name it
   (`Option A - blue`), tick what to record, add a comment for the client.
3. Repeat per option. Click the box at the left of a comp to apply it; arrows step through.
4. **Last Document State** returns to where you were.

## Updating safely
- After changing the design, apply a comp, adjust, then click **Update Layer Comp** (or Update
  Visibility/Position/Appearance individually) for that comp.
- Warning icon on a comp = it refers to deleted or merged layers. Clear the warning after
  checking (right-click > Clear Layer Comp Warning).
- Do not merge or delete layers used by comps.

## Export
- File > Export > **Layer Comps to Files** (one image per comp, prefix naming).
- **Layer Comps to PDF** (one page per comp, comments optional) - quick client deck.
- Artboards + comps: comps can store artboard positions too.

## Smart object layer comps
If a placed smart object's source PSD contains layer comps, select the smart object and choose
the comp in the **Properties** panel - one master component, different states per instance.

## Gotchas
- Text edits apply to all comps - put alternative copy on separate text layers.
- Adjustment layer settings are global; use separate adjustment layers per option and toggle visibility.

## Verify
- [ ] Stepping through comps shows each option correctly with no warnings.
- [ ] Exported files/PDF named per option.
