---
id: creative-arts.animation.blender.light-power-units
name: light-power-units
category: creative-arts
field: animation
product: blender
tags: [blender, lights, light-power-units, light-watts, light-power, exposure, lumens]
level: practitioner
status: docs-checked
description: "Convert real-world lamp ratings to Blender light power: watts as radiant power, the manual table of typical values, sun W/m2 and exposure balancing."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_light.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# light-power-units

## What the number means

- Point, Spot and Area **Power** is radiant power in watts (radiant flux): the energy radiated as visible light, NOT the electrical wattage printed on a bulb box.
- Sun **Strength** is irradiance in W/m2 (when Normalize is on).
- **Normalize** (on by default) keeps the total power the same when the light size or shape changes. **Exposure** multiplies the light intensity by 2^exposure.
- In a Cycles light node tree, the basic Light settings are applied on top of the light output node.

## Typical values from the manual

| Real world light | Power | Suggested type |
|---|---|---|
| Candle | 0.05 W | Point |
| 800 lm LED bulb | 2.1 W | Point |
| 1000 lm light bulb | 2.9 W | Point |
| 1500 lm PAR38 floodlight | 4 W | Area, Disk |
| 2500 lm fluorescent tube | 4.5 W | Area, Rectangle |
| 5000 lm car headlight | 22 W | Spot, size 125 degrees |

Sun Strength: clear sky 1000 W/m2, cloudy sky 500 W/m2, overcast sky 200 W/m2, moonlight 0.001 W/m2.

These values look much brighter or dimmer than expected because eyes adapt and a render engine does not; compensate with Exposure (Render > Film works on the data; Color Management > Exposure works on the view transform). Also set realistic light size and colour; light colour changes how bright a light looks (green seems brightest, blue darkest at equal power).

## Balancing

- Use exposure for global brightness instead of scaling every light.
- Light Groups (`creative-arts.animation.blender.light-groups`) let you rebalance after render.

## Gotchas

- Lights with a location have radiometric power in watts, which is sensitive to the scene unit scale (note in the Blender source).
- Pick one convention per project and document it; mixing gives inconsistent exposure.

## Verify

Render a grey card under the key light and check it reads mid-grey at the chosen exposure.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Radiant power meaning, Normalize, Exposure, the typical-value tables and exposure advice (Light Objects page); Film Exposure acts on the data versus Color Management exposure on the view transform (Cycles Film page); unit-scale sensitivity of watt lights (rna_light.cc comment). Removed unconfirmed lumen-per-watt conversions, sun/exposure figures and the glTF importer claim.

Method: documentation only; no commands were run.
