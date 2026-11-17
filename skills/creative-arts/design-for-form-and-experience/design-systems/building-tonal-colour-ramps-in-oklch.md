---
id: creative-arts.design-for-form-and-experience.design-systems.building-tonal-colour-ramps-in-oklch
name: building-tonal-colour-ramps-in-oklch
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [tonal-palette, color-ramp, color-system, oklch, perceptual-color, tonal-ramp, design-tokens, color-science]
level: practitioner
status: draft
description: "Build a colour system from tonal ramps in OKLCH: pick hues, set lightness steps for contrast, tame chroma at the extremes, check gamut, and export tokens."
sources:
  - "Bjorn Ottosson, A perceptual color space for image processing - Oklab (bottosson.github.io/posts/oklab)"
  - "CSS Color Module Level 4 and 5 - oklch() and color-mix() (w3.org/TR/css-color-4)"
  - "Material Design 3 - Tonal palettes and HCT (m3.material.io/styles/color/system/how-the-system-works)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tonal colour ramps in OKLCH

**Goal:** colour ramps whose steps have predictable lightness and contrast, so accessible pairings are a matter of arithmetic.

## Why OKLCH
OKLCH = Lightness (0-1), Chroma (0-about 0.4), Hue (0-360), a perceptual space: equal L steps look like equal lightness, unlike HSL where yellow at 50 percent is far lighter than blue. Use CSS `oklch(0.62 0.19 255)` directly.

## Build a ramp
1. **Choose hues:** brand primary, a neutral (low chroma, hue tinted toward brand, C about 0.01-0.03), status colours (red about 25-30, amber about 85, green about 145, blue about 250).
2. **Define lightness stops** shared by all ramps, e.g. 50, 100, 200 ... 900, 950 mapped to L 0.98, 0.95, 0.90, 0.83, 0.74, 0.65, 0.55, 0.46, 0.37, 0.28, 0.20 (tune by testing contrast). Material uses tones 0-100 with fixed lightness: 10, 20, 30, 40 ... 90, 95, 99.
3. **Set chroma per step:** peak at mid-lightness; reduce at very light and very dark ends to stay in gamut (sRGB chroma limits vary by hue; yellows peak at high L, blues at low L). Clamp with `culori` (`clampChroma`) or Colorjs.io gamut mapping (`toGamut`) rather than letting values clip.
4. **Generate in code** (culori, Colorjs.io, or the open-source Leonardo from Adobe by target contrast ratios) and output hex for legacy plus `oklch()` for modern CSS.
5. **Verify contrast:** pairs with at least 4.5:1 for text must differ by roughly 4-5 lightness stops (checked with WCAG 2 ratios, and APCA for reference); fix steps, not exceptions.
6. **Name** steps numerically (`blue-600`) as primitive tokens, then alias semantic roles (`color.action.primary`) (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`).

## Gotchas
- Browser support for `oklch()` is universal in current browsers; provide an sRGB fallback via `@supports` when targeting older engines.
- Out-of-gamut colours get clipped inconsistently; map intentionally.
- Hue shifts in blues when chroma changes: preview ramps side by side.

## Verify
- [ ] All ramps share lightness stops; chroma tapered at the ends.
- [ ] Gamut-mapped output; fallbacks for legacy.
- [ ] Contrast of key pairs computed, not eyeballed.
