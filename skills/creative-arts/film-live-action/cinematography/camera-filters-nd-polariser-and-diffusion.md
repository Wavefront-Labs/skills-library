---
id: creative-arts.film-live-action.cinematography.camera-filters-nd-polariser-and-diffusion
name: camera-filters-nd-polariser-and-diffusion
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, camera-assistant, 1st-ac, camera-filters, filters, nd, nd-filters, neutral-density, ir-nd, irnd, internal-nd, variable-nd, polariser, polarizer, circular-polariser, linear-polariser, diffusion-filters, pro-mist, black-pro-mist, glimmerglass, hollywood-black-magic, pearlescent, soft-fx, classic-soft, streak-filter, grad-nd, graduated-filter, matte-box, filter-trays, 4x5-65, 6x6, filter-stacking, flare, halation, in-camera-look, nd-filter-use, nd-grades, ir-contamination, polariser-technique, reflection-control, pola-rotation, diffusion-choice, diffusion-strength, diffusion-test, matte-box-setup, filter-stacking-order, filter-trays-setup]
level: practitioner
status: draft
description: "Front-of-lens filters with intent: ND and IR-ND grades, polarisers for sky and reflections, diffusion families and strengths, grads, matte-box stacking, and what cannot be undone in post."
sources:
  - "American Cinematographer Manual, 10th ed. - Filters"
  - "https://tiffen.com/ (Tiffen diffusion and ND filter guides)"
  - "https://www.schneiderkreuznach.com/ (Schneider motion picture filters)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera filters: ND, polariser and diffusion

**Goal:** filters as decisions, not habits - exposure control that keeps the stop you
chose, polarisation that shapes skies and glass, and a diffusion look that is tested,
consistent across lenses and *meant*, because it is baked in forever.

## 1. ND - the exposure tool
- Grades in optical density: **0.3 = 1 stop, 0.6 = 2, 0.9 = 3, 1.2 = 4, 1.5 = 5, 1.8 = 6,
  2.1 = 7**. Exteriors at T2.8 / ISO 800 / 180° typically need ND 1.2-1.8 in sun.
- **IR-ND / IRND** (Tiffen IRND, Schneider Platinum IRND, Formatt Firecrest): digital
  sensors see far-red at heavy ND; plain ND turns blacks brown/magenta. Use IR-cut ND
  at 0.9 and above (or always, on cameras known to need it - RED, some Sony).
- **Internal ND** (ARRI Alexa 35/Mini LF, Sony Venice, FX series, Blackmagic): sensor-
  side, colour-neutral, saves a tray - prefer it; add glass ND beyond its range.
- **Variable ND**: two polarisers; fine for docs/run-and-gun, but cross-pattern at heavy
  settings and polarisation side-effects make it a bad choice for drama.
- **Grad ND** (hard/soft edge, 0.3-0.9): hold a sky against a landscape in a wide; align
  the edge to the horizon on a slider in the matte box; not for shots with the horizon
  crossing faces.

## 2. Polariser
- **Linear** vs **circular**: cine cameras don't need circular; linear is more effective.
  Rotate to effect: darkens blue sky at 90° from the sun, cuts reflections off glass,
  water, foliage, sweaty skin; deepens colour saturation.
- Costs ~1.5-2 stops; changes as the camera pans (sky gradient across a wide).
- Essential for car interiors (windscreen reflections) and shooting through windows.
- Don't stack with a variable ND; strange results.

## 3. Diffusion - the look
Families (Tiffen names; Schneider/others have equivalents):
- **Pro-Mist**: halation around highlights, lowered contrast, softened skin; the "classic
  film" cheat. **Black Pro-Mist** does the same with less lift in the blacks - the most
  used. Strengths 1/8, 1/4, 1/2, 1, 2 - **1/8 to 1/4** is modern taste; 1/2 reads as a look.
- **Glimmerglass**: fine sparkle, gentle softening, keeps contrast - subtle beauty.
- **Black Satin / Black Diffusion FX / Hollywood Black Magic**: softening and mild halation
  with blacks held; for faces on sharp modern lenses.
- **Classic Soft / Soft FX / Pearlescent**: skin softening with less highlight bloom.
- **Streak / Blue streak**: anamorphic-style flare lines on spherical lenses.
The strength needed **depends on focal length and sensor**: a 1/4 on a 25 mm looks like
a 1/8 on a 100 mm; wide shots show less effect. Many DPs scale strength down for wides
and up for close-ups to keep the *perceived* look constant - or hold one strength and
accept the variation. Test on the show's lenses and camera, on faces with a backlight,
and view through the show LUT. Diffusion is unrecoverable: a strong Pro-Mist cannot be
"un-done" for VFX or a clean delivery, and keying greenscreen through heavy diffusion
is a VFX problem - go light or none on VFX plates.

## 4. Matte box practice
- 4x5.65 is the standard tray size; 6.6x6.6 for wide lenses on large format; rotating
  stage for pola/grads. Note **stacking**: each extra glass surface adds flare and
  possible double images with bright sources - keep to 2-3 filters, put diffusion closest
  to the lens, ND outermost; ensure the lens hood/top flag kills direct sun on the glass.
- Clean front glass before each setup; dust on diffusion shows in backlight.
- Camera reports record filters per shot - the colourist and VFX need it.

## Gotchas
- Heavy ND without IR correction - brown blacks, mismatched between setups.
- Variable ND in drama; cross-polarisation and uneven darkness in wides.
- A diffusion strength decided on a wide and discovered on close-ups.
- Polariser rotated for the sky, then the camera pans and the sky gradient moves.
- Grad edge visible across an actor's forehead.

## Verify
- [ ] ND plan per setup holds the chosen stop; IR-ND used above 0.9.
- [ ] Diffusion family/strength tested on the show's lenses and recorded per lens.
- [ ] Filters logged on camera reports; VFX plates shot clean or with agreed minimal diffusion.
- [ ] Matte box stacked in order with the sun flagged off the glass.
