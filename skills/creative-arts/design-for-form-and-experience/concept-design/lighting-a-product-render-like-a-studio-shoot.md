---
id: creative-arts.design-for-form-and-experience.concept-design.lighting-a-product-render-like-a-studio-shoot
name: lighting-a-product-render-like-a-studio-shoot
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [product-rendering, presentation-render, studio-lighting, three-point-lighting, softbox, rim-light, keyshot, blender, area-lights]
level: practitioner
status: draft
description: "Light a product render like a studio photograph: key, fill and rim area lights, large soft sources for reflective surfaces, gradients on the backdrop and edge highlights."
sources:
  - "KeyShot Manual - Lighting, Area lights, Physical lights and Lighting presets (manual.keyshot.com)"
  - "Blender Manual - Light objects, Area light (docs.blender.org/manual)"
  - "Koos Eissen and Roselien Steur, Product Design Rendering (BIS), lighting chapter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Studio lighting for product renders

**Goal:** a render that describes the form (every surface reads with a different value) and
looks like it came from a professional product shoot.

## The setup
1. **Background first:** an infinite cyclorama (curved floor-to-wall plane) in mid grey.
   Light it separately so you control the gradient behind the product.
2. **Key light:** a large rectangular area light above and to one side, angled down about 30-45
   degrees. Size matters more than strength: a source as big as the product gives soft,
   readable gradients on curved surfaces.
3. **Fill:** a weaker, larger light (or a bounce card) opposite the key, about 1/4 to 1/2 key
   intensity, to keep shadow sides from going black.
4. **Rim / edge lights:** thin strip lights behind the product, high, to draw a bright line along
   the silhouette and separate it from the background.
5. **Reflection cards:** for glossy plastic, glass and metal, the light sources are what you see
   reflected. Place long thin planes (emissive or white) where you want a highlight streak on the
   surface. Metal shows the environment, not the light, so you design the reflections.

## Tool notes
- KeyShot: build lights with Area Light materials applied to planes or the HDRI Editor (pins on
  an HDRI); turn on Lighting > Ground shadows and occlusion; use Interior mode only for enclosed scenes.
- Blender (Cycles): Area lights with Shape Rectangle, Spread under 90 degrees to focus; enable
  Filmic/AgX view transform for a photographic range.

## Gotchas
- One small point light = hard shadows and blown highlights; nearly never right for products.
- Pure black backgrounds hide dark products; use a gradient.
- Do not let the brightest highlight sit on an unimportant detail.

## Verify
Convert the render to greyscale: top, front and side faces each read as clearly different
values, the silhouette separates from the background all round, and no area clips to pure white.
