---
id: creative-arts.photography-fine-art.adobe-lightroom.hdr-panorama-merge
name: hdr-panorama-merge
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, hdr-panorama, photo-merge, hdr-merge, panorama-merge, lightroom-classic]
level: practitioner
status: draft
description: "Create HDR panoramas in one step in Lightroom Classic from bracketed panorama sets, with capture requirements, settings and recovering from failed merges."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Create HDR panoramas)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDR panorama merge

Photo > Photo Merge > **HDR Panorama**: Lightroom groups the brackets per position, merges each to HDR, then stitches them into one floating-point DNG.

## Capture
- Same number of brackets at every pan position (e.g. 3 frames at -2/0/+2) and identical EV offsets.
- Manual exposure (bracketing around a fixed base), manual WB, manual focus, tripod.
- 30-50% overlap; level the tripod head so the horizon stays straight.
- Shoot a hand or lens-cap frame at start and end to mark sets on the card.

## Merge
1. Select all frames of the set (every bracket of every position).
2. Photo > Photo Merge > HDR Panorama. Lightroom shows the panorama dialog: choose projection, Boundary Warp, Fill Edges, Auto Crop.
3. HDR options (alignment, deghost) use the last HDR merge settings; set them first by doing a single HDR merge if you need deghosting.

## Fallback when it fails
1. Merge each position to HDR separately (select the bracket, Ctrl/Cmd+Shift+H for headless merge with last settings).
2. Select the resulting HDR DNGs and run Photo Merge > Panorama. The result is the same kind of DNG.

## Gotchas
- Mixed bracket counts (one position missing a frame) make the one-step merge fail.
- Processing is heavy: large sets can take many minutes and very large files.

## Verify
- [ ] Merged DNG holds highlight and shadow detail at +/-3 EV and stitch seams are invisible at 100%.
