---
id: computing-software.data-science-and-analytics.data-visualization.colour-and-accessibility
name: colour-and-accessibility
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [colour-palettes, colorblind-safe, sequential-diverging]
level: practitioner
status: docs-checked
description: "Choose sequential, diverging and qualitative colour maps appropriately using Matplotlib's lightness guidance and avoid jet-style maps."
sources:
  - https://matplotlib.org/stable/users/explain/colors/colormaps.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour
- Sequential maps change lightness (and often saturation) incrementally, often from a single hue; use them for information that has ordering.
- Diverging maps use two colours that meet in the middle at an unsaturated colour; use them when the data has a critical middle value or deviates around zero.
- Cyclic maps are for values that wrap around, such as phase angle, wind direction or time of day.
- Qualitative maps are miscellaneous colours for information with no ordering or relationships; they are not perceptual maps.
- The perceptually uniform sequential maps listed by Matplotlib are `viridis`, `plasma`, `inferno`, `magma` and `cividis`.
## Gotchas
- Check lightness (CIELAB L*): sequential maps should increase it monotonically. Maps with plateaus or kinks in L* (Matplotlib names autumn, cool, spring, winter, afmhot, copper, gist_heat and hot) cause a perception of banding.
- `jet` and `hsv` have L* varying widely, which makes them a poor choice for representing data perceptually.
- Diverging maps should rise to a lightness maximum near 100 and fall again, with similar minima at both ends; the page names `BrBG` and `RdBu` as good options and notes `coolwarm` spans a narrower L* range.
## Verify
- [ ] Check the lightness order survives in greyscale, and test with a colour-vision-deficiency simulator.

## Checked

2026-11-09. Confirmed against the Matplotlib choosing-colormaps page (searched by keyword, then the sequential, diverging, qualitative and jet passages read): map category definitions, perceptually uniform sequential list, banding, jet and hsv warning, diverging recommendations. Removed: the ColorBrewer source (JavaScript page, not readable), the red/green advice, the 6-8 category limit, the WCAG contrast note, the rcParams and seaborn palette code, and the sentence about shapes and annotation (none found on the Matplotlib page).
Method: docs-checked 2026-11-09 against the Matplotlib colormaps page only.
