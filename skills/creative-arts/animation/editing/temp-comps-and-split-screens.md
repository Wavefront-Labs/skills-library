---
id: creative-arts.animation.editing.temp-comps-and-split-screens
name: temp-comps-and-split-screens
category: creative-arts
field: animation
product: editing
tags: [temp-comp, split-screen, edit-effects, crop, picture-in-picture, temp-vfx, premiere-pro, resolve, avid, editorial]
level: practitioner
status: draft
description: "Build temp comps and split screens in the cut to combine takes, preview a missing element or pitch a shot change, and document them for the department that does it for real."
sources:
  - https://helpx.adobe.com/premiere-pro/using/compositing-alpha-channels-adjusting-clip.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.focalpress.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Temp comps and split screens in the cut

**Goal:** show the director something that does not exist yet (a character from another take, a missing prop, a
reframed shot) cheaply, and make sure it becomes a proper request downstream.

## Common temp comps

| Temp | How in the NLE | Real fix downstream |
|---|---|---|
| Split screen: left half take A, right half take B | two clips stacked, Crop effect on the top one (Premiere *Crop*, Resolve Inspector > Cropping) with 10-20 px feather | animation re-renders a single shot combining both performances |
| Reframe/push-in | Scale/Position keyframes on the clip | layout changes the camera, see `creative-arts.animation.editing.time-remap-speed-changes` for timing equivalents |
| Character pulled from another shot | render with alpha placed over the plate (blend mode Normal; ProRes 4444 with alpha) | compositing/lighting renders the real element |
| Flop | Horizontal Flip | layout re-stages; flopped characters break model asymmetry (hair parts, logos) |
| Speed ramp | time remapping | animation retimes |

## Rules

1. **Label every temp:** a burn-in or a red `TEMP` title on V-top so nobody mistakes it for approved work in a
   screening.
2. **Log it:** add a marker with the shot code and the intended fix; export the marker list with the turnover so
   layout or comp receives a concrete note (see `creative-arts.animation.editorial.editorial-change-lists`).
3. **Keep source media at full res:** a scale-up above 110% shows soft line art; flag it as needing a layout change.
4. Temp comps are not turned over as effects; the turnover lists the base clip, and the change is a written note.

## Gotchas

- Premultiplied renders composited as straight alpha give dark fringes on line art; set the alpha interpretation
  (see `creative-arts.animation.color.premultiplied-alpha`).
- Split screens hide continuity errors at the seam: watch hands and props crossing the split line.

## Verify

The director-approved temp has a matching ticket or change-list entry for every comp, and the screener shows the
`TEMP` label on each one.
