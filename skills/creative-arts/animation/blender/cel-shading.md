---
id: creative-arts.animation.blender.cel-shading
name: cel-shading
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, cel-shading, toon, npr, shader-to-rgb, colorramp, inverted-hull, outline, solidify, hue-shift, bloom, glare, view-transform, light-linking]
level: advanced
status: verified
description: "Professional EEVEE Next cel recipe: Shader-to-RGB + CONSTANT ramp 3-tone, hue-shifted shadows, inverted-hull outlines, bloom control, Standard view transform."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Blender Cel-Shading — EEVEE Next NPR to a professional bar

**Goal:** flat, saturated, hard-banded toon surfaces with a crisp constant-weight
ink line, hue-shifted (not merely darkened) shadows, and controlled bloom — the
Murder Drones / Rick & Morty register. This shader is the single biggest lever on
the show's fidelity. Target engine: **EEVEE Next** (Blender 4.5 LTS).

---

## 1. Render / color settings (non-negotiable)

- **Engine: EEVEE Next.** `scene.render.engine = 'BLENDER_EEVEE_NEXT'`.
  `Shader to RGB` — the node the whole recipe pivots on — exists only in EEVEE,
  not Cycles. NPR = EEVEE here, always.
- **View Transform = Standard.** `scene.view_settings.view_transform = 'Standard'`.
  This is mandatory and the most common reason a cel render looks muddy. AgX
  (4.x default) and Filmic apply a film-emulation tone curve that desaturates and
  soft-rolls highlights/shadows — it *reshapes the exact flat values your ColorRamp
  just produced*. Your ramp outputs a deliberate 3-tone; AgX then smears those three
  values into a gradient and mutes the saturation. Standard passes your authored
  values straight through (no tone map), so the bands stay flat and saturated. Keep
  `Look = None`, `Exposure = 0`, `Gamma = 1`.
- **Samples:** TAA render 16–32. Flat banded shading has almost no noise, so high
  samples waste time; 16 is usually plenty, 32 for fine outline AA.
- **Shadows:** keep soft shadows low / jittered-shadow samples low for the hardest
  terminator (the band break should be a crisp line, not a soft gradient the ramp
  then has to re-harden). Enable Shadows (EEVEE Next raytraced shadows) so the ramp
  has a real light/shadow signal to quantize.

---

## 2. The toon material node graph (per character/prop)

The core chain, with real values:

```
Diffuse BSDF                     base color = the fill color (e.g. Ivy skin 0.85,0.62,0.50)
  │  (BSDF output)
  ▼
Shader to RGB                    converts the shaded result to an RGB value 0..1
  │  (Color output)
  ▼
Color Ramp   interpolation = CONSTANT     ← the quantizer: N flat bands
  │
  ▼
Mix Color (Multiply, Fac=1)     A = ramp output,  B = base fill color
  │   → multiplies the band mask over the character's actual color
  ▼
Emission     (Color = Multiply result, Strength = 1.0)
  │
  ▼
Material Output (Surface)
```

Why each node:

- **Shader to RGB** turns the lit BSDF into a plain brightness value you can remap.
- **Color Ramp, interpolation = CONSTANT.** Constant interp = hard steps = cel
  bands. Each stop is one flat tone; the stop *position* is the terminator
  threshold. (Linear/Ease interp would give you a smooth gradient — not cel.)
- **Multiply over base color.** The ramp produces a grayscale-ish light mask; you
  multiply it against the object's real fill color so one ramp drives every colored
  material. Alternatively put the actual tinted colors *in the ramp stops* (lets you
  hue-shift per band, §4) — do that for hero characters.
- **Emission output.** Feeding the final color through Emission makes EEVEE treat
  it as self-lit and **stop re-lighting it** — the ramp already *is* the lighting, so
  you don't want the engine adding another diffuse pass on top. Result: pure flat
  cartoon fill. (A Diffuse BSDF as the final surface would get re-shaded by scene
  lights and lose the flatness.)

Save the whole chain as a node group **`NPR_Toon`** with exposed inputs (Base
Color, band positions, shadow tint) and append it into every character file. One
group, edited once, updates the whole cast.

---

## 3. Band count and positions

