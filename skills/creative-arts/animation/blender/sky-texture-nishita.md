---
id: creative-arts.animation.blender.sky-texture-nishita
name: sky-texture-nishita
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, sky-texture, sky-texture-nishita, nishita, atmosphere]
level: practitioner
status: docs-checked
description: "Light outdoor scenes with Blender's physical Sky Texture: sun elevation and rotation, sun disc, altitude, air, dust and ozone, and EEVEE caveats."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/sky.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# sky-texture-nishita

## Setup

World: **Sky Texture** -> Background -> World Output. The node generates a procedural sky.

## Sky Type

- **Single Scattering**: improved version of the 1993 Nishita model, accounting for single bounces in the atmosphere. Legacy; may be removed in a future version.
- **Multiple Scattering**: based on work by Fernando Garcia Linan; the most accurate, since it accounts for multiple bounces.
- **Preetham** (1999) and **Hosek/Wilkie** (2012): legacy, to be removed in a future version. These use **Sun Direction**, **Turbidity** (2 arctic, 3 clear sky, 6 warm/moist day, 10 hazy day) and **Ground Albedo** instead of the Single/Multiple Scattering controls below.

## Settings (Single and Multiple Scattering)

- **Sun Disc** (Cycles only), **Sun Size** (angular diameter in degrees), **Sun Intensity** (multiplier for sun disc lighting).
- **Sun Elevation** (rotation of the sun from the horizon, degrees) and **Sun Rotation** (rotation around the zenith, degrees).
- **Altitude**: distance from sea level to the camera (0 for a beach, about 10 km for an aeroplane cockpit).
- **Air** (density of air molecules; 1 is roughly urban city air, 0 none), **Aerosols** (water droplets and aerosol particles; 1 roughly urban, 0 none), **Ozone** (makes the sky bluer; 1 roughly urban, 0 none).

## Brightness

The Single and Multiple Scattering skies are very bright by default (hence accurate). Lower the scene Exposure in Properties > Color Management > Exposure to compensate.

## Gotchas

- Sun Disc lighting is Cycles only; in EEVEE use a Sun light for the sun's shadows.
- Keep Sun Elevation, Sun Rotation and any Sun light direction consistent by hand or with drivers.

## Verify

Lower the Sun Elevation toward the horizon: the sky turns orange and warmer; a high sun gives a deep blue sky and neutral light.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/sky: Sky Type list and legacy status, Preetham/Hosek-Wilkie controls and Turbidity values, Sun Disc Cycles only, Sun Size, Intensity, Elevation, Rotation, Altitude, Air, Aerosols, Ozone and the exposure note. Removed the '2.90' and '5.0 reworked' version claims, the 0.545 degree sun size, the Background Strength and AgX exposure numbers, the Sun Position extension, the below-horizon claim and the EEVEE world sun threshold remark; the draft's 'Dust' control is named Aerosols in the manual.

Method: documentation only; no commands were run.
