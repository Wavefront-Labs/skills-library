---
id: creative-arts.graphic-design.adobe-illustrator.asset-export-for-screens
name: asset-export-for-screens
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-export, asset-export, export-for-screens, png, svg, pdf, ios-android-scales, icon-export, batch-export]
level: practitioner
status: draft
description: "Batch-export icons and artboards from Illustrator with the Asset Export panel and Export for Screens: multiple scales and formats, suffixes, naming, and padding control."
sources:
  - https://helpx.adobe.com/illustrator/using/collect-assets-export.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset Export and Export for Screens

**Goal:** a full set of correctly named assets in every size and format with one click,
repeatable when art changes.

## Two routes
- **Export for Screens (Alt+Ctrl+E / Opt+Cmd+E):** exports **artboards** or the assets in
  the Asset Export panel. Best when each icon has its own artboard (exact size, padding).
- **Asset Export panel (Window > Asset Export):** drag objects or groups in; each becomes a
  named asset exported to its **artwork bounds**. Best for picking pieces out of one layout.

## Set up formats
In Export for Screens > Formats:
- Add scales: 1x, 2x, 3x (iOS) with suffixes `@2x`, `@3x`; or Android density folders
  (Android preset gives mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi).
- Formats: PNG, PNG8, JPG, SVG, PDF, WebP (newer versions).
- **Prefix** for naming (e.g. `ic_`).
- "Create Sub-folders" sorts outputs by scale or format.
- Advanced settings (gear) per format: PNG anti-aliasing (Art Optimized vs Type Optimized),
  background transparent; SVG styling (see SVG export skill).

## Naming
Asset and artboard names become file names: `ic_search`, `ic_close`. Use lowercase,
hyphens or underscores, no spaces - developers will thank you.

## Control the bounds (padding)
- Artboard route: art centred on a fixed 24x24 artboard gives consistent padding for icon sets.
- Asset route exports the visible bounds - strokes and effects included. If you need fixed
  padding, add an invisible rectangle (no fill, no stroke) of the target size grouped with
  the icon.

## Gotchas
- Strokes exported as PNG at small sizes blur unless aligned to the pixel grid (see pixel
  grid alignment skill).
- Hidden layers are skipped; locked are exported.
- Re-exporting overwrites files with the same names without asking.

## Verify
- [ ] Output folder contains every asset at every scale with consistent names.
- [ ] Open a 1x PNG at 100%: edges crisp, padding as specified.
