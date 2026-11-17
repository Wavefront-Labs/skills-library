---
id: creative-arts.graphic-design.adobe-photoshop.spot-healing-and-patch-tool
name: spot-healing-and-patch-tool
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photo-retouching, image-repair, spot-healing-brush, healing-brush, patch-tool, remove-tool, blemish-removal, dust-removal, non-destructive]
level: practitioner
status: draft
description: "Remove blemishes, dust and distractions non-destructively with Spot Healing, Healing Brush, Remove tool and Patch on an empty layer."
sources:
  - https://helpx.adobe.com/photoshop/using/retouching-repairing-images.html
  - https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spot healing, healing brush and patch tool

**Goal:** invisible removal of small to medium distractions without touching the original pixels.

## Set up non-destructively
Create an empty layer above the photo named `Heal`. On every healing tool set
**Sample: Current & Below** (Spot Healing: **Sample All Layers** checkbox). Your fixes
live on that layer and can be masked or deleted.

## Choose the tool
| Problem | Tool | Settings |
|---|---|---|
| Dust spots, small blemishes | **Spot Healing Brush (J)** | Type: Content-Aware; brush ~20% bigger than the spot |
| Wires, cables, people in background | **Remove tool (J)** | Paint over the whole object in one stroke; "Remove after each stroke" on |
| Blemish next to an edge or pattern | **Healing Brush** | Alt/Option+click to pick source with matching texture; Aligned on |
| Larger area of even texture (sky, wall) | **Patch tool** | Patch: Content-Aware or Normal; draw around the area, drag to clean source |
| Hard lines, repeated structure | Clone Stamp (see clone stamp skill) | Healing blends colour and would smear edges |

## Technique
- Work at 100% zoom; dab, don't scrub. Several small strokes beat one long one.
- Healing tools take texture from the source and colour/tone from the destination edges -
  they fail when the destination touches a contrasting edge (smudge appears). Move away
  from the edge or use Clone Stamp with a hard brush.
- Patch tool on an empty layer needs **Sample All Layers** (Content-Aware mode); Normal mode
  patch requires pixels on the active layer, so duplicate the photo layer for it.
- Repetition: if the same texture appears twice side by side, the eye spots it. Vary sources.

## Gotchas
- Healing near the canvas edge pulls in transparent/edge data; crop slightly or clone instead.
- Spot healing on a Smart Object directly is not allowed - use the empty layer method.
- Overdoing skin removes pores; see the frequency separation and dodge and burn skills for skin.

## Verify
- [ ] Toggle the `Heal` layer visibility: changes are invisible at 100% and print size.
- [ ] No repeated texture patterns, no smudged edges where an object meets a background.
