---
id: creative-arts.graphic-design.adobe-photoshop.blend-modes-and-opacity-vs-fill
name: blend-modes-and-opacity-vs-fill
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, blend-modes, opacity-vs-fill, multiply, screen, overlay, soft-light, color-blend-mode, luminosity, special-eight]
level: practitioner
status: draft
description: "Use Photoshop blend modes by group (darken, lighten, contrast, comparative, component) for real tasks, and know when Fill differs from Opacity."
sources:
  - https://helpx.adobe.com/photoshop/using/blending-modes.html
  - https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blend modes and Opacity vs Fill

**Goal:** pick the blend mode that does the job first time, and control strength with the right slider.

## The groups and what they are for
| Group | Modes | Neutral colour | Typical uses |
|---|---|---|---|
| Darken | Darken, **Multiply**, Color Burn, Linear Burn, Darker Color | white | drop white backgrounds from scanned line art, shadows, textures that only darken |
| Lighten | Lighten, **Screen**, Color Dodge, Linear Dodge (Add), Lighter Color | black | fire/sparks/light leaks shot on black, glows |
| Contrast | **Overlay**, **Soft Light**, Hard Light, Vivid, Linear, Pin Light, Hard Mix | 50% grey | dodge and burn layers (Soft Light/Overlay on a grey layer), texture overlays, contrast boosts |
| Comparative | Difference, Exclusion, Subtract, Divide | black | aligning layers (Difference turns identical pixels black), frequency separation |
| Component | Hue, Saturation, **Color**, **Luminosity** | - | colourising (Color), sharpening or curves without hue shifts (Luminosity) |

Cycle modes: Shift+plus/minus with the Move tool. Shortcuts: Alt+Shift+M (Multiply), S (Screen),
O (Overlay), F (Soft Light), C (Color), Y (Luminosity) - Option on Mac.

## Recipes
- **Line art scan:** set the scan layer to Multiply - paper white vanishes, colour shows through.
- **Curves without colour shift:** Curves adjustment layer set to Luminosity.
- **Texture on a graphic:** texture layer Overlay or Soft Light, clipped to the graphic, at 30-60% opacity.
- **Paint shadows:** new layer, Multiply, paint with a desaturated darker version of the ground colour.

## Opacity vs Fill
- **Opacity** fades the layer **and its layer styles**.
- **Fill** fades only the layer's pixels; layer styles (stroke, drop shadow) stay at full strength.
  Fill 0% + stroke style = outline-only text that stays live.
- **The "special eight"** modes (Color Burn, Linear Burn, Color Dodge, Linear Dodge, Vivid Light,
  Linear Light, Hard Mix, Difference) react differently to Fill than to Opacity - lowering Fill
  gives stronger, more saturated results than lowering Opacity.

## Gotchas
- Blend modes inside a **Pass Through** group affect layers below the group; set the group to
  Normal to contain them.
- CMYK documents disable some modes (Lighter Color, Subtract, Divide, etc.).
- Blend modes on spot/print output can flatten unpredictably in PDF/X-1a; proof the PDF.

## Verify
- [ ] Each blended layer is the simplest mode that achieves the effect.
- [ ] Opacity vs Fill choice correct for layers with styles.
