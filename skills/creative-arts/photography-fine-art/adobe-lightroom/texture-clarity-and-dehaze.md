---
id: creative-arts.photography-fine-art.adobe-lightroom.texture-clarity-and-dehaze
name: texture-clarity-and-dehaze
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, texture-clarity-dehaze, lightroom-develop, presence-panel, local-contrast, lightroom-classic]
level: practitioner
status: draft
description: "Use Lightroom Classic Texture, Clarity and Dehaze correctly: what frequency each affects, safe ranges, negative values, and applying them locally with masks."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Adjust image tone and color; Presence controls)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture, Clarity and Dehaze

All three sit in the Basic panel's Presence section and are also available as local adjustments.

| Slider | What it acts on | Positive | Negative |
|---|---|---|---|
| Texture | Medium-fine detail (skin pores, foliage, bark) | Crisper detail without haloes | Smooths skin while keeping eyes and edges |
| Clarity | Mid-tone local contrast at larger radius | Punchy, gritty; haloes at high values | Soft glow, dreamy |
| Dehaze | Atmospheric haze via a dark-channel contrast model | Cuts haze, saturates and darkens | Adds mist/fog |

## Safe working
- Global: Texture +10 to +25, Clarity +5 to +20, Dehaze +5 to +15 is a typical upper range for natural landscape work. Beyond this, watch skies and edges at 100%.
- Dehaze also darkens and shifts colour (often blue); compensate with Exposure, Temp and Vibrance.
- Portraits: never add global Clarity; use negative Texture (-15 to -30) in a skin mask instead.
- Prefer local application: brush or AI mask a hazy background with +Dehaze, or Sky mask with +Clarity.

## Gotchas
- Dehaze reveals sensor dust spots and vignetting; check with Visualize Spots afterwards.
- Combined high Clarity + Dehaze creates bright haloes along horizons, very visible in prints.
- These sliders increase apparent noise; apply Denoise first.

## Verify
- [ ] At 100% and 200% zoom, no halo lines at high-contrast edges; at fit-to-screen the image still looks natural.
