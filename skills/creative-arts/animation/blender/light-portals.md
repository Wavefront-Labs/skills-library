---
id: creative-arts.animation.blender.light-portals
name: light-portals
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-portals, light-portal, interior-lighting, cycles]
level: practitioner
status: docs-checked
description: "Speed up Cycles interior renders with light portals: the area light Portal option, placement in openings, and when portals help or hurt."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/intern/cycles/blender/addon/ui.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# light-portals

## What they do

A portal is an area light with **Portal** enabled (Cycles). Area lights can function as light portals to help sample the environment light and significantly reduce noise in interior scenes.

## Setup

1. Add an Area light shaped to the window or opening.
2. Place it in windows, door openings and any place where light will enter the interior.
3. Light properties > Settings > **Portal** checked (Cycles, Area lights only).
4. One portal per opening.

With Portal on, the light's Max Bounces, Cast Shadow and Multiple Importance settings and its Nodes panel are not shown.

## When they help / hurt

- Help: interiors lit through openings by the world (HDRI or sky).
- Rendering with portals is usually slower per sample, but it converges more quickly, so fewer samples are required.
- Outdoor scenes: most rays do not bounce much and fly off into the sky, so portals are not helpful.

## Gotchas

- Portal is a Cycles light setting; the 5.2 EEVEE light panel has no Portal option.

## Verify

Same samples with/without portals: the noise in the room drops noticeably with portals.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Portal purpose, placement, performance trade-off and outdoor note (Cycles light settings page); Portal checkbox only for Area lights in the Cycles Settings panel and the hidden settings while Portal is on (ui.py); no Portal in the EEVEE light panel (properties_data_light.py). Removed unsupported facing-direction, sun-light and glass-placement claims.

Method: documentation only; no commands were run.
