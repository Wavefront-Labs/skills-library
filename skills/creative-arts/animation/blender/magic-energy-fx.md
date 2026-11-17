---
id: creative-arts.animation.blender.magic-energy-fx
name: magic-energy-fx
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, magic, energy, fx, sparkle, pixie-dust, glow, aura, beam, zap, lightning, electricity, shield, portal, fresnel, shockwave, heat-haze, emission, glare, bloom, cel, stylized, on-twos]
level: advanced
status: draft
description: "Stylized magic/energy FX for a cel show in EEVEE Next: glows, pixie-dust trails, beams, shields, lightning, shockwaves — readable Disney-sparkle language, not noise."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# magic-energy-fx

Goal: the classic feature-animation "Disney sparkle" — magic that reads as *drawn*,
shaped, and timed, not as a particle preset. Everything here targets Blender 4.5
EEVEE Next inside the show's cel pipeline (`creative-arts.animation.blender.cel-shading`:
ShaderToRGB + CONSTANT ramp, Standard view transform, inverted-hull outlines). The
router for which FX go 3D vs 2D cards is
`creative-arts.animation.blender.fx`; the 2D card/smear language itself is
`creative-arts.animation.blender.toon-effects-animation`.

## The one law: shape first, glow second

Audiences read magic by **silhouette and timing**, not by brightness. Every effect
below is built as a hard-edged, flat-colored shape (on-model with the cel look),
and *then* given controlled glow in comp. If an effect only works because it's
bright, it doesn't work.

**Glow discipline (applies to everything in this skill):**
- In-shader: *Emission* with Strength 2–8. Under the Standard view transform there
  is no filmic shoulder to save you — values above ~10 clip to white mush and
  destroy the flat-color read.
- Bloom: EEVEE Next has no legacy Bloom; bloom is the compositor **Glare node
  (Bloom mode)**. Set Threshold *above* your brightest non-FX pixel (typically
  1.05–1.3) so only emissives bloom — the cel fills stay flat. Size 6–7, Mix ≈
  −0.7 (mostly original + a little glare). This is the single most common failure:
  threshold under 1.0 blooms the whole character.
- Separate control: put magic emitters on their own View Layer or use a Cryptomatte
  so the grade (`creative-arts.animation.blender.compositing-grade`) can gain FX
  glow without touching the picture.
- Auras: inverted-hull-style shell (Solidify, flipped normals, backface culling) with
  a **fresnel-gated emission** — *Layer Weight (Facing)* → *ColorRamp (CONSTANT)*
  with two stops, so the rim is a hard band, not a soft falloff. A soft fresnel
  gradient is the #1 tell of "3D render pretending to be cel".

## Color language of magic

Decide this once per show and never improvise per shot:
- **Hue = allegiance/source.** e.g. protagonist arcana cyan-white, wild/dangerous
  magic magenta, corrupted sickly green. Audiences track it subconsciously;
  breaking it for one shot reads as an error.
- **Two flats + white core** per effect: core (near-white, value ~0.95), body
  (saturated hue), rim/trail (darker, shifted hue — shift the *hue*, not just the
  value, same rule as cel shadows). Three flat colors max; more turns to mud at
  TV scale.
- **Hot frames are white.** Impact frames flash the full shape to near-white for
  1–2 frames. White is reserved for peaks — if idle magic is white, impacts have
  nowhere to go.

## Pixie-dust trails

The signature sparkle. Build:
1. Emitter: particle system (or the GN trail rig from
   `creative-arts.animation.blender.geometry-nodes`) on an empty parented to the
   wand/hand. Count low — **40–120 alive**, not thousands; sparkles are individuals,
   not fog. Lifetime 12–24 frames. Normal velocity near 0, gravity ~ −0.2 (dust
   floats), Brownian 0.02 for shimmer drift.
2. Render each particle as an instanced **4-point star card** (flat mesh, emissive,
   camera-facing via *Track To* on the instance or a GN *Align Rotation* to camera
   vector) — never halo dots. Two or three star sizes picked randomly.
3. **Twinkle on 2s:** drive each star's emission strength with a square-wave —
   material *Attribute* (particle random) + *Math: Modulo* on frame/2 so half the
   stars are bright on even frames, half on odd. Stepped twinkle reads as drawn;
   smooth sine reads as a screensaver.
4. Death: scale to zero over the last 4 frames **in steps** (4→2→1→0 px), not a
   fade. Cel magic pops out; it doesn't dissolve.
   Particle fundamentals live in `creative-arts.animation.blender.particles-fx`.

## Beams and zaps

- Geometry: a curve from caster to target, *Curve to Mesh* with a flat ribbon
  profile (GN), not a cylinder — a ribbon with a white core strip and colored edge
  strips (UV-mapped CONSTANT ramp across the width) gives the classic 2-tone beam.
- **Timing is the craft:** anticipation glow at the hand (4–6 f, growing star) →
  beam appears **full length in 1 frame** (never grow it along its length — lasers
  in animation are instantaneous, growth reads as a garden hose) → hold with
  width oscillating ±15% on 2s → cut off in 1 frame + a 2-frame afterimage (same
  ribbon, rim color only, 50% width).
- Zaps (short-range hits): 3–5 frames total. Frame 1: white hit-flash card at the
  target (`toon-effects-animation` impact-flash language). Frames 2–4: beam breaks
  into 2–3 dashes that fly backwards along the path and pop out.

## Shields and portals

