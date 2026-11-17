---
id: creative-arts.animation.texturing.texture-painting
name: texture-painting
category: creative-arts
field: animation
product: texturing
tags: [texturing, texture-paint, blender, stencil, mask, cel, toon, hand-painted, grime, wear, decal, npr, baking, eevee]
level: advanced
status: draft
description: "Hand-painting texture detail for a cel show in Blender Texture Paint: stencils, masks, keeping paint off the ramp, baking, resolution."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hand-painting texture detail for a cel-shaded series

**Context:** `../texturing/textures-maps.md` decides *whether* a surface needs a map,
its UV strategy and resolution. This skill is the other half — the actual **painting**:
sitting in Blender's Texture Paint mode and laying down grime, wear, decals, face
markings, screen art and painted "shadow-as-art" by hand, so the result looks like a
*designed* cel image and not a photo patch. The one law from `textures-maps` carries
through everything here: **paint the albedo only, never paint light** — the toon ramp
(`../blender/cel-shading.md`) owns all shading, and any highlight/shadow you paint
fights it.

---

## 1. Set up the paint surface before you touch a brush

1. **UV first.** A relaxed, low-distortion unwrap (`../blender/uv-unwrapping.md`) for
   anything you'll hand-paint — distortion in the island = smeared brush strokes.
2. **Create the image, don't paint onto "Untitled".** In Texture Paint > add a new
   image at the target size (§6), **32-bit float off**, color space **sRGB** for a
   color/albedo map, **Non-Color** for a mask you'll feed a factor. Name it
   `<char>_<role>_col` / `_mask` so it is findable in the asset README.
3. **Paint through the shader, not a bare image.** Add an `Image Texture` node wired
   into the **Base Color** of `NPR_Toon` and select it as the paint slot, so the
   viewport shows the ramp banding *while you paint*. Painting against a flat unlit
   image lies to you — you only learn the paint fought the ramp at render.
4. **Set the viewport to Rendered (EEVEE Next) with the key light on.** You must see
   the banded result live; Material Preview hides the ramp.

---

## 2. Brushes that match the cel look

The toon surface is **hard graphic shapes and flat values**, so default soft
airbrushes are wrong — a soft falloff reads as photoreal gradient the moment it sits
next to a crisp fill.

- **Hard-edge brushes.** Falloff = **Constant** or a tight custom curve, not Smooth.
  For graphic shapes (decals, markings) paint with a near-binary edge.
- **Low, flat opacity.** Build local-color patches with one or two confident passes,
  not fifty airbrush taps — accumulation makes muddy value, and value is the ramp's
  job.
- **Texture/alpha brushes for repeat detail.** Load a hard-dot or hatch alpha for
  stylized "cel grain", stamp it; don't smear a noise brush.
- **Lock value, shift hue.** Pick grime/wear colors at **the same value as the base
  fill, different hue/saturation** (see §4). A value plunge becomes a hole once the
  ramp darkens the band.
- **Symmetry (X mirror)** for faces/costumes so markings stay on-model and you paint
  half the work.

---

## 3. Stencils — the workhorse for graphic shapes

Stencil mode (press/hold the stencil, scale/rotate over the mesh) is how you place a
**sharp designed shape** — a logo, a number, a face marking, a scuff band — without
hand-trembling the edge.

- Make the stencil image in a raster editor (clean vector-ish shape on transparent),
  load it as the brush **Texture**, mapping = **Stencil**.
- Position it in the viewport over the surface, paint — the shape transfers with its
  own crisp edge regardless of brush jitter.
- **For decals that must stay movable per shot, don't stencil into the body map** —
  use a separate decal plane (`textures-maps` §3). Stencil-into-map only for marks
  that are permanent on the character (a cheek scar, a painted stripe).
- Stencils respect UV seams badly across an island boundary — keep a stencilled shape
  inside one island, or paint the seam crossing by hand.

---

## 4. Painting grime, wear and "painted shadow" without fighting the ramp

This is the part that separates a cel artist from someone who imports Substance grunge
and wonders why it looks wrong.

- **Grime = local-color patches, not dirt-with-shadow.** A soot streak is a desaturated
  cooler patch of the *same value*; it must read after the ramp bands it. Paint it,
  then flip the light off — the patch should still be visible as a hue shift, proving
  it is color not light.
- **Wear = graphic edge damage.** A chipped paint edge is a hard shape of the
  underlying material color, placed by stencil on corners/edges — not a bevel-baked
  cavity.
- **"Painted shadow as art" (the deliberate exception).** Sometimes the director wants
  a *graphic* contact shadow or a stylized AO shape that the ramp can't give — a hard
  dark shape under a collar, a designed grime-in-the-crease. This is **art, painted as
  flat dark local color into a dedicated layer**, used sparingly and consciously. It is
  NOT baked AO (that's §5's forbidden move) — it's a hand-placed graphic the art
  director approved shot-to-shot. Keep it on its own image/mask so it can be dialed or
  removed, and keep its value one step, not a gradient.
- **Never paint a highlight.** A specular glint is a comp or a small emissive detail,
  never a painted bright blob in the albedo — the ramp's light band already is the
  highlight.

---

## 5. Masks and layered paint

Hand-painting one flat image is limiting; layer with masks so detail is editable.

