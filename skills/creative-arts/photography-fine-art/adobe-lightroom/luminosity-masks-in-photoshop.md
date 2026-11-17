---
id: creative-arts.photography-fine-art.adobe-lightroom.luminosity-masks-in-photoshop
name: luminosity-masks-in-photoshop
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, luminosity-masks, edit-in-photoshop, channel-masks, apply-image, photoshop]
level: practitioner
status: draft
description: "Build luminosity masks in Photoshop from channels (lights, darks, midtones, intersected ranges) and use them for precise tonal edits after a Lightroom round trip."
sources: ["https://helpx.adobe.com/photoshop/user-guide.html (Channel basics; Load selection from channel; Apply Image)", "https://helpx.adobe.com/photoshop/using/channel-basics.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Luminosity masks in Photoshop

A luminosity mask is a selection derived from the image's own brightness, so adjustments blend with no edges.

## Build the basic set
1. Channels panel: **Ctrl/Cmd-click the RGB composite thumbnail**. This selects brightness (pixels selected in proportion to their lightness): **Lights 1**. Save it: Select > Save Selection > `Lights 1`.
2. **Lights 2**: with Lights 1 active, Ctrl/Cmd+Alt/Option+Shift-click the Lights 1 channel (intersect with itself) and save. Repeat for Lights 3, 4 (each narrower, brighter tones only).
3. **Darks 1**: load Lights 1, Select > Inverse, save. Darks 2-4 by self-intersection.
4. **Midtones**: Select All, then subtract Lights 1 and Darks 1 (Ctrl/Cmd+Alt/Option-click), save as `Mids 1`.
- Alternative: Image > Apply Image or Calculations (Multiply a channel with itself) for the same result with more control.

## Use
1. Load the mask (Ctrl/Cmd-click its channel), then add a Curves or Levels adjustment layer: the selection becomes its layer mask.
2. Typical: Curves on Lights 3 to bring down bright sky; Curves on Darks 2 to open shadows; Hue/Saturation on Mids to add saturation only in midtones.
3. Refine the layer mask with a brush, or Properties > Density/Feather. Paint black where the effect should not apply.

## Gotchas
- Selections with under 50% selected pixels show "No pixels are more than 50% selected" warnings; the mask still works.
- Masks are made from the current state; build them after major global tone moves.
- Panels like TK8 or Lumenzia automate the build; understanding the channel method lets you check them.

## Verify
- [ ] Toggle the adjustment layer: change confined to the intended tonal range with no visible transitions.
