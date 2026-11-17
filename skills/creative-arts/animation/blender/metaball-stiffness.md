---
id: creative-arts.animation.blender.metaball-stiffness
name: metaball-stiffness
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, metaball-stiffness, metaball-radius, influence, blending]
level: practitioner
status: docs-checked
description: "Control how Blender metaballs blend: per-element Radius and Stiffness, the white (radius) and green (stiffness) rings, and tuning merge distance with Influence Threshold."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# metaball-stiffness

Goal: blobs that merge at the distance you want with the softness you want.

## Per-element settings (Edit mode > Properties > Data > Active Element)

- **Radius**: the physical size of the metaball (same as scaling it in Object Mode). Shown by the **white ring**; select the ring and scale it (`S`) to change the value.
- **Stiffness**: the influence range of this element, as opposed to Influence Threshold which is global to the family. With low stiffness the meta begins to deform from further away; with a high value the meta must be close to another to start merging. Shown by the **green ring**; select it and scale it to change the value. To be visible, Stiffness must be slightly larger than the Threshold. The property range is 0 to 10.
- **Negative**: switches the element's influence from positive (attraction, surfaces stretch toward each other) to negative (repel). A negative element is not visible in the 3D Viewport, only its rings are shown.
- **Hide**: hides the selected elements and also disables them from the metaball computation, which affects the final geometry.

## Tuning recipe

1. Pick a Threshold for the whole family first (it is global).
2. Drops that merge too early: raise their Stiffness (or raise the Threshold).
3. Long gooey necks between blobs: lower the Stiffness on those elements.
4. Check the family at Render resolution before finalising.

## Animation

Radius and Stiffness are properties and can be keyed (`I` over the field). Keying many elements inside one object is awkward; split elements into separate objects of the same family instead.

## Gotchas

- Stiffness is per element, Threshold is per family: tune both levels.
- A Stiffness at or below the Threshold gives an element with no visible surface.

## Verify

Move two elements apart slowly: they should separate at the intended distance.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Metaball Properties > Active Element) and 5.2 source range for Stiffness. Confirmed: Radius and Stiffness meanings, ring colours, visibility rule, Negative and Hide behaviour, Stiffness range 0-10. Corrected: the outer ring is the white Radius ring and the green ring is Stiffness (not "outer green-ish radius, inner red-ish stiffness"); the 0-10 range was right but the default of 2 and the suggested numeric recipes are not in the docs and were removed.
Method: documentation only; no commands were run.
