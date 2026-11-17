---
id: creative-arts.photography-fine-art.adobe-lightroom.output-sharpening-on-export
name: output-sharpening-on-export
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, output-sharpening, lightroom-export, sharpening, resizing, lightroom-classic]
level: practitioner
status: draft
description: "Choose Lightroom Classic output sharpening on export by medium and amount (screen, matte, glossy), and know how it interacts with resizing and capture sharpening."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html", "Bruce Fraser and Jeff Schewe, Real World Image Sharpening (Peachpit) - output sharpening"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Output sharpening on export

Output sharpening compensates for softness from resampling and the output medium (ink spread on paper, screen pixel pitch). It is applied **after resizing**, based on the final pixel size and medium, so it is never visible in Develop.

## Settings (Export > Output Sharpening; also in Print Job)
- **Sharpen For**: Screen, Matte Paper, Glossy Paper.
- **Amount**: Low, Standard, High.
- Algorithm derived from PixelGenius PhotoKit Sharpener.

## Choosing
- Screen: Standard for most web images; Low for portraits; High only for small downsized landscape images.
- Matte paper (fine-art cotton rag, watercolour): Standard to High; ink spreads more.
- Glossy/lustre/baryta and lab C-type: Standard.
- Metal/acrylic labs often sharpen themselves; ask the lab.
- When the file goes to someone who will resize it (designer, publisher, print master), **no output sharpening**: sharpening must happen at final size.

## Testing
- Make a strip of the same crop at Low/Standard/High on your paper; evaluate at normal viewing distance, not with a loupe. Output sharpening looks crunchy on screen at 100%, which is expected for print.

## Gotchas
- Combined with heavy capture sharpening, High output sharpening makes haloes visible in prints.
- Exports with no resizing still get sharpening if ticked.

## Verify
- [ ] Test print at viewing distance shows crisp detail without haloes; a web export at 100% looks crisp without grit.
