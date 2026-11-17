---
id: creative-arts.animation.blender.lighting
name: lighting
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, eevee, three-point, rim-light, kick, key-fill-ratio, toon, terminator, mood, cinematic, exposure]
level: advanced
status: verified
description: "Cinematic cel lighting in Blender EEVEE Next: clean toon terminators, key/fill/rim ratios, mood rigs, and exposure control so backgrounds never blow out."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Lighting for cel-shaded cinema (Blender EEVEE Next)

Lighting does two jobs at once in a toon show: it **drives the cel ramp** (where the
tone-band terminator falls = the drawn shadow shape) AND it **carries mood** (the
color script, per scene). A primitive scene lit with one flat sun and a blown-white
world is the #1 reason renders look cheap. This skill is how you light to the bar.

## 1. Key / fill / rim as explicit RATIOS (not "three lights")
Decide a **contrast ratio** per scene from the color script, then set energies to hit it:
- **Key (Sun or large Area):** the one light that defines the terminator. A Sun gives
  the cleanest, most parallel toon shadow edge; a large Area gives a softer wrap. Pick
  per look. Angle it 30–45° off camera and ~30–45° up for a classic sculpting key.
- **Fill:** raises the shadow band so it's not black. In cel work the shadow *colour*
  comes from the material ramp's cool-shifted dark band (see cel-shading), so fill is
  deliberately weak — a 4:1 to 8:1 key:fill for drama, ~2:1 for a soft/friendly scene.
  Fill via a weak opposite-side Area OR the World, never so strong it kills the bands.
- **Rim / kick:** a back-and-side light (often cool, slightly stronger than key at the
  edge) that separates the character from the background — the anime/Murder-Drones pop.
  Aim it down the far contour. This is what makes a character sit *in front of* a set
  instead of pasting flat against it.

## 2. Exposure discipline — the blown-background fix
Flat white backgrounds and pure-yellow frames are an **exposure/value failure**, not a
colour choice, and they destroy every composition:
- Set `view_transform = 'Standard'` for cel (required — Filmic/AgX desaturate the ramp),
  then control brightness at the SOURCE. With Standard there is no highlight rolloff, so
  anything over 1.0 clips to paper-white. Keep emissive and bright surfaces' output
  values in range (a bright wall ~0.7–0.85, not 2.0).
- A background/sky that reads should sit **darker than the subject** (value separation).
  If a doorway/sky blows out, drop its emission strength or world strength until the
  subject is the brightest thing in frame. The eye goes to the lightest, highest-contrast
  area — make that the subject, never an empty backdrop.
- Check with the compositor's scopes / a `volumedetect`-style value read, or just a
  luminance view: if the background is at 1.0 and the face isn't, the frame is wrong.
- Bloom/glare in comp AMPLIFIES anything near-white — an over-bright emissive face
  (e.g. Pixel's screen) will glow out to a white blob. Fix at the light/emission level
  AND raise the glare threshold (see cel-shading, compositing-grade).

## 3. World / ambient as scene tint (bounce)
Use a low World colour (not white) as cheap global fill that **tints everything toward
the scene's temperature** — this is what makes characters feel lit by the environment.
Strength ~0.3–0.8, colour pulled from the color-script key (warm amber interior, cool
blue night). A white World at strength 1+ flattens the ramp and washes the frame — avoid.

## 4. Named mood rigs per location (locked, reusable = consistency)
Store a rig per set as an appendable collection / node setup, each an explicit state of
key angle+energy+colour, fill ratio, rim, and World tint from the color script:
- **dusk_street ("the lie"):** warm gold low key, long shadows, amber World ~0.5,
  saturated and inviting — but keep the sky value below the characters.
- **drained (dread):** pull key warmth, World toward sepia-grey, flatten saturation,
  raise a sick ambient; animate the drain as a keyframed state.
- **alley/edge:** cooler higher-contrast key (6:1), the green seam as an emissive strip
  acting as a coloured rim.
- **void/archive:** near-black World, lit "by the machines" — emissive set pieces and
  half-dark practicals; chroma-green emissive seam. Characters lit by rim + practicals.
- **witnessed (finale "un-gold"):** soft warm-neutral low-contrast (2:1), sourceless
  gentle fill — the deliberate opposite of the gold glare.

## 5. EEVEE Next mechanics
- Hard shadows (soft-shadow low/off) give the crispest cartoon terminator; raise
  softness only for an intentionally soft look.
- Enable raytracing for contact shadow/AO if the set needs grounding; keep sample count
  modest (cel hides noise). 
- Use **light groups / light linking** to grade key vs rim separately in comp, and to
  stop a character fill from spilling onto a self-lit prop (e.g. don't fill Pixel's screen).
- Animate mood shifts (gold→drained, the "stutter") by keyframing World colour + key
  energy per shot — it's a storytelling beat, authored not accidental.

## Verify
- [ ] The subject is the brightest, highest-contrast thing in frame; background sits
      darker (no blown-white sky/door/wall). Confirm with a luminance/scope read.
- [ ] Key:fill ratio matches the scene's intended drama (measure, don't eyeball).
- [ ] Rim light visibly separates character from background on the far contour.
- [ ] view_transform is Standard and no large surface clips to 1.0 unintentionally.
- [ ] Each location uses its named locked rig; mood variations are explicit keyed states.
- [ ] Emissive faces/props don't bloom to white under the comp glare (threshold tuned).

## Verified (proof)
The exposure law was applied in the production `render_shot.py` as `apply_exposure_law()`
(run right after a set loads, before characters append): cap the world background Strength
to ~0.6 and clamp set emissive Strengths (a gold sky backdrop was emitting at 2.4, clipping
to paper-white) — sky to ~0.8, other set emissives to ~1.0, leaving the brighter character
materials untouched. On shot EP01_SQ01_SH110 the previously blown-out gold mainst sky
became a readable muted amber with the subject the brightest element; storefront/windows/
awning all read with depth. Confirms "subject brightest, background darker, nothing clips."

See cel-shading (the ramp this drives), color-script (the per-scene brief), compositing-grade
(glare/grade), look-development (the mood language + "no blown backgrounds" rule).
