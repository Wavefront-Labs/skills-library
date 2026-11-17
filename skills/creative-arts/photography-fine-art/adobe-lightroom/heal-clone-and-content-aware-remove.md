---
id: creative-arts.photography-fine-art.adobe-lightroom.heal-clone-and-content-aware-remove
name: heal-clone-and-content-aware-remove
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, content-aware-remove, lightroom-transform, spot-removal, heal, clone, visualize-spots, lightroom-classic]
level: practitioner
status: draft
description: "Retouch with the Lightroom Classic Remove tool: content-aware remove, heal and clone modes, Visualize Spots for dust, source selection and syncing spots."
sources: ["https://helpx.adobe.com/lightroom-classic/help/remove-tool.html", "https://helpx.adobe.com/lightroom-classic/desktop/help/healing-tool.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heal, clone and content-aware remove

The Remove tool (`Q`) replaced Spot Removal/Heal in Lightroom Classic 13.3. Modes:
- **Remove** (content-aware): paint over an object; Lightroom synthesises a fill. Best for complex areas.
- **Heal**: copies texture from a source and blends tone/colour to the destination. Best for dust and skin spots.
- **Clone**: copies pixels exactly. Best near edges and lines where blending smudges.

## Dust removal
1. Tick **Visualize Spots** in the toolbar and raise the slider: dust becomes white outlines on black.
2. Click each spot with Heal at a brush slightly larger than the spot.
3. Sync spots to other frames from the same session (Sync > Process > Remove/Spot Removal) then check each: synced spots can land on detail.

## Moving the source
Drag the source pin; or press `/` to pick a new source automatically. Ctrl/Cmd-drag to set source manually.

## Strokes
Brush strokes (not just circles) cover wires and long cracks. Shift-click two points for a straight line.

## Content-aware tips
- Click **Refresh** for a different fill variation.
- Large removes look smeared; for those use Generative Remove or round-trip to Photoshop.

## Gotchas
- Spot edits are ordered: removing an early spot can change later ones that sampled it.
- Upright or crop changes after spotting can shift spots; finish geometry first.

## Verify
- [ ] Visualize Spots shows no remaining dust; at 100% repairs show no repeated texture patterns.