- **Paint masks, composite in the shader.** Paint a grime *mask* (Non-Color, white =
  grime) and `MixRGB` the grime color over the base fill by that mask in the node
  graph (`../blender/shader-authoring-lookdev.md`). Now grime placement and grime color
  are independently tweakable, and the mask is reusable.
- **Channel-pack masks.** R=grime, G=wear, B=decal-area in one Non-Color image — three
  masks, one texture sample (echoes `textures-maps` §6).
- **Vertex-paint masks** for broad, UV-independent zones (whole-limb dirt) — cheaper
  than an image and seam-free.
- Keep each paint purpose on its own image or channel; a single baked-flat image is the
  *last* step (§5-bake), not how you work.

---

## 6. Baking painted layers

Bake only to **flatten** a multi-layer paint/procedural stack into one ship image for
performance or hand-off — never to bake light.

- **Bake Diffuse → Color only:** disable Direct + Indirect contribution so no lighting
  enters the image, or use an **Emit** bake of the specific color output. This is the
  same rule as `textures-maps` §5 — the ramp must still light at render after the bake.
- Margin **≥ 4–8 px** (bleed past seams), bake at the ship size, non-color for masks.
- **Prove the bake carries no light:** after baking, toggle the scene key light — the
  shading must still change. If the baked surface looks the same lit and unlit, you
  baked light in; redo with Direct/Indirect off.
- Alpha-bake decals so transparency survives.

---

## 7. Resolution while painting

Paint ~2× the ship size for crisp strokes, downsize on export (`textures-maps` §6 owns
the ship numbers). Practical defaults: grime/wear masks **512–1024**, hand-painted
markings/decals **1024**, a hero face-to-camera marking up to **2048**. Flat-fill
surfaces get **no** painted map — a color value is zero texels. Don't paint 4K detail
the outline and banding will swallow.

---

## 8. Consistency (the show's #1 law)

- Pull grime/wear/mark colors from the character's **locked palette hexes** in the
  asset README — painted detail must sit beside the flat fills without a color clash.
- Any painted detail that encodes a **state** (battle damage, a specific mark) is a
  **named canonized asset** saved to the shared `tex/` library, never an ad-hoc per-shot
  repaint — same reason `../pipeline/character-consistency.md` locks everything else.
- Save the `.blend`'s packed paint images out to disk (`File > External Data > Unpack`)
  and register them; an image living only inside one `.blend` is lost the moment the
  asset is reused.

---

## 9. Common failures (and the fix)

| Symptom | Cause | Fix |
|---------|-------|-----|
| Grime looks "muddy" after render | painted value drop | repaint as same-value hue shift (§2, §4) |
| Double shadows on the surface | painted highlight/AO in albedo | strip it; let the ramp light (§2) |
| Soft photo patch amid crisp fills | soft airbrush, smooth falloff | hard/constant brush, flat opacity (§2) |
| Decal edge jitters | hand-painted, no stencil | use a stencil-mapped brush (§3) |
| Smeared strokes | UV distortion in the island | relax the unwrap first (§1) |
| Seam-line bleed on bake | margin too small | margin ≥ 4–8 px (§6) |
| Baked surface won't re-light | baked light in | bake Diffuse→Color only, Direct/Indirect off (§6) |
| Grime placement welded, can't tweak | painted into one flat image | layer via a mask + node mix (§5) |
| Detail blurs out at render | over-resolution swallowed by band/outline, or under-res | right-size (§7), author 2× ship |
| Paint lost when asset reused | image packed only in one `.blend` | unpack to disk + register (§8) |

The through-line: nearly every failure is either **painting light** (fix: albedo only)
or **painting soft** (fix: hard graphic shapes). Keep those two reflexes and the cel
read holds.

## 10. Workflow order (summary)

UV-relax → create named image in the right color space → wire into Base Color → set
Rendered view with key light → block local-color patches (hard brush) → stencil the
graphic shapes → paint masks for editable detail → composite masks in nodes → (only if
needed) bake color-only → size down to ship → unpack + register. Painting against the
live banded result the whole way is the single habit that keeps paint from fighting the
ramp.

---

## Verify

1. **Light-off test.** Toggle the scene lights off: every painted grime/wear/mark patch
   is still visible as a **local-color** shift. Anything that *disappears* was painted
   light — repaint it as color.
2. **Ramp-fight test.** Place the painted surface beside a plain flat-fill of the same
   base color under the key: both band identically at the same terminator; the paint
   adds no extra value steps or its own highlight/shadow.
3. **Flat-read test.** At the hero camera the painted area reads as crisp graphic cel
   detail (hard shapes, flat value), not a soft photo patch.
4. **Edit test.** Grime color and placement can be changed independently (mask-driven),
   not welded into one flat image — proving you layered, not stamped.
5. **Bake test.** Any baked image contains color/mask only — toggling lights still
   re-shades it.
6. **Consistency test.** Painted colors match the locked palette hexes; any state-detail
   is a named asset in the shared library, not re-painted per shot.

See `../texturing/textures-maps.md` (when/UV/resolution strategy), `../blender/cel-shading.md`
(the ramp this must not fight), `../blender/uv-unwrapping.md`, `../blender/shader-authoring-lookdev.md`
(mask compositing in nodes), `../pipeline/character-consistency.md`.

See also `creative-arts.animation.blender.texture-painting` (`../blender/texture-painting.md`) for the general Blender Texture Paint workflow: brushes, slots, stencils, bleed and saving packed images.
