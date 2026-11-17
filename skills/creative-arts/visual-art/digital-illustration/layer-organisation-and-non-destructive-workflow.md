---
id: creative-arts.visual-art.digital-illustration.layer-organisation-and-non-destructive-workflow
name: layer-organisation-and-non-destructive-workflow
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-layers, layer-masks, layer-organisation, non-destructive, layer-groups, filter-layers, adjustment-layers, krita, clip-studio-paint, photoshop]
level: practitioner
status: draft
description: "Organise layers for a painting you can still change: naming and grouping, masks instead of erasing, adjustment/filter layers, merging checkpoints, and file versioning in Krita, CSP and Photoshop."
sources: ["https://docs.krita.org/en/user_manual/layers_and_masks.html", "https://helpx.adobe.com/photoshop/using/layer-basics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer organisation and non-destructive workflow

**Goal:** keep a digital painting editable as long as useful, without drowning in
hundreds of unnamed layers (Krita Manual, layers and masks; CSP and Photoshop docs).

## Structure that scales
- **Groups** by stage or element: `sketch`, `line`, `flats`, `shading`, `fx`,
  `background`. Name layers as you create them.
- Colour-label groups (Krita and Photoshop support colour labels).
- Keep the sketch on its own layer at low opacity, hidden later, never deleted.

## Non-destructive tools
- **Layer masks** instead of erasing: paint black to hide, white to reveal; restore
  anytime. Krita: transparency masks; CSP: layer masks; Photoshop: layer masks.
- **Adjustment / filter layers**: colour changes (curves, HSV, levels, gradient map)
  as separate layers or masks you can tweak or delete. Krita: filter layers and
  filter masks; CSP: correction layers; Photoshop: adjustment layers.
- **Clipping**: shading and texture clipped to flats so they never spill (see the
  rendering-light skill).
- **Transform** with smart objects (Photoshop) or on duplicates, so scaling does not
  degrade pixels repeatedly.

## Merging checkpoints
Painterly work eventually needs a merged surface to paint over. Before merging:
1. Save a versioned copy (`piece_v07_layers.kra`).
2. Merge visible into a new layer (Krita: Layer > New > New Layer From Visible;
   Photoshop: Ctrl+Alt+Shift+E / Cmd+Opt+Shift+E "stamp visible") and paint on top.
This gives freedom to paint without losing the layered version.

## Housekeeping
- Delete empty layers; merge tiny touch-up layers into their parent.
- Watch memory: layer count times canvas size; Krita shows image memory in the status bar.
- Save in the native layered format (.kra, .clip, .psd); export flattened copies separately.

## Gotchas
- Painting the final on the sketch layer.
- Erasing on masks' parent instead of the mask (check which thumbnail is active).
- Overwriting the only layered file with a flattened export.

## Verify
- [ ] Groups named by stage/element; no unnamed clutter.
- [ ] Masks and adjustment layers used instead of destructive edits.
- [ ] Versioned layered saves exist before merges.
