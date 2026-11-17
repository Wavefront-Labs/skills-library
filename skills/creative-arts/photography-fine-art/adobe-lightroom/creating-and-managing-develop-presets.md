---
id: creative-arts.photography-fine-art.adobe-lightroom.creating-and-managing-develop-presets
name: creating-and-managing-develop-presets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, develop-presets, lightroom-presets, xmp-presets, preset-amount, lightroom-classic]
level: practitioner
status: draft
description: "Create Lightroom Classic develop presets with only the right settings ticked, organise groups, use preset Amount, install XMP presets and back them up."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/apply-presets.html", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creating and managing develop presets

## Create
1. Edit a reference image.
2. Presets panel `+` > **Create Preset**. Name it and choose a group (`Project - Coastline`, `Base - Import`).
3. **Tick only the settings the preset should change.** A look preset should not include White Balance, Exposure, Crop, Spot Removal or Lens Profile; otherwise it overwrites per-image work.
4. Optional: Support Amount Slider; Auto Settings (applies Auto Tone per image).

## Apply
- Click to apply; hover for preview in Loupe. Presets are cumulative only for the settings they include.
- **Amount** slider (top of Presets panel) scales a preset with "Support Amount Slider" from 0-200.
- Apply at import via Develop Settings in the Import dialog.
- Presets with masks: AI masks inside presets recompute on each image (adaptive presets: Sky, Subject, People).

## Organise and share
- Right-click > Move, Export (`.xmp`), Import (`.xmp`, `.zip`, legacy `.lrtemplate` converts automatically).
- Hide unused groups: Presets panel `...` > Manage Presets.
- Location: Preferences > Presets > Show Lightroom Develop Presets (`Settings` folder, shared with Camera Raw). Back this folder up.
- "Store presets with this catalog" (Preferences > Presets) keeps presets per-catalog; off by default.

## Gotchas
- Presets built on a different profile or Process Version look different; include the profile in look presets made for raw.
- Updating a preset: right-click > Update with Current Settings (choose settings again).

## Verify
- [ ] Apply the preset to an unedited image: only intended sliders change (check History entry).