- **3-tone (this show's default):** lit / mid / shadow. Three ColorRamp stops,
  CONSTANT. Typical positions: **shadow 0.0–0.35, mid 0.35–0.65, lit 0.65–1.0**.
  Move the lit→mid boundary higher (~0.7) for a smaller, punchier highlight; move
  the mid→shadow boundary (~0.3) to control how much of the form sits in core
  shadow.
- **2-tone (anime lit/shadow):** simpler characters/props — one terminator around
  0.5. Reads very "anime".
- **Optional 4th "core shadow" band** (darkest, ~0.0–0.12) adds richness on hero
  faces. Don't exceed 4 — more bands drift toward smooth shading and lose the toon
  punch.

Band positions are a look decision; lock them in `NPR_Toon` so the whole cast
quantizes identically.

---

## 4. Hue-shifted shadows (the appeal lever)

A "just darker" shadow (same hue, lower value) reads cheap and muddy. Professional
cel tints the shadow **cooler** and often slightly **more saturated**. In each
ColorRamp shadow stop (or in the per-band tint), push the color:

- **Hue toward blue/purple** (+0.04 to +0.12 in hue) relative to the lit color.
- **Value ~65–80%** of the lit band (not 40% — shadows that are too dark kill the
  flat-graphic read).
- **Saturation equal or slightly up** in shadow, so the shadow has color, not grey.

So Ivy's warm skin (hue ~0.06 orange) gets a shadow at hue ~0.60–0.70
(blue-violet), ~75% value. The warm-light / cool-shadow split is what gives the
image depth and "expensive" appeal without adding geometry or lights. Do the same
across the palette so the whole frame reads as one lit environment.

---

## 5. Rim / spec in NPR

- **Rim light (fake, cheap, recommended).** Add `Layer Weight → Facing` → its own
  `Color Ramp` (CONSTANT, one bright stop near the grazing edge) → `Add` into the
  emission color, masked to the **lit side only** (multiply the rim by the main
  light's N·L mask so it doesn't ring the shadow side). Gives the Murder-Drones
  edge-pop. Keep it a thin hard band, not a gradient.
- **Toon specular.** For glossy surfaces (Pixel's case, eyes), a second small
  CONSTANT-ramp band driven by a specular/Fresnel term gives a hard clipped
  hotspot — the classic anime "shine chip." Keep it a single tiny hard shape, not a
  blurry Blinn highlight.
- Avoid real `Glossy BSDF` reflections in the toon chain; they reintroduce
  continuous gradients that fight the bands.

---

## 6. Inverted-hull outline — exact recipe

Per-object, GPU-cheap, gives the silhouette ink line.

1. Add a **Solidify** modifier to the mesh.
2. **Thickness:** small negative, e.g. **-0.01 to -0.03** world units (or positive
   thickness **+ Flip Normals ON** — equivalent). Negative/flipped pushes a shell
   *outward* whose faces point *inward*.
3. **Material Offset:** set to the slot index of a dedicated outline material
   (add `OUTLINE_black` as the last material slot; set Material Offset so the
   solidify shell uses it).
4. **`OUTLINE_black` material:** a flat **black Emission** (Strength 1.0), with
   **Backface Culling ON** (`Settings → Backface Culling` in EEVEE material
   settings). Backface culling hides the shell's front faces (which point away from
   camera) and shows only the back faces along the silhouette — producing a clean
   black rim exactly on the silhouette edge, and nothing over the character's front.
5. Keep the shell's normals flipped so only the silhouette band renders black.

Because the outline color is pure black emission, the Standard view transform (§1)
keeps it a true 0,0,0 line instead of AgX lifting it to dark grey.

### Controlling outline weight

- Thickness is **world-scale** → apparent line weight changes with character size
  and camera distance. **Fix each character's canonical height and apply scale**
  (see `character-modeling.md` §8) so the line is consistent. Pick one thickness
  per character at the reference camera distance and store it in the asset README.
- For a line that stays pixel-constant regardless of zoom, drive thickness by
  distance-to-camera (Geometry Nodes: extrude along normals by `factor /
  distance_to_camera`, flip faces, assign the black backface-culled material). Save
  as node group `NPR_Outline`. Use on hero characters where camera pushes in.
- Vertex-group limiter on the Solidify (`Vertex Group` field) lets you thin or
  remove the line on specific areas (inside the mouth, tiny fingers).

### When the hull fails, and fixes

- **Thin features (fingers, antennae, thin cards):** if the feature's cross-section
  is thinner than ~2x the shell thickness, the inward shell self-overlaps and the
  line inverts/flickers or shows white backfaces. **Fix:** give the feature real
  volume, reduce thickness locally via vertex-group limiter, or split it to its own
  object with a thinner hull.
- **Intersections / interpenetrating surfaces:** two meshes poking through each
  other produce stray black where the hulls collide. **Fix:** boolean/merge them
  into one surface, or separate objects and accept the seam, or exclude via vertex
  group.
- **Hard concave corners** can show a gap in the line. **Fix:** `Solidify →
  Complex` mode, or add a tiny bevel so the corner has a face to carry the shell.
- **Open meshes / zero-thickness cards** can't form a closed shell — the line
  breaks. **Fix:** make the mesh manifold, or outline it with Freestyle instead.

### Freestyle (secondary — interior lines the hull can't do)

`scene.render.use_freestyle = True`, add a LineSet (silhouette + crease + material
boundary), linestyle thickness ~1.5–2.5 px with slight along-stroke variation for a
hand-drawn feel. Use for interior creases (jaw line, case seams) the hull doesn't
produce. Slower — reserve for hero shots.

---

## 7. Preventing bloom/glare from washing out emissive faces

**Real problem on this show:** Pixel's emissive screen-face blows out to white under
the compositor **Glare node in FOG_GLOW** mode. Because the screen-face is an
Emission surface and the toon fills are *also* emission, a FOG_GLOW glare with a low
threshold treats the bright screen (and bright lit bands) as a light source and
bleeds a white halo across them, destroying the flat read.

Fixes, in order:

1. **Raise the Glare threshold** so only genuinely super-bright pixels bloom.
   Emission Strength 1.0 fills sit at ~1.0; set the Glare `Threshold` above 1.0
   (e.g. 1.2–2.0) so normal toon fills and the screen-face at strength 1 are *below*
   threshold and don't bloom. Only push a light/effect above that threshold when you
   actually want it to glow.
2. **Use `BLOOM` (or SCREEN mix) low, not FOG_GLOW aggressive.** FOG_GLOW spreads a
   wide soft halo; keep its `Size` small and `Mix` toward -0.8..-0.5 so the glow is a
   faint additive sheen, not a wash.
3. **Keep the screen-face emission at a controlled strength** (≈1.0, not 5–10) and
   drive its *apparent* brightness with the fill color, not raw strength. If it must
   read as bright, use a thin rim-glow rather than cranking strength past the glare
   threshold.
4. **Mask bloom with a render pass / cryptomatte** if a single element must glow
   while flat fills stay crisp — glare that element on its own layer in comp.

Net rule: emission strength is a *glare budget*, not a brightness dial. Keep toon
fills ≈1.0, keep the glare threshold above 1.0, and only deliberate glow elements
exceed it.

---

## 8. Lighting drives the ramp (light-linking)

The ramp quantizes whatever light hits the surface, so lighting *is* the shading
control:

- **One Sun key** (clean, single terminator) + soft fill via a low ambient / world
  color or a second dim area. Many lamps = many terminators = muddy bands. Light the
  cel scene like a 2-light key/fill setup.
- **Light position sets the terminator**, i.e. where the band break lands on the
  face. Aim the key so the shadow shape flatters the character — this replaces
  "shadow painting."
- **Light Linking** (`Object → Light Linking`, or the light's collection): link a
  character's key light only to that character so you can art-direct each hero's
  terminator without disturbing others. Use a dedicated rim light light-linked to
  hero characters for the §5 rim without ringing the set.
- Because the fills are emission (§2), scene lights affect the *BSDF feeding Shader
  to RGB*, not the final emission — so lights steer the band mask, never add an
  uncontrolled second lighting pass.

---

## 9. Upgrade path (not needed now)

- **Blender 5.x EEVEE NPR nodes** (Light Evaluation, Shadow Raycast, Light Info,
  Light Accumulation — co-developed with Goo Studios) give finer control without the
  Shader-to-RGB round-trip. We're on 4.5 LTS; migrate at the next LTS.
- **Goo Engine** (anime-focused Blender fork) is an option but a fork to maintain;
  stay on stock 4.5 unless we hit a wall.

---

## Verify

1. **View transform check.** Render the hero frame; toggle View Transform
   Standard ↔ AgX. Under Standard the bands are flat and saturated with a crisp
   terminator; if your "cel" look only appears under AgX, the ramp is misconfigured.
   Ship Standard.
2. **Banding check.** Sample the lit face across the terminator: exactly N distinct
   flat values (no gradient between them), ramp interp = CONSTANT.
3. **Hue-shift check.** The shadow band is measurably cooler in hue than the lit
   band (blue/violet shift), not just lower value.
4. **Outline check.** The silhouette carries a clean constant-weight black line; no
   white backface flicker on thin features; line weight matches the rest of the cast
   at the reference camera distance (object scale applied = 1,1,1).
5. **Bloom check.** Pixel's screen-face and the bright lit bands read flat and crisp
   with the Glare node on; no white halo wash. Only elements you *intend* to glow
   exceed the glare threshold.

## Verified (proof)
In use across a production pipeline: the Diffuse→ShaderToRGB→CONSTANT ColorRamp→Multiply
→Emission graph with Standard view transform produces clean 3-tone cel with hue-shifted
shadows and crisp inverted-hull outlines on the hero close-ups (Pixel, Ivy) and in-set
(EP01_SQ01_SH110). With the comp glare threshold at 1.0/mix 0.10 the emissive faces read
without blowing to white. The recipe holds from hero to episode shot.
