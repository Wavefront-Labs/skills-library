---
id: creative-arts.film-live-action.cinematography.lighting-fixtures-modifiers-and-the-lighting-plan
name: lighting-fixtures-modifiers-and-the-lighting-plan
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, gaffer, key-grip, lighting-fixtures, fixtures, hmi, led-fixtures, led-panels, tungsten, fresnel, par, open-face, skypanel, aputure, arri-m18, kino-flo, tube-lights, space-light, book-light, modifiers, diffusion, softbox, lantern, china-ball, frames, 4x4, 8x8, 12x12, silk, grid-cloth, muslin, ultrabounce, bounce, flags, floppies, nets, scrims, cutters, c-stand, lighting-diagram, lighting-plan, lighting-plot, power-plan, amps, distro, generator, dmx, wireless-dmx, pre-rig, bounce-lighting, diffusion-frames, soft-light-rigs, grip-control, flagging, cutting-light, lighting-plot-drawing, plot-symbols, power-distribution-plan, negative-fill-technique, subtractive-lighting, flagging-fill, source-size, softness-of-light, wrap]
level: practitioner
status: draft
description: "Pick fixtures and modifiers - HMI, LED, tungsten, tubes, book lights, frames, flags, nets - size them to stop and distance, and draw the lighting plan with power so the gaffer can pre-rig."
sources:
  - "American Cinematographer Manual, 10th ed. - Lighting; Lighting equipment; Electrical"
  - "https://www.arri.com/en/lighting (ARRI photometric data)"
  - "https://www.aputure.com/ (Aputure photometric data)"
  - "Harry Box, Set Lighting Technician's Handbook"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lighting fixtures, modifiers and the lighting plan

**Goal:** choose the smallest kit that produces the planned light - right quality,
colour, level and control - and communicate it as a plan the gaffer and key grip can
rig before you arrive.

## 1. Fixture families (what each is for)
| Family | Examples | Use | Notes |
|---|---|---|---|
| **HMI daylight** | ARRI M18/M40/M90, 1.2k-18k | Sun through windows, big exteriors fill, hard daylight | Most output per watt for hard daylight; needs ballast, warm-up, flicker-free ballast at high frame rates |
| **LED panels / soft** | SkyPanel S60/S360, Aputure Nova, Litepanels Gemini | Soft key/fill, colour effects, fast setup | Tunable K and gels; check TLCI/SSI; output drops vs HMI for hard throw |
| **LED point source** | Aputure 600d/1200d, ARRI Orbiter, Creamsource Vortex | Hard or bounced key, through diffusion, bowens modifiers | Replacing tungsten/HMI for most mid-size work; battery options |
| **Tungsten** | 1k/2k/5k Fresnels, 650 "tweenie", 300, Dedolights | Warm practicals look, hard controllable beam, dimmable | 3200 K, hot, power-hungry; still the reference for skin |
| **Tubes** | Astera Titan/Helios, Quasar, Kino Flo | Thin soft sources, hide in sets, car interiors, colour FX | Battery, wireless DMX |
| **Big soft** | Space lights, balloon lights, 20x20 book lights | Night exteriors, large interiors ambient | Rig from above; crane/condor |
| **Practicals** | Lamps, bulbs (Philips Hue / Astera bulbs) | In-frame motivation | Dimmers, bulb swaps, ND gel on shades |

## 2. Modifiers: quality is size and distance
Softness = apparent size of the source from the subject. A 4x4 frame at 1 m is softer
than a 12x12 at 10 m. Tools:
- **Diffusion**: 216 (heavy), 250 (half), 251 (quarter), Opal, grid cloth (full/half/quarter),
  silk (directional), muslin (bleached/unbleached - warm). Frames: 4x4, 6x6, 8x8, 12x12, 20x20.
- **Book light**: bounce into a white/Ultrabounce then through diffusion - the softest
  controllable key; needs floor space.
- **Bounce**: beadboard/foam core, Ultrabounce, muslin, griff - turns any hard source soft.
- **Negative fill**: black floppies, duvetyne, solids - the most under-used tool;
  shape faces by *removing* ambient.
- **Control**: flags/cutters (hard edges), nets (single/double, 1/2 and 1 stop reduction
  with no colour shift), scrims (metal, in the fixture), barn doors, snoots, egg crates /
  honeycombs on soft sources to stop spill, topper flags to keep light off backgrounds.
- **Softboxes / lanterns / China balls** for quick omnidirectional soft; Chimera on Fresnels.

## 3. Size the light to the stop
Use the manufacturer's **photometric tables** (lux/fc at distance, beam angle) or an app
(Aputure Sidus, ARRI Photometrics). Rule of thumb: to shoot T2.8 at ISO 800, 180°,
you need ~ 100 lux on the key; T5.6 needs ~400 lux. Each diffusion layer costs 1-2
stops, bounce costs 2-3 stops, distance costs by inverse square (double distance =
-2 stops). Work backwards from the intended stop and distance to the fixture wattage,
then add 1 stop margin.

## 4. The lighting plan
Per set/scene, an overhead (Shot Designer, Vectorworks, or a sketch) showing: camera
positions and lenses; each fixture with type, wattage, diffusion/gel, stand or rig;
frames, flags and bounce; practicals; the direction of the "sun"; power draw per circuit.
Add a notes box: colour plan, stop, K, special rigs (condor, Menace arm), sequence for
the day. The gaffer turns this into a **power plan** (amps = watts / volts; 20 A circuits
on a 120 V location carry ~1,800 W safely; a 2k tungsten needs its own) and a distro
plan (generator/tie-in, cable runs, where the dimmer/DMX desk sits). Share before the
tech scout; refine on it.

## 5. Efficiency habits
- Pre-rig the big sources (through windows, overheads) before unit call.
- Light the space, not the shot: an ambient base plus a movable key covers most coverage.
- Wireless DMX (Astera, Sidus, Lumen Radio) lets you adjust from the monitor; keep a
  cue sheet of levels per setup for matching.
- Battery LEDs for pickups and insert days instead of running a generator.

## Gotchas
- Soft source too far away - it becomes hard and dim.
- Spill from a big soft key flattening the background; no egg crate or topper.
- LED at 1% dimming flickering or shifting colour; use fixtures with good low-end dimming.
- HMI without a flicker-free ballast at high frame rates.
- Power plan missing; breakers trip at the first take.

## Verify
- [ ] Each scene has an overhead with fixtures, modifiers, gels, camera, and the sun direction.
- [ ] Fixtures sized from photometrics to hit the stop with margin.
- [ ] Power plan per circuit signed off by the gaffer; generator/distro placed on the tech scout.
- [ ] Levels/cues recorded per setup for matching across the scene.
