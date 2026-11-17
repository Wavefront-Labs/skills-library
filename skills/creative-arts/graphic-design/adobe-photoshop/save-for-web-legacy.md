---
id: creative-arts.graphic-design.adobe-photoshop.save-for-web-legacy
name: save-for-web-legacy
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-export, save-for-web, gif-optimisation, png-8, jpeg-quality, file-weight]
level: practitioner
status: draft
description: "Use Save for Web (Legacy) when Export As falls short: GIF and PNG-8 palettes and dithering, JPEG quality vs weight, metadata, and optimise-to-file-size."
sources:
  - https://helpx.adobe.com/photoshop/using/optimizing-images.html
  - https://helpx.adobe.com/photoshop/using/export-artboards-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Save for Web (Legacy)

**Goal:** the smallest acceptable web image when you need controls Export As lacks.

## When to use it over Export As
- Animated GIFs from the Timeline.
- **GIF / PNG-8** with colour palette, dither and transparency matte control.
- **Optimize to File Size** (target KB, e.g. ad networks' 150 KB caps).
- 2-up/4-up comparison with file size and download time per setting.

## Opening
File > Export > **Save for Web (Legacy)** (Alt+Shift+Ctrl/Cmd+S). Works up to ~8,000 px; large
documents are slow.

## Settings per format
- **JPEG**: Quality 60-80 typical for photos; Progressive on; Optimized on; Embed Color
  Profile off but **Convert to sRGB** on; Metadata None or Copyright.
- **PNG-24**: lossless, full alpha - flat graphics with gradients/transparency.
- **PNG-8 / GIF**: palette 2-256 colours. Selective/Adaptive reduction; Dither 0-100% (more =
  smoother gradients, bigger file); Transparency + Matte set to the page background colour to
  avoid halo pixels around anti-aliased edges. Lock key colours (brand colours) in the colour table.
- Image Size tab: resample here only for quick jobs; resize properly in the document for best quality.

## Optimize to File Size
Flyout menu > Optimize to File Size > target KB, "Current Settings" or auto GIF/JPEG.

## Gotchas
- Save for Web strips most metadata and does not support CMYK; convert to sRGB 8-bit.
- Animated GIF frame delays and Looping Options (Forever) are set at the bottom.
- Modern web prefers WebP/AVIF; Export As or other tools produce those, Save for Web does not.

## Verify
- [ ] File size under target; check colours vs original side by side in 2-up.
- [ ] No halo around transparent edges on the real background.