- **Shield:** a sphere/section with two layers. Layer 1: fresnel rim as above (hard
  CONSTANT band at Facing ≈ 0.7). Layer 2: an **animated ramp** across the surface —
  a *Wave* or ring texture mapped on UV/object-Z, fed through a CONSTANT ColorRamp,
  with its Mapping *Location* keyed so bands sweep outward from the impact point.
  On hit: flash rim to white 1 frame, spawn a hex/ripple ring (GN *Curve Circle*
  Progress rig) at the impact, wobble shield scale 1.0→1.04→0.99→1.0 over 6 frames.
- **Portal:** flat disc, 2–3 counter-rotating emissive rings (keyed rotation on 2s,
  i.e. stepped interpolation every 2 frames), plus an inner disc shaded with a
  slow-scrolling noise through a 3-stop CONSTANT ramp (deep/mid/bright of the magic
  hue) so the interior churns in flat bands. Rim gets the pixie-dust emitter at low
  count. The portal edge gets **no inverted-hull outline** (it's light, not an
  object): put it in a collection excluded from the outline pass or zero the hull
  thickness.

## Lightning / electricity

Hand-feel comes from jitter, not simulation:
- Build the bolt as a curve: GN *Mesh Line* caster→target → *Set Position* with
  **white-noise offset perpendicular to the path** (Noise Texture 4D, W = `floor
  (frame/2)` via a Value node driver `floor(frame/2)` so the bolt re-rolls **every
  2 frames and holds between** — the on-2s re-jitter *is* the electricity look) →
  *Points to Curves* → ribbon profile.
- Add 1–2 child branches: duplicate the rig, start at a random parametric point of
  the parent, half the width, 2/3 the length.
- Lifetime of any bolt: 2–6 frames. Lightning that persists reads as a rope. For a
  sustained arc, cycle 3 pre-rolled bolt variations A-B-A-C on 2s.
- Ground contact gets a flash card + 2–3 debris sparks
  (`toon-effects-animation`); big strikes add a frame of **inverted exposure** on
  the whole shot (compositor switch) — one frame only.

## Shockwaves and heat-haze-style distortion

- **Shockwave ring:** GN *Curve Circle*, radius keyed with a sharp ease-out
  (80% of final radius in the first 25% of frames), ribbon width shrinking to 0 as
  it expands, 2 flat colors. Duration 6–10 frames. Offset a second, thinner ring 2
  frames behind at 60% opacity for richness.
- EEVEE Next has no cheap refraction-everything; **fake distortion in comp**: render
  a mask of the haze region (emissive-white object on its own view layer), use it
  to drive a *Displace* node on the main image with an animated noise. Keep
  displacement ≤ 6–8 px and **posterize the noise** (ColorRamp, CONSTANT, 3 stops)
  so even the distortion is stepped — smooth refraction next to stepped shading
  breaks style. For most shots a drawn wobble-line card from
  `toon-effects-animation` is cheaper and reads better than true distortion.

## Shaped flashes on 2s

The connective tissue of all of the above: magic animates **on 2s with held
poses**, exactly like the character animation. Keyframe emission strength, scale,
and ramp positions with **Constant interpolation** (T → Constant in the Graph
Editor) and place keys on even frames. Shapes change pose-to-pose: a flash is
star → burst → ring → gone, four distinct drawings, not one shape scaling up.
If an effect looks wrong, fix the *poses and spacing*
(`creative-arts.animation.principles.twelve-principles`) before touching the shader.

## Layering 3D emitters with 2D cards

The finished look is a sandwich:
1. **3D core** (this skill): beams, shields, trails that must track 3D space and
   parallax.
2. **2D toon cards** (`toon-effects-animation`): impact flashes, smears, radiating
   speed-lines — camera-facing cards or Grease Pencil, drawn on 2s. These sell the
   hits.
3. **Comp** (`creative-arts.animation.blender.compositing-grade`): the single Glare
   pass, per-effect gain via Cryptomatte, the one-frame invert on big impacts.
Rule of thumb: 3D for anything the camera moves around; 2D for anything under 8
frames long. When in doubt, 2D — it's cheaper and more stylish.

## Readability, not noise (the taste section)

- **One hero effect per frame.** If the shield, the beam, and the dust all peak at
  once, stagger them by 2–4 frames. The eye follows the newest brightest thing.
- Count your particles on a paused frame: if you can't count them, there are too
  many.
- Check every FX shot in **greyscale** (viewport → Display Render Preview with a
  desaturate comp toggle): the effect must read by value alone. If it vanishes,
  the problem is value structure, not color.
- Watch at 25–50% zoom — YouTube-at-phone-size is the delivery target; sparkle that
  only reads at 100% is wasted render time
  (`creative-arts.animation.blender.render-optimization`).

## Verify

- [ ] Glare threshold > brightest non-FX pixel: toggle the Glare node — only magic
      changes, the character's fills don't.
- [ ] No emission strength above ~10 anywhere (clips under Standard view
      transform); hot frames hit near-white without pure 255 flat-lining the core.
- [ ] Fresnel rims and ramps are CONSTANT-stepped bands — zero smooth gradients in
      a frame-grab.
- [ ] All FX keys are Constant interpolation on 2s; a frame-by-frame step-through
      shows distinct held poses, no sub-frame slide.
- [ ] Pixie dust: countable stars (≤ ~120), stepped twinkle, pop-out deaths.
- [ ] Lightning re-jitters every 2 frames and never persists > 6 frames per bolt.
- [ ] Greyscale pass: every effect still reads by value.
- [ ] Portal/shield/beam objects excluded from the inverted-hull outline pass.
- [ ] Color language matches the show bible hue assignments; white appears only on
      peak frames.
