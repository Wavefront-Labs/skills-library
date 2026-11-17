---
id: creative-arts.animation.texturing.textures-maps
name: textures-maps
category: creative-arts
field: animation
product: texturing
tags: [texturing, cel, toon, uv, maps, mask, decal, hand-painted, procedural, baking, resolution, screen-content, grime, wear]
level: advanced
status: draft
description: "Texture maps for a cel show: when flat fills aren't enough, UV strategy for toon, maps that don't fight the ramp, decals, baking, resolution discipline."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Texture maps for a cel-shaded series

**Context:** this show is **mostly flat material fills + the toon ramp**
(`../blender/cel-shading.md`). Most surfaces need **no texture at all** — a single
base color feeding the `NPR_Toon` chain. Texturing here is the exception, not the
rule. The skill is knowing *when* a map earns its place, and painting it so it
**reinforces the cel look instead of fighting it**.

---

## 1. When you actually need a map

Only when flat color can't carry the idea. The legitimate cases:

- **Screen / display content** — Chip's CRT face, UI panels, signage. This is the
  big one: animated or state-switched emissive imagery.
- **Decals / markings** — logos, numbers, face markings, insignia, stickers. Sharp
  graphic shapes that would be absurd to model.
- **Grime / wear / damage** — a *masked* break in the flat fill (a scuff band, oil
  streak, rust patch) to say "used." Used sparingly; cel grime is graphic shapes,
  not photoreal noise.
- **Pattern** — fabric print, tartan, camo — a repeating graphic the ramp then
  shades as one surface.

If you can't name which of these a map is for, don't make it — use a flat fill and
a second material slot instead.

---

## 2. The rule that governs everything: maps must not fight the ramp

The toon ramp quantizes **lighting** into bands. A texture that carries its own
light/shadow (painted highlights, baked AO, photo grunge with embedded shadow)
collides with the ramp — you get double shading, muddy bands, and the flat read
dies. So:

- **Texture the *albedo/fill color only*.** Feed the map into the **Base Color**
  input of `NPR_Toon` (the color the ramp multiplies), never into a lighting path.
  Let the ramp do 100% of the light.
- **No baked AO, no painted highlights/shadows in the color map.** Flat local color
  only. If you want a form shadow, it comes from the ramp + light, not the texture.
- **Keep value range tight and flat.** A grime map should shift *hue/local color*
  in patches, not plunge value — a near-black grunge patch will read as a hole once
  the ramp darkens it further.
- **Masks, not gradients.** Wear/decals as hard-edged masks (think stencil) match
  the hard-banded look; soft photo gradients look foreign next to crisp cel fills.

---

## 3. UV strategy for toon

Because most color is flat, UVs are *light* work — but do them cleanly for the maps
you do need:

- **Seam placement:** hide seams where the inverted-hull outline or a natural form
  break already sits (silhouette edges, under the jaw, inside limbs). Seams are
  invisible on flat fills anyway, so prioritize *un-distorted* islands over minimal
  seams.
- **Relaxed, low-distortion unwrap** for anything painted (faces, screens, decal
  areas). Flat-fill-only parts can get a trivial projection or even share one tiny
  UV patch — don't waste texel space on surfaces that are one solid color.
- **Decals:** don't bake a decal into a full-body map. Use a **separate decal
  mesh/plane** (`Shrinkwrap` to the surface) with its own small texture + alpha, or
  Blender's decal workflow. Keeps the base map clean and lets you move/retire the
  decal per shot.
- **Screen content** (Chip): a dedicated flat plane with its own 1:1 UV, its own
  emissive material, separate from the head mesh — so viseme/expression frames swap
  without touching the body texture.
- **Pack by material role**, and keep a consistent **texel density** across a
  character so the (few) maps sample evenly.

---

## 4. Hand-painted vs procedural

- **Hand-painted (default for hero graphic shapes):** decals, face markings, screen
  art, deliberate wear placement. Paint in a raster editor or Blender Texture Paint
  directly on the UV/mesh. Gives art-directed, on-model graphic shapes — the cel
  look is a *designed* image, so painting beats noise.
- **Procedural (for subtle, repeatable surface variation):** fabric weave, uniform
  grime, tiling patterns. Author as a Blender shader node network (`Noise`,
  `Voronoi`, `Musgrave`, `Brick`) feeding a `ColorRamp` set to **CONSTANT or very
  few stops** so the procedural result is *already quantized* and matches the cel
  bands. A smooth procedural gradient will fight the toon ramp — always step it.
- **Hybrid:** procedural base variation + a hand-painted mask to place it only where
  it reads (a grime streak under a vent, not uniformly).

Keep procedural seeds/parameters in the node group so the look is reproducible
across shots (consistency is the show's #1 rule).

---

## 5. Baking

- **When:** only to *flatten* an expensive procedural or a multi-layer paint into a
  single image for performance or hand-off — not for lighting (the ramp lights at
  render, never bake light in). Bake **Diffuse → Color only** (disable Direct +
  Indirect so no light is baked), or bake the specific node output via an Emit bake.
- **How:** EEVEE/Cycles bake to an image the size you'll ship at, margin ≥ 4–8 px to
  avoid seam bleed, bake to a non-color-data image where it's a mask.
- **Decal/alpha bakes:** bake with alpha so transparency survives.
- **Never bake AO or a combined pass into a toon albedo** — it reintroduces the
  double-shading problem (§2).

---

## 6. Resolution discipline

Cel surfaces are flat; they don't need 4K. Over-resolution is wasted VRAM and bake
time for zero visible gain once banded.

- **Flat-fill materials:** no texture — a color value, 0 texels.
- **Grime/wear/pattern masks:** **512–1024 px** is almost always enough; the ramp
  and outline hide fine detail.
- **Hand-painted decals / face markings:** **1024 px**, up to 2048 for a hero decal
  that pushes to camera.
- **Screen content (Chip):** size to how big it gets on screen — **1024** typical,
  **2048** only for a full-frame insert.
- **Author ~2x final, downsize on export** for crisp edges, then ship the smaller
  size. Power-of-two dimensions. Pack single-channel masks into RGB channels of one
  image (R=grime, G=wear, B=pattern mask) to cut texture count.

Rule: start at the smallest size that reads, only go up when a specific shot proves
it's blurry.

---

## 7. Keeping it consistent (reused assets)

- Pull every fill color and map from the **character's palette hexes** in the locked
  asset README — maps must match the flat fills they sit beside.
- Keep reusable masks/decals/overlay plates in a shared library (`comp/plates/`,
  `tex/decals/`), generated once and appended into shots — same analog texture
  everywhere (see `../blender/compositing-grade.md`).
- Any map that encodes a *state* (damage, glitch, screen frame) is a named,
  canonized asset, never an ad-hoc per-shot repaint.

---

## Verify

1. **Ramp-fight test.** Put the textured surface next to a plain flat-fill surface
   of the same base color under the key light. Both show the same clean N bands at
   the same terminator; the map shifts local color only, it does **not** add its own
   highlights/shadows or extra value steps.
2. **Flat-read test.** At the hero camera the textured area still reads as a crisp
   graphic cel surface (hard shapes, flat values) — not a photoreal/noisy patch.
3. **Resolution test.** Drop the map one size (e.g. 1024→512) and re-render the hero
   frame; if you can't see the difference, ship the smaller map.
4. **No baked light.** Any baked texture contains color/mask only — toggling the
   scene lights still changes the shading (proof light isn't baked in).
5. **Consistency.** Fill colors and decals match the locked palette hexes; reused
   decals/plates come from the shared library, not re-authored per shot.
