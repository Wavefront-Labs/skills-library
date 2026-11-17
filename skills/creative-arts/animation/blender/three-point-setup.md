---
id: creative-arts.animation.blender.three-point-setup
name: three-point-setup
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, three-point, three-point-setup, key-fill-rim, key-light]
level: practitioner
status: docs-checked
description: "Build a three-point lighting rig in Blender: key, fill and rim area lights, ratios in stops via Power or Exposure, Track To aiming, Light Groups and a False Color exposure check."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/track_to.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# three-point-setup

The placement values here are lighting practice, not Blender rules; Blender facts are listed in Checked.

## Placement (subject facing camera)

- **Key**: area light to one side of the camera and above the subject's eye line; larger area lights give softer shadows.
- **Fill**: opposite side, near camera height, larger and dimmer; or a bounce card (white plane) instead of a light.
- **Rim / back**: behind the subject, opposite the key, high; small and strong to separate the silhouette from the background.
- Optional background or kicker light.

## Ratios

Key to fill ratio sets mood: 2:1 is one stop of difference, 4:1 two stops, 8:1 three stops. In Blender, either halve the fill **Power** for each stop at equal distance, or use the light's **Exposure** (intensity is multiplied by 2^exposure, so each exposure step is one stop). Area light **Normalize** is on by default, so changing the light's size keeps its total power; with Normalize off a bigger light emits more.

## Rig

1. Empty `look_target` at the subject's head.
2. Give each area light a **Track To** constraint targeting the empty. Choose a Track Axis that matches the way the light points and an Up axis that is different from it (the constraint stops working if both are the same). Lights then stay aimed when moved.
3. Parent the lights to an empty to rotate the whole rig around the subject.
4. Name lights `KEY`, `FILL`, `RIM`. In Cycles, **Light Groups** (View Layer) give separate Combined passes lit by chosen lights, to rebalance in compositing.

## Checks

- Solo each light (hide the others) and render to see its contribution.
- View Transform **False Color** shows a heat map of image intensities to help judge exposure.
- The Area light **Spread** setting controls how widely the light fans out: smaller values give sharper, gridded-softbox light, larger values softer shadows (Cycles).

## Gotchas

- World lighting adds hidden fill; lower the world strength or use black while building a controlled rig.

## Verify

Render each light solo, then combined; the ratio between lit and shadow side of the face should match the target.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/lights/light_object.rst (Exposure 2^exposure, Normalize, Power, area shapes), render/cycles/light_settings.rst (Spread, Light Groups reference), animation/constraints/tracking/track_to.rst (Track Axis, Up must differ), render/layers/passes.rst (Light Groups, Cycles only), color_management/displays_views.rst (False Color). Removed: specific angles and sizes, Track -Z/Up Y values, catchlight and Ray Visibility Glossy claims for lights, the "mid-to-upper grey" skin target, and 1-2x rim power claim. Method: documentation only; no commands were run.
