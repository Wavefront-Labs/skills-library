---
id: creative-arts.visual-art.digital-illustration.clip-studio-sub-tools-and-brush-settings
name: clip-studio-sub-tools-and-brush-settings
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, clip-studio-paint, digital-brushes, brush-engine, clip-studio-brushes, sub-tools, sub-tool-detail, clip-studio-assets, brush-density, ink-bleed]
level: practitioner
status: draft
description: "Configure Clip Studio Paint brushes: tools vs sub tools, the Sub Tool Detail palette, pressure and stroke settings, brush tips and textures, assets, and backing up sub tools."
sources: ["https://assets.clip-studio.com/en-us/", "https://tips.clip-studio.com/en-us"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clip Studio Paint sub tools and brush settings

## Structure
- **Tools** (Pen, Pencil, Brush, Airbrush, Decoration, Eraser...) each contain **sub tools** (e.g. G-pen, Mapping pen, Turnip pen under Pen). A sub tool is a saved brush.
- **Tool Property** palette shows the common settings; the wrench icon opens **Sub Tool Detail** with every setting.

## Important settings (Sub Tool Detail)
- **Brush size** with pressure dynamics (the small graph button sets the pressure curve per setting).
- **Ink**: opacity, blending mode, anti-aliasing, **combine mode**; **colour mixing** (Blend / Running colour) and paint amount/density for painterly brushes.
- **Brush tip**: circle or material tip(s) (images), thickness, direction (by pen tilt, direction of line, random), multiple tips.
- **Stroke**: **interval** (spacing; lower = smoother), repeat method, ribbon.
- **Texture**: paper texture, density, with pressure.
- **Watercolour edge** for wet media look.
- **Correction**: stabilization, post-correction, vector magnet, speed - important for inking.
- **Starting and ending**: taper in/out by length or percentage; useful for line art without pressure.

## Make your own
- Duplicate a sub tool (sub tool palette menu > Duplicate sub tool), edit the copy, keep the original.
- Register frequently used settings to the Tool Property view (eye checkbox in Sub Tool Detail).
- **Assets**: download brushes from Clip Studio ASSETS; they appear in the Download folder of the Material palette; drag them into the Sub Tool palette.

## Backup and moving
- Export a sub tool as `.sut` (right-click > Export sub tool); import with "Import sub tool".
- Back up all settings via Clip Studio's cloud/backup function, or the File > Export settings options in your version.

## Gotchas
- Editing the default sub tool and forgetting: use "Reset to initial setting" on the sub tool.
- Pressure that feels wrong everywhere is usually the **global pen pressure** setting (File > Adjust pen pressure detection level) rather than the brush.
- Stabilization set high makes lines lag on fast strokes.

## Verify
- [ ] Customised brushes are duplicates, not overwritten defaults.
- [ ] Global pen pressure calibrated.
- [ ] Custom sub tools exported as .sut backups.
