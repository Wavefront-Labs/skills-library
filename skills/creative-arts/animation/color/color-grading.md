---
id: creative-arts.animation.color.color-grading
name: color-grading
category: creative-arts
field: animation
product: color
tags: [color, grading, color-grade, lift-gamma-gain, curves, scene-referred, display-referred, agx, lut, scopes, shot-matching, color-script, cel]
level: advanced
status: draft
description: "The color grade as a craft: scene- vs display-referred, lift/gamma/gain + curves, shot matching, mood, episode consistency, scopes, not fighting the cel ramp."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Color grading (the grade as craft)

**Goal:** the deliberate control of color and tone across a whole episode so each
shot reads with the intended mood, every shot in a scene matches its neighbors,
and the series holds one visual identity. This is tool-agnostic craft; in a Blender pipeline it's executed in the Blender compositor (per shot, `multipass-compositing`)
and with ffmpeg (global pass at delivery, `youtube-master`). The grade *realizes*
the `color-script` the art department drew; it does not invent color blind.
Finishing texture (glow, grain, vignette) is `compositing-grade` — a different
pass from the grade itself.

## Scene-referred vs display-referred — get this right first

Everything upstream mistake traces to confusing these two spaces.

- **Scene-referred** = linear light, open-ended values (a highlight can be 50.0).
  Your EEVEE renders and the Multilayer EXR live here. Grading in scene-referred
  means you're pushing light the way a real colorist does — multiply = exposure,
  and highlights roll off through a view transform instead of clipping.
- **Display-referred** = 0–1, already mapped for a screen (sRGB/Rec.709). An 8-bit
  PNG or the final H.264 lives here.
- **The view transform** (AgX in Blender 4.5, or Filmic, or Standard) is the
  function that maps scene-referred light to a display. **Grade before the view
  transform, in linear**, then view through a fixed transform. If you grade a
  display-referred PNG you're pushing already-clipped values and highlights band.

**Practical rule:** do the real grade on the linear EXR in the compositor with a
fixed view transform (pick AgX or Filmic for the show and never change it
mid-series); reserve ffmpeg for a light, last-mile display-referred trim at
delivery, not the primary grade.

## The primary tools

