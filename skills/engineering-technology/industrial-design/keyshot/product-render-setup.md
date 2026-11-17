---
id: engineering-technology.industrial-design.keyshot.product-render-setup
name: product-render-setup
category: engineering-technology
field: industrial-design
product: keyshot
tags: [industrial-design, keyshot, rendering, product-rendering, product-visualisation, product-visualization, hdri, studio-lighting, materials, plastic-advanced, metallic-paint, anisotropic, cmf-variants, model-sets, studios, denoise, render-settings, area-light, ground-shadows, camera, focal-length, clown-pass, render-passes, presentation-renders, design-review]
level: practitioner
status: draft
description: "KeyShot product renders: material types and parameters, HDRI studio lighting, render modes and sample settings, and CMF variant sets for design reviews."
sources: ["Luxion, KeyShot User Manual", "Pharr, Jakob & Humphreys, Physically Based Rendering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Product render setup in KeyShot — renders that support a design decision

**Goal:** produce consistent, believable renders that show form, material and
colour honestly, and let a review compare variants side by side.

## 1. Prepare the import
- Export from CAD with sensible tessellation: fine enough that silhouettes are not
  faceted (adjust in the import or by re-tessellating in a CAD plugin).
- Keep parts split by **material**, not by assembly hierarchy; one part with two
  finishes needs to be two bodies or a texture/label.
- Import **in mm with the correct up axis** so physical lights and depth of field
  behave at real scale.
- Use Rounded Edges (a geometry/bump effect in recent versions) to add a ~0.1-0.3 mm
  edge highlight to sharp CAD edges; real moulded parts are never knife-sharp.

## 2. Choose the right material type
| Real material | KeyShot type | Key settings |
|---|---|---|
| Moulded gloss/matte plastic | Plastic or Plastic (Advanced) | Roughness 0 (gloss) to ~0.2-0.4 (textured look); add bump texture for moulded grain |
| Painted part | Paint / Metallic Paint | base colour, metal flake size and visibility, clearcoat |
| Bead-blasted or machined metal | Metal | roughness for blast; colour sets the metal |
| Brushed aluminium | Anisotropic | roughness X vs Y, set mapping so grain follows the brushing direction |
| Clear lenses / windows | Glass or Solid Glass | refractive index ~1.49 (PMMA), ~1.58 (PC); Solid Glass needs real thickness |
| Light pipes, frosted diffusers | Translucent / Translucent (Advanced) | subsurface colour and transmission |
| LEDs, screens | Emissive | power; image texture for UI |
| Rubber, TPE | Plastic (Advanced) with high roughness | low specular |

Map textures with **box or UV mapping** at real scale; check scale against a known
dimension. Use the Multi-Material feature to hold colour variants on the same part.

## 3. Light it like a studio
1. Start with a neutral studio **HDRI** (soft boxes on grey). Set Brightness so the
   brightest face is just under clipping; rotate the environment until the main
   highlight runs along the key form line.
2. Use the **HDRI editor** to add pins (rectangular soft boxes) for a rim light on the
   silhouette and a strip light down a long face. Pin hardness controls edge sharpness
   of the reflection.
3. Add physical lights (area light materials applied to a plane, point or spot lights)
   only for local accents such as lighting into a recess.
4. Use a backplate or flat colour background, and turn on **ground shadows** and
   **ground occlusion**; ground reflections only if the story is a glossy table.
5. Choose the lighting preset to suit: product-oriented presets for single objects,
   interior presets when light must bounce through enclosed geometry; raise ray bounces
   for glass and light pipes.

## 4. Camera
- Focal length **50-100 mm equivalent** for hero shots; wide lenses distort products.
- Lock a named camera per view so every variant uses the identical angle.
- Use orthographic views for CMF sheets and side-by-side comparisons.
- Depth of field: subtle, and only when it supports the point.

## 5. Render output
- Real-time is for setup; produce finals in the Render dialog with **Max samples** (e.g.
  128-512 depending on glass and caustics) or **Max time**, plus denoise. Check denoise
  has not smeared texture.
- Resolution: ~2x the display size; 300 dpi at print size for boards.
- Render **passes/layers** (e.g. clown/object mask, reflection, shadow) for compositing.
- GPU mode is faster on a supported graphics card; confirm CPU and GPU output match
  before mixing them in one set.

## 6. Variants for review
Use **Model Sets** (geometry options) and **Studios** (saved combinations of model set,
camera, environment and materials) so each variant is one click and lighting stays fixed.
Batch them with the render queue.

## Gotchas
- Too-dark or too-bright HDRI makes every colour look wrong; calibrate with a grey
  reference sphere of ~18% grey.
- Colours on screen are not physical colour standards; CMF approval needs physical
  plaques (see cmf-design).
- Glass with no thickness renders as a soap bubble; model real wall thickness.
- Changing environment between variants makes reviewers compare lighting, not designs.
- Inverted normals from CAD show black or see-through faces; flip or re-export.

## Verify
- [ ] Every part has a material type that matches its real process and finish.
- [ ] Highlights run along key form lines and show no faceting.
- [ ] All variants share one camera and environment (Studios).
- [ ] Texture scale checked against a known dimension.
- [ ] Final output is noise-free at the target resolution, with passes saved.
