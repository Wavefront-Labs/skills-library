---
id: creative-arts.photography-fine-art.adobe-lightroom.basic-panel-tone-controls
name: basic-panel-tone-controls
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, basic-panel-tone, lightroom-develop, clipping-preview, exposure, highlights-shadows, lightroom-classic]
level: practitioner
status: draft
description: "Set tone in the Lightroom Classic Basic panel: exposure, contrast, highlights, shadows, whites and blacks with clipping previews and Auto as a reference."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Adjust image tone and color)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Basic panel tone controls

## Order
1. **Exposure**: set midtones (skin, mid-grey stone, grass) to look right. Ignore highlights for now.
2. **Contrast**: overall separation around the midpoint.
3. **Highlights** (pull down to recover bright detail) and **Shadows** (lift to open dark detail). These are tone-mapping sliders that protect the extremes.
4. **Whites** and **Blacks**: set the end points. Hold **Alt/Option** while dragging: the image turns black (whites) or white (blacks) and only clipping pixels show in colour. Stop where only specular highlights and true black accents clip.
5. Re-check exposure; the sliders interact.

## Tools
- Histogram triangles (top corners) or `J` toggle clipping overlays: red = highlights, blue = shadows.
- Drag directly on the histogram regions (Blacks, Shadows, Exposure, Highlights, Whites) to move the matching slider.
- **Auto** (Tone > Auto) uses Adobe Sensei; good as a reference point, then refine. Shift+double-click on Whites or Blacks sets each automatically.
- Process Version 6 (current) ranges: Exposure +/-5 EV; others -100..+100.

## Fine-art notes
- For a print, avoid setting blacks to clip on detail you want to read on paper; matte paper cannot hold deep shadow separation anyway (soft-proof).
- Heavy Highlights -100 with Shadows +100 gives flat HDR-looking results; prefer moderate values and local masks.
- Grey uniform skies: lower Highlights before Exposure.

## Gotchas
- Old Process Versions (2010/2012) have different sliders (Fill Light, Recovery). Update via the lightning-bolt icon under the Histogram, and expect a visual change.

## Verify
- [ ] Alt-drag on Whites/Blacks shows only intentional clipping; histogram touches but does not pile up at either edge.
