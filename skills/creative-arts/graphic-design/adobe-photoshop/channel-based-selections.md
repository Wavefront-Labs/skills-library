---
id: creative-arts.graphic-design.adobe-photoshop.channel-based-selections
name: channel-based-selections
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-selections, channel-selection, alpha-channels, channels-panel, calculations, apply-image, hair-masking, tree-masking, save-selection, load-selection]
level: advanced
status: draft
description: "Make masks from colour channels for hair, trees and fine detail: pick the best channel, push contrast with Levels/Curves, and save/load alpha channels."
sources:
  - https://helpx.adobe.com/photoshop/using/channel-basics.html
  - https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Channel-based selections

**Goal:** a precise mask for complex edges (hair against sky, tree branches, smoke) built from
the image's own contrast.

## Method
1. Window > Channels. Click Red, Green, Blue in turn and find the one where the subject and
   background differ most (sky behind hair: usually **Blue**; foliage against sky: Blue).
2. **Duplicate** that channel (drag to New Channel). Never edit the original colour channel.
3. On the copy, increase contrast:
   - Image > Adjustments > **Levels**: drag black and white input sliders inward until the
     background is pure white (or black) and the subject solid, keeping edge detail.
   - Or **Curves** for finer control; or Image > Apply Image / **Calculations** to combine two
     channels (e.g. Blue Multiply Blue) for even more contrast.
4. Paint the solid interior with a hard black/white brush (Overlay mode brush protects edges:
   black brush in Overlay darkens darks without touching lights).
5. **Dodge/Burn** tools on the channel with Range: Highlights/Shadows to push edges selectively.
6. Invert if needed (Ctrl/Cmd+I) so the subject is white.
7. **Ctrl/Cmd+click the channel thumbnail** to load it as a selection, return to RGB (Ctrl/Cmd+2),
   select the layer, add a layer mask.

## Alpha channels
- Any saved selection is an alpha channel: Select > **Save Selection** (name it), **Load Selection**
  with add/subtract/intersect options.
- Alpha channels increase file size and are kept in PSD/TIFF; delete unused ones before delivery
  (some printers' RIPs dislike extra channels).

## Combining with other tools
Use the channel mask for hair, a pen path for the hard body edge, and combine (Ctrl/Cmd+Shift+click
adds a selection). Then fix colour contamination at edges (see select and mask skill).

## Gotchas
- Busy backgrounds with similar luminance defeat channel masks; use Select and Mask or reshoot.
- Pushing Levels too hard thickens or chops hair; zoom to 100% on edges while adjusting.

## Verify
- [ ] Mask shows fine strands intact without background haze (view mask alone).
- [ ] Composite against a contrasting background at 100%: no halos.
- [ ] Spare alpha channels removed from the delivery file.
