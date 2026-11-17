---
id: creative-arts.animation.blender.eevee-world-sun-extraction
name: eevee-world-sun-extraction
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-world-lighting, sun-extraction, world-lighting, hdri]
level: practitioner
status: docs-checked
description: "Light EEVEE scenes from the world: HDRI sun extraction threshold, angle and shadow, world light probe resolution, and how EEVEE differs from Cycles here."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/world_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-world-sun-extraction

Goal: proper sun shadows and ambient light from an HDRI in EEVEE.

## How EEVEE treats the world

The world lighting is stored in an internal light probe, which makes it less precise than in Cycles. EEVEE considers world lighting indirect lighting, whereas Cycles considers it direct.

## World > Light Probe > Sun

EEVEE can separate intense light sources (for example the sun in an outdoor HDRI) and replace them with a sun light, which increases lighting quality because the internal probes alone cannot reproduce such lighting precisely.

- **Threshold**: if non-zero, the maximum world contribution recorded in the world light probe; the excess is converted to a sun light, reducing light bleeding from very bright sources. 0 disables the feature, and all lighting stays in the internal probe.
- **Angle**: angular diameter of the extracted sun as seen from Earth.
- **Use Shadow**: enables shadow casting on the extracted sun. The shadow properties are the same as for a sun light object (see the EEVEE light settings: Jitter, Overblur, Filter, Resolution Limit).

## World light probe resolution

World settings > Light Probe > **Resolution** is the resolution used to store world light, equivalent to the resolution of light probe spheres.

## Matching Cycles

- Cycles treats the world as direct light and samples it directly; in EEVEE use sun extraction (or a manual sun light) for sharp sun shadows.
- Indirect bounce in EEVEE comes from light probe volumes (see eevee-volume-probe), raytracing or Fast GI.

## Gotchas

- Overcast HDRIs have no clear sun: leave Threshold at 0 or high enough that nothing is extracted.
- If you add a manual sun light that matches the HDRI sun, avoid double sunlight by turning extraction off.
- Recheck the extracted sun direction after rotating the world mapping.

## Verify

Render a character outdoors with a sunny HDRI: the shadow should point away from the sun position visible in the HDRI.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE World settings, Light settings). Confirmed: Threshold, Angle, Use Shadow, 0 disables, probe resolution, indirect-vs-direct difference. Corrected: the panel is World > Light Probe (Sun), not Render Properties; probe resolution is in World settings. Removed unconfirmed: version gate, guidance to lower Threshold until the disc is captured, rotation behaviour.
Method: documentation only; no commands were run.
