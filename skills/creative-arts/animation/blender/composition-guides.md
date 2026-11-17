---
id: creative-arts.animation.blender.composition-guides
name: composition-guides
category: creative-arts
field: animation
product: blender
tags: [blender, camera, composition-guides, passepartout, safe-areas, rule-of-thirds]
level: practitioner
status: docs-checked
description: "Frame shots in Blender camera view: passepartout opacity, rule-of-thirds/golden/diagonal guides, title/action safe areas and center-cut safe areas."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# composition-guides

Goal: framing guides in the viewport that match how the shot will be delivered.

## Camera Data > Viewport Display
- **Passepartout** + opacity slider: darkens the area outside the camera's field of view (fully opaque also speeds up rendering inside the frame).
- **Composition Guides**: Thirds, Center (Center, Diagonal), Golden (Ratio, Triangle A/B), Harmony (Triangle A/B), plus a guide **Color** with alpha.
- **Show Name**, **Size** (display only), **Show Limits** (clip range and focus), **Show Mist**, **Show Sensor** (dotted frame).

## Safe Areas
Safe Areas panel on the camera: **Title Safe** (graphics) and **Action Safe** margins X/Y, shared with the sequencer; **Center-Cut Safe Areas** for content seen on other aspect ratios (default 4:3 inside 16:9). Blender defaults follow the EBU standard; each country sets its own broadcast standard, so use the broadcaster's specified values.

## Practice
- Lock camera to view (see lock-camera-to-view) + thirds guides for quick framing.
- Keep text/titles in title safe; key action in action safe for TV/social crops.

## Gotchas
- Guides are viewport overlays on the camera view (the manual describes them as overlays that help framing).
- Set the final resolution aspect before composing, since the camera frame follows it.

## Verify
Camera view: subject eyes on the upper third line, titles inside the title-safe box, at the final aspect ratio.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Passepartout, Composition Guides names, Show Name/Limits/Mist/Sensor, Safe Areas, Center-Cut, EBU defaults note). Removed unconfirmed margin presets, EBU R 95 percentages and "Harmonious" naming (manual says Harmony).
Method: documentation only; no commands were run.
