---
id: architecture-construction.architecture.architectural-visualisation.exterior-render-composition
name: exterior-render-composition
category: architecture-construction
field: architecture
product: architectural-visualisation
tags: [architectural-visualisation, archviz, arch-viz, rendering, exterior-render, cgi, photorealistic, camera, two-point-perspective, vertical-lines, shift-lens, tilt-shift, focal-length, eye-level, composition, rule-of-thirds, lighting, golden-hour, hdri, sun-and-sky, materials, pbr, entourage, people-cutouts, scale-figures, post-production, photoshop, d5-render, enscape, lumion, twinmotion, v-ray, corona, verified-views, honesty]
level: practitioner
status: draft
description: "Compose an exterior architectural render that sells the design honestly: camera height and vertical correction, focal length, light and time of day, materials, entourage scale and post-production."
sources: ["Common archviz practice (V-Ray, Corona, Enscape, D5, Lumion documentation on cameras and lighting)", "Landscape Institute TGN 06/19 on visual representation (for verified views)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composing an exterior architectural render

**Goal:** a still image that communicates the building's idea at a glance, reads as
believable, and doesn't mislead the client or a planning committee. Most weak renders
fail on the camera and the light, not the software.

## 1. Decide the story first
One image, one message: the entrance sequence, the relationship to the street, the
roof form, the material. Write it down. It decides the viewpoint, the time of day and
what to leave dark.

## 2. Camera
- **Eye level ~1.5–1.7 m** for street views. Higher viewpoints (drone, upper window) are
  for context or massing, not for selling the experience.
- **Vertical lines vertical:** use two-point perspective. In the renderer enable
  vertical correction / *2-point perspective* / camera *shift* (the tilt-shift lens
  equivalent) rather than tilting the camera up. Converging verticals make buildings
  look like they're falling backwards.
- **Focal length:** roughly 24–35 mm (full-frame equivalent) for most exteriors.
  Ultra-wide (<20 mm) stretches the foreground and exaggerates size — clients notice later
  when the built result feels smaller.
- Compose with thirds/leading lines: the street edge, a path, a shadow line leading to
  the entrance. Leave the subject breathing room; avoid cropping the roof edge.
- Foreground layer (tree branch, planting, a kerb) adds depth — keep it out of focus or
  dark so it frames rather than competes.

## 3. Light
- **Time of day:** low sun (morning/late afternoon) rakes across façades, revealing
  texture and depth. Midday overhead sun flattens everything.
- Pick the sun direction so the main façade is lit and the secondary face falls into
  shade — light/shade contrast defines the form.
- HDRI sky for believable ambient light; match HDRI sun direction to the physical sun.
- Dusk shots: interior lights on, sky still holding blue — the classic "the building
  is alive" image. Balance interior exposure so it doesn't blow out.

## 4. Materials
- Use physically based (PBR) materials with **real-world scale** — brick coursing at
  real size is the most frequent scale giveaway.
- Add imperfection: roughness variation, slight colour variation between panels, edge
  wear on concrete. Perfect CG uniformity reads as fake.
- Glass: reflection is the main read; set what it reflects (sky, trees, context).

## 5. Entourage and context
- People at **correct scale and perspective** (eye level at camera height means heads of
  standing people roughly on the horizon line); match their lighting direction.
- Fewer, purposeful people: walking toward the entrance, sitting where the design
  intends.
- Context buildings neutral, not distracting. Trees in season consistent with the light.

## 6. Post-production
Render passes (beauty, reflection, light-select, Z-depth, object ID / cryptomatte)
allow targeted grading. Typical steps: exposure/contrast, colour balance, atmospheric
depth, subtle vignette, sharpening. Keep it subtle.

## Honesty
Renders for planning must not misrepresent scale, visibility or landscaping maturity.
Where a view is used to assess impact, produce **verified views** (camera matched to a
surveyed photograph with known lens) per the relevant guidance. Mark artistic images as
"illustrative".

## Gotchas
- Trees at 20-year maturity hide the building — and mislead about the first years.
- Over-saturated skies and perpetual sunsets date fast and reduce trust.
- Renderer-specific settings differ (Enscape vs V-Ray vs Corona); *the principles hold,
  menu names vary.*

## Verify
- [ ] Verticals are vertical; focal length ≥ ~24 mm equivalent unless justified.
- [ ] The single message of the image is obvious within 3 seconds.
- [ ] Material textures are at real-world scale.
- [ ] People sit on the horizon line consistent with camera height.
- [ ] Planning images are either verified or labelled illustrative.
