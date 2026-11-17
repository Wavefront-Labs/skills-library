---
id: creative-arts.photography-fine-art.adobe-lightroom.lens-profile-chromatic-aberration-and-defringe
name: lens-profile-chromatic-aberration-and-defringe
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, lens-profile-correction, lightroom-detail, chromatic-aberration, defringe, vignetting, lightroom-classic]
level: practitioner
status: draft
description: "Correct lens distortion, vignetting, chromatic aberration and purple/green fringing in Lightroom Classic with profiles, CA removal and the Defringe sliders."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Correct lens distortion and adjust perspective)", "https://helpx.adobe.com/camera-raw/kb/supported-lenses.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lens profile, chromatic aberration and defringe

## Profile (Lens Corrections > Profile)
1. Tick **Enable Profile Corrections**. Lightroom reads make/model from EXIF and selects a profile.
2. If none loads (adapted or manual lenses), choose Make/Model by hand. A missing profile can be created with the Adobe Lens Profile Creator.
3. **Distortion** and **Vignetting** amount sliders (default 100) scale the correction. Reduce Vignetting to 50-70 if you like some falloff, or 0 when adding your own vignette.
4. Many mirrorless lenses embed corrections in the raw ("Built-in Lens Profile applied"); Lightroom applies them automatically.

## Chromatic aberration
- Tick **Remove Chromatic Aberration** for lateral CA (red/cyan or blue/yellow edges toward frame corners). Leave it on by default in your import preset.

## Defringe (axial CA: purple/green fringes on high-contrast edges)
1. Manual tab: pick the **Fringe Selector** eyedropper and click on a purple or green fringe at 200-400% zoom. Lightroom sets the hue range and amount.
2. Or adjust Purple Amount/Hue and Green Amount/Hue directly. Alt/Option-drag shows the affected areas.
3. Watch for desaturated purple or green subject areas (flowers, foliage edges, clothing); if they turn grey, narrow the Hue range or apply defringe locally with a brush (Defringe slider in masks).

## Order
Apply lens profile before Upright and crop: Upright analyses the corrected geometry.

## Verify
- [ ] Straight lines near edges are straight; corners match centre brightness; no coloured fringes at 200% on branches against sky.
