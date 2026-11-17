---
id: creative-arts.photography-fine-art.adobe-lightroom.ai-denoise-and-manual-noise-reduction
name: ai-denoise-and-manual-noise-reduction
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, ai-denoise, lightroom-detail, noise-reduction, enhance, lightroom-classic]
level: practitioner
status: draft
description: "Remove noise in Lightroom Classic with AI Denoise (Enhance) or manual luminance and colour noise sliders, knowing DNG output, order of operations and limits."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/enhance-details.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Reduce noise)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI Denoise and manual noise reduction

## AI Denoise (raw files)
1. Detail panel > Noise Reduction > **Denoise...** (or Photo > Enhance, Ctrl/Cmd+Alt/Option+I).
2. Set **Amount** (default 50). Preview zooms to a sample; drag in the preview to check other areas. Higher values smooth fine texture: 30-60 covers most files.
3. Lightroom writes a new linear **DNG** (`-Enhanced-NR` suffix) next to the original and stacks them. Edits carry over.
- Do it **first**, before AI masks, Remove and sharpening: AI masks are computed more accurately on clean data. Each file can be enhanced only once; to change the amount, run Denoise on the original raw again.
- Works on Bayer and X-Trans raw files; not on JPEG/TIFF (use manual sliders or Photoshop Camera Raw filter).
- Time depends on GPU; batch selections run in the background.
- Output DNG is roughly 3-4 times the raw file size.

## Manual sliders (any file)
- **Luminance** (0-100): smooths grain; start 15-30. **Detail** (default 50) preserves edge texture; **Contrast** restores local contrast lost to smoothing.
- **Color** (default 25 on raw): removes coloured blotches; rarely needs above 40. **Detail** and **Smoothness** refine it.
- Use local Noise sliders in a mask to smooth only a sky or shadow area.

## Gotchas
- Pushing shadows +2 EV or more after denoising reveals residual noise; denoise the version you will push.
- Grain for look comes after noise reduction (Effects > Grain), never instead of it.

## Verify
- [ ] At 200%, shadows show no colour blotches and fine textures (hair, foliage) are not waxy.
