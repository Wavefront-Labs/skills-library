---
id: creative-arts.film-live-action.davinci-resolve.sky-secondaries-relight-and-depth-map
name: sky-secondaries-relight-and-depth-map
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, sky-secondary, sky-grade, background-secondary, relight-tool, depth-map-use, resolve-relight, sky-replacement, gradient-window, depth-isolation]
level: practitioner
status: draft
description: "Isolate and grade skies and backgrounds in Resolve: gradient windows, luma/HSL keys and Magic Mask for skies, the Depth Map effect for depth-based grades, and the Relight FX."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Power Windows, Qualifiers, ResolveFX Depth Map and Relight)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training) - secondaries"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sky secondaries, relight and depth map

**Goal:** control skies and backgrounds separately from the foreground, and reshape light
after the fact - convincingly, without halos.

## 1. Sky secondaries
Order of tools, simplest first:
1. **Gradient window** (Linear window with large softness) angled at the horizon:
   darken/add density and colour to the sky - classic grad filter. Track it if the camera
   tilts.
2. **Luma or HSL qualifier** on the sky (bright, blue): refine with *Clean Black/White*,
   *Blur radius*, *Denoise*; combine with the gradient window (key AND window) to protect
   bright faces/whites below the horizon.
3. **Magic Mask** (Studio, Object mode) for complex edges (trees) - track and refine.
Adjust: reduce gain/offset for density, add saturation carefully (blue skies noisy),
hue-shift toward cyan or warmer for time-of-day.
Check edges against hair, trees and buildings at 100% zoom - halos give it away.
**Sky replacement** is a VFX/Fusion task (key + new sky + matching light) - flag it.

## 2. Background secondaries
Separate subject and background with a window/mask on the subject and **invert** (or
use the outside node `Alt+O`): darken, desaturate or blur the background for depth.

## 3. Depth Map (ResolveFX, Studio)
Generates a **depth matte** from the image (AI). Apply on a node, adjust near/far limits,
then use its output as a key (via the alpha / key output connected to another node's
key input) - grade by distance: haze in the distance, darken the far background, separate
foreground.
Check temporal stability across the shot (flicker in the depth estimation) - add
softness/ Matte finesse.

## 4. Relight (ResolveFX, Studio, Resolve 18.5+)
Adds virtual light sources (directional, point, spot) using a surface-normal map
estimated from the image; control position, colour, intensity and falloff. Use for a
subtle key on a face that was underlit, or to shape a background. Combine with a mask to
limit it. Small amounts look natural; large ones look plastic.

## 5. Performance
Depth Map and Relight are GPU-heavy - cache the node output (*Node Cache*) or use
render cache; analyse at full resolution before final render.

## Gotchas
- Qualifier-only sky keys catching faces and white shirts.
- Halos around trees and hair from hard key edges.
- Depth map flicker on moving shots.
- Overdone relight producing obvious CG light.

## Verify
- [ ] Sky isolated with window + key; edges checked at 100%.
- [ ] Background separation tracked across the shot.
- [ ] Depth map stable over time; used as a key correctly.
- [ ] Relight subtle and masked; heavy nodes cached.