**Lift / Gamma / Gain** (the colorist's three-way) — the `Color Balance` node in
Blender (set to Lift/Gamma/Gain mode) or ffmpeg `colorbalance`/`curves`:

- **Lift** → shadows/black point. Push lift blue for a cold night, lift it up to
  fade blacks for a dreamy/drained look, crush it down for contrast.
- **Gamma** → midtones (skin, fills, the bulk of a cel frame). Most mood lives
  here — warm the gamma gold for a nostalgic scene, pull it green for the void.
- **Gain** → highlights/white point. Tint the gain to color the light source
  (gold key, sickly green LIVE light), or pull it to tame blown emissives.

**Curves** — for shaping contrast and per-channel crossovers (classic teal-shadow
/ warm-highlight split: lift the red curve in highlights, the blue in shadows).
On a cel show use curves gently: the image is already stepped by the toon ramp,
and an aggressive S-curve will posterize the fills.

**Hue/Sat** — global saturation to set richness per mood (sepia-crush the drained
scenes, push saturation in the gold ones), plus `Hue Correct` for a single
problem hue.

## Mood via grade (serving the color-script)

The `color-script` assigns each sequence a palette and emotional temperature.
The grade is how you hit it on the actual render:

- **Gold / nostalgic:** warm gamma + gain, lifted-but-not-faded blacks, full
  saturation. Sunlight memory.
- **Drained / dread:** desaturate, sepia/green bias in midtones, slightly crushed
  highlights — the color leaving the world.
- **Void:** crushed blacks, green push in shadows, minimal saturation except the
  emissive accents.
- **Un-gold** (the gold palette gone wrong): the gold grade with the warmth pulled
  to a sickly cast — same hue family, inverted feeling.

Build each as a **named master grade group** and reuse it; a mood is a reusable
grade, never re-eyeballed per shot (this is the consistency law — see below).

## Matching shots in a sequence

Two shots cut together must feel like one light. Process:

1. **Pick a hero/anchor shot** per scene — the one that nails the intended look.
   Grade it fully first; it's the reference.
2. **Grade neighbors to the anchor**, not to their own isolated "nice." A shot
   that looks great alone but jumps on the cut is wrong.
3. **Match on scopes, not just eyes** (next section). Line up black points,
   white points and the dominant skin/fill hue across the cut.
4. **Account for shot content:** a CLOSE and a WIDE of the same moment have
   different average brightness; match the *light intention* (black point, key
   color, saturation), not the raw histogram.

## Scopes — don't grade by eye alone

Your monitor lies (ambient light, calibration, fatigue). Read the signal:

- **Waveform** → tonal placement. Set a consistent black point (where shadows
  sit) and white point across a scene; it's the fastest shot-match tool. Watch
  that emissives (screen-faces, HUD) don't illegally clip the top.
- **Histogram** → overall exposure balance and clipping at either end.
- **Vectorscope** → hue and saturation. The dominant mood hue should point the
  same direction across every shot in a scene; skin-equivalent (the fill on a
  character's face) should sit on a consistent line.
- **Parade (RGB)** → per-channel balance for neutralizing or deliberately tinting;
  the tool for a precise teal/orange split.

In Blender, use the compositor's `Viewer` + the image editor's Scopes panel; in
ffmpeg, render a `waveform`/`vectorscope` filter preview to eyeball a batch.

## Consistency across an episode (and the series)

At ~870 shots this is the whole game:

- **Grades are locked node groups, appended, not rebuilt.** One group per mood,
  stored in the show's versioned `comp/` library. Changing the mood = edit the
  group once, every shot updates.
- **Fixed view transform + fixed working space** for the entire series. Switching
  AgX↔Filmic mid-season re-renders the feeling of every prior shot.
- **A light-rig-tied grade:** because locations have locked light rigs
  (`character-consistency`), the per-location grade is stable — grade the location
  once, reuse per shot there.
- **Keep an ungraded intermediate** so a note like "the whole void sequence is too
  green" is a group tweak + re-encode, never a re-render.

## Don't fight the cel ramp

The single most common cel-grading mistake: treating the stepped toon image like
a photographic plate.

- The toon shader already quantizes light into 2–4 bands. A heavy contrast grade
  **widens the gap between bands** and the fills posterize / band visibly.
- If a shot's tone is wrong, the fix is usually **upstream** — the light rig, the
  ramp, the shader (`cel-shading`, `lighting`) — not a violent curve in the grade.
- Grade for *hue and black/white point* on cel fills; save strong contrast
  shaping for the continuous-tone elements (painted BGs, FX, atmosphere).
- Protect the ink line: grade `toon_fill`, treat `toon_line` separately
  (`multipass-compositing`), so the grade never muddies the line.

## Delivery trim (ffmpeg)

The primary grade is baked per shot in comp. At delivery do only a light global
pass if the assembled cut needs a unifying touch, e.g.:

```bash
ffmpeg -i cut.mov -vf "curves=preset=medium_contrast,eq=saturation=1.03" \
  -c:v libx264 -crf 16 -pix_fmt yuv420p graded.mp4
```

Keep it subtle (`crf 16` intermediate, not the final YouTube encode) and feed the
result to `youtube-master`. The final delivery is display-referred Rec.709/sRGB.

## LUTs: bake a mood, apply it fast

Once a per-mood grade group is locked, you can bake it to a **3D LUT** (`.cube`)
and apply that instead of the full node tree — useful for previews, for a
consistent on-set/on-animatic look, and for a fast ffmpeg path:

- Bake by running an identity Hald CLUT image through your grade group and saving
  the result as a `.cube`, or author the LUT in the grade tool.
- Apply in Blender via a `File Output`-staged LUT, or in ffmpeg with the
  `lut3d` filter:

```bash
ffmpeg -i shot.mov -vf "lut3d=file=gold.cube" -c:v libx264 -crf 16 out.mp4
```

- A LUT is a **shortcut to a locked look, not the authoring tool** — it bakes in
  one transform and can't do the masked, per-element work the node graph does
  (`multipass-compositing`). Author in nodes; bake a LUT for speed and
  portability. And a LUT is display-space-specific: a `.cube` built for one view
  transform/working space is wrong under another, so pin it to the show's fixed
  space like everything else.

## Verify

1. Open a graded shot's scopes: the mood hue points one consistent direction on
   the vectorscope, and no emissive illegally clips the top of the waveform.
2. Cut your anchor shot against its graded neighbor in the sequence: black points,
   white points and dominant hue line up on the waveform/vectorscope — no visible
   jump at the cut.
3. Toggle the mood grade group off/on: it's a single appended node group, and
   editing it updates every shot in that mood (not a per-shot tree).
4. Zoom into a graded cel fill at 200%: the toon bands are intact and smooth, not
   posterized/stair-stepped by the grade.
5. Confirm the working space/view transform (e.g. AgX) is identical to the one
   used on an earlier episode's shots — pull one up side by side and they match.
