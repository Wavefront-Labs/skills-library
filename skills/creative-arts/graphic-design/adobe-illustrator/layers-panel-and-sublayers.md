---
id: creative-arts.graphic-design.adobe-illustrator.layers-panel-and-sublayers
name: layers-panel-and-sublayers
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-layers, sublayers, locking, layer-organisation, isolation-mode]
level: intro
status: draft
description: "Organise Illustrator artwork with the Layers panel: layers vs sublayers, locking and hiding, template layers, selection targeting and paste remembers layers."
sources:
  - https://helpx.adobe.com/illustrator/using/layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layers panel, sublayers and locking

## Structure
- Every object sits in a layer; groups and paths appear as sublayers inside it.
- Name top-level layers by role: `Guides`, `Artwork`, `Type`, `Backgrounds`, `Dieline`, `Notes` (non-printing).
- Layer Options (double-click): colour of selection highlight, **Template** (dimmed, locked,
  non-printing - for tracing sketches), Print on/off, Preview, Dim images.

## Targeting and selecting
- Click the circle at the right = **target** (select object and its appearance; a layer-level
  target applies effects to everything in the layer).
- Small square = selected art indicator; drag it to move objects to another layer.
- Alt/Opt-click the eye: hide all other layers. Ctrl/Cmd-click the eye: outline view for that layer.

## Locking
- Lock icon per layer or object; Object > Lock Selection (Ctrl/Cmd+2), Unlock All (Ctrl/Cmd+Alt+2).
- Lock backgrounds and dielines early to avoid moving them.

## Useful settings
- Flyout > **Paste Remembers Layers** - pasted objects return to their source layer (useful between documents).
- Flyout > Locate Object to find selected art in the panel.
- Flyout > Collect in New Layer / Release to Layers (Sequence/Build) for animation exports.

## Gotchas
- Non-printing layers are excluded from PDF only if "Create Acrobat Layers" options and print flags are set - verify in the PDF.
- Hidden objects still export in some SVG settings; delete unused artwork.

## Verify
- [ ] Every object lives in a named layer; dieline/notes layers set to non-printing as required.
