---
id: creative-arts.photography-fine-art.adobe-lightroom.print-resolution-and-print-sharpening
name: print-resolution-and-print-sharpening
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, print-resolution, lightroom-print-module, print-sharpening, ppi, 16-bit-output, lightroom-classic]
level: practitioner
status: draft
description: "Set Print Resolution and Print Sharpening in the Lightroom Classic Print Job panel, understanding ppi, native printer resolution, upsampling and media type."
sources: ["https://helpx.adobe.com/lightroom-classic/help/print-module-basics.html", "https://helpx.adobe.com/lightroom-classic/desktop/help/printing-photos-basic-workflow.html", "Jeff Schewe, The Digital Print (Peachpit) - print resolution and output sharpening"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print resolution and print sharpening

Print Job panel (right side, bottom of Print module).

## Print Resolution
- Lightroom resamples the image to this ppi at the printed size. Common native driver resolutions: **Epson 360 ppi** (720 for fine), **Canon 300 ppi** (600 fine).
- Rule: if the file's native resolution at print size (shown in the cell when Dimensions guides are on) is above 360 (Epson) set 720; between 180 and 360 set 360; below 180, consider Super Resolution first.
- Leaving Print Resolution unticked sends native ppi and lets the driver resample (usually worse).

## Print Sharpening
- Low / Standard / High and Media Type Matte or Glossy (glossy covers lustre, baryta, semi-gloss).
- Applied at final print resolution after resampling: invisible on screen, by design.
- Fine-art cotton matte: Standard or High. Baryta/lustre: Standard. Portraits: Low.

## 16-bit Output
- Tick on macOS for printers/drivers that accept 16-bit data; reduces banding in smooth gradients. Windows drivers generally receive 8-bit.

## Testing
- Print the same detailed crop at Low/Standard/High on your usual paper (Custom Package with three cells) and choose at viewing distance.

## Gotchas
- Double sharpening (heavy capture sharpening + High print sharpening) shows haloes.
- Very high ppi beyond the driver's native step adds nothing and slows spooling.

## Verify
- [ ] Test strip at normal viewing distance: detail crisp, no haloes; gradient areas smooth.
