---
id: creative-arts.animation.blender.multipass-compositing
name: multipass-compositing
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, multipass, aov, cryptomatte, depth-fog, defocus, relight, mattes, cel, node-group, eevee-next]
level: advanced
status: draft
description: "Assemble a shot in the Blender compositor from AOVs/cryptomatte: local grades, depth atmosphere/DOF, element isolation, FX+BG+character integration, cel-safe."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Multipass compositing (assembling the shot from passes)

**Goal:** take the Multilayer EXR from `render-aov-passes` and *build* the final
frame in the Blender compositor — grading, relighting and isolating elements per
pass instead of pushing one flat image around. This is the step above
`compositing-grade`: that skill is the single-graph finishing polish (glow,
grain, vignette) applied to an assembled frame; this skill is how you assemble
that frame from components in the first place, and how a feature comp pass keeps
30 shots in a sequence looking like one film.

## The comp graph, in layers

Read the graph bottom-up as a stack. Each layer is a node group appended from the
show's `comp/` library (versioned with the show, never re-authored per shot):

```
[EXR MultiLayer in]
   ├─ Combined        (reference only; muted in final)
   ├─ Emission ───────────────► glow build ─┐
   ├─ Mist / Depth ──► atmosphere + DOF ─────┤
   ├─ Crypto (char)──► char local grade ─────┤
   ├─ toon_line ─────► line treatment ───────┤
   └─ toon_fill ─────► fill grade ───────────┴─► combine ─► [compositing-grade finish] ─► out
```

The principle: **rebuild the beauty from components, don't repaint Combined.**
Combined is the sanity check you A/B against; the delivered image is the sum of
graded parts.

## Local grades with cryptomatte (the core move)

A feature colorist never grades the whole frame when the note is "warm up the
character." You isolate.

1. `Cryptomatte` node, input the `CryptoObject`/`CryptoAsset` layers, eyedrop the
   character (or type the asset name). Output is a clean, antialiased alpha.
2. Feed that alpha as `Fac` into a `Mix` between the ungraded plate and a
   `Color Balance` (lift/gamma/gain) of the character only.
3. Repeat for the set, the sky, the prop. Each element gets its own
   `Color Balance`, all gated by its matte.

This is per-element grading with pixel-exact mattes that respect hair, motion
blur and the emissive HUD edge — impossible with a hard object-index mask. Tie
each element's grade to the per-mood master group (gold / drained / void /
un-gold) from `color-grading` so the isolation serves the sequence look, not a
one-off.

## "Relight" in comp without re-rendering

You can't add a real light in comp, but with the shading passes you can rebalance
the ones you rendered:

- **Dim/boost the fill:** if EEVEE wrote a usable diffuse-direct vs environment
  split, scale the environment (ambient) contribution down to deepen the key, or
  up to lift crushed shadows — then re-add Emission on top. This recovers a
  "too flat / too contrasty" note without a render.
- **Push emissive key:** multiply the Emission pass before recombining to make the
  screen-face read as the dominant light in a dark shot (the self-lit-character
  problem from `shot-renderer`), rather than re-rendering with a brighter shader.
- **Kill a blown highlight:** mask the hot region via cryptomatte + luminance key
  and pull gain locally.

Honest ceiling: this is *rebalancing rendered light*, not new light. A missing
rim or a wrong key direction is a re-render (or a hand-painted fix), not a comp
fix. Know the line.

## Depth: atmosphere and DOF from Mist/Z

Both come free from the data passes:

- **Atmospheric perspective:** `Mix` the plate toward the set's haze color using
  the **Mist** pass as `Fac`. Far geometry desaturates and lifts toward the fog
  color; near characters stay saturated. A `ColorRamp` on Mist before the Fac
  shapes where the fog starts biting — keep the character end near 0 so faces
  never fog.
- **Depth of field:** `Defocus` node driven by the **Z** pass (or convert Z→
  `Bokeh Blur`). Set the focus distance to the character's Z; comp DOF is far
  cheaper to iterate than EEVEE's in-render DOF and lets the director re-rack
  focus as a note. For a cel show keep it gentle — heavy bokeh fights the flat
  aesthetic.
- Order matters: apply atmosphere **before** DOF so haze is in the plate the blur
  samples, and apply both **before** the glow/grain finish.

## Integrating FX, backgrounds and characters

A shot is rarely one render. The comp is where the beauty render, a separate FX
pass (smoke, the seam glitch, sparks — see `fx`), and a painted/2D background
meet:

- Render FX on its own view layer / pass with alpha; `Alpha Over` it onto the
  beauty at the right depth. Use the **Z** passes of both layers with a `Z Combine`
  node so FX behind a character is correctly occluded instead of floating on top.
- A 2D/matte-painted background plugs in under the character via its cryptomatte
  alpha; grade it with the same per-mood group so the painted BG and the rendered
  character share one grade and don't read as two media.
- Diegetic UI (the engagement-counter HUD, `hud-engagement-counter`) comes in as
  its own element with its own bloom curve off its `id_face`/Emission mask, so its
  analog flicker and glow are tuned independently of the character behind it.

## Keeping the cel look through comp

Multipass power makes it easy to over-render the image into "3D CG." Guard the
flat cel aesthetic:

- **Grade the fill, protect the line.** Do color work on `toon_fill`; treat
  `toon_line` separately (recolor per mood, adjust thickness) so grades never
  smear or desaturate the ink. Recombine line over fill with `Alpha Over`.
- **Don't let DOF/fog round off the 2D read** — keep both subtle; the cel look is
  crisp shapes, not photographic falloff.
- **Bloom only emissives** (via the Emission mask), never a frame-wide glow that
  hazes the flat fills.
- **Don't fight the toon ramp with the grade** — if a shot reads wrong, fix the
  lighting/ramp upstream, not with a violent curve that bands the cel steps
  (see `color-grading`, `cel-shading`).

## Make it a reusable group, not a per-shot graph

With ~870 shots across the series, a bespoke node tree per shot does not scale
(the `shot-renderer` lesson applied to comp):

- Build one master comp group per mood containing: pass-split, atmosphere, the
  element-grade sockets, line/fill handling, and an exposed `Fac`/strength input.
- Append it into every shot of that mood; the only per-shot work is eyedropping
  the right cryptomatte asset and setting the focus distance. Same group = same
  look = a sequence that holds together.
- Keep an **ungraded intermediate** render available so a sequence-wide re-grade
  is a group edit, not 30 re-renders.

## Render-time vs comp-time (what to decide where)

The whole value of multipass is deferring decisions to the cheap domain. A quick
rule for every look choice:

| Decision | Where | Why |
|----------|-------|-----|
| Geometry, animation, real light direction/rim | render | can't be faked from passes; a re-render |
| Glow / bloom strength & threshold | comp | off Emission pass, instant |
| Fog density, atmospheric desat | comp | off Mist pass |
| Depth of field / focus rack | comp | off Z pass, director-tweakable |
| Per-character / per-element grade | comp | off cryptomatte |
| Line thickness / line recolor | comp | off toon_line AOV |
| Fill mood grade | comp | off toon_fill AOV |
| Ambient/key *balance* (within rendered light) | comp | shading-pass rebalance |
| New light, missing rim, wrong key | render | not recoverable from passes |

If a note can be answered in the right-hand column, it's a node tweak the
director sees in seconds; only the two render rows cost a frame. Designing the
pass stack (`render-aov-passes`) is really designing which decisions you keep
cheap.

## Gotchas

- **Cryptomatte picks drift if the asset renames.** The node stores a name/hash;
  rename a locked asset (`asset-management`) and the matte goes black. Pick by the
  stable asset name and re-verify after any asset version bump.
- **Z Combine aliases** on hard edges — add a tiny anti-alias/erode on the FX
  alpha or composite FX with its own alpha over a Z-sorted stack rather than a raw
  per-pixel Z test on thin elements.
- **Mist used as DOF** — don't. Mist is 0–1 over a clamped range; use real **Z**
  (metric) for `Defocus` or focus will be wrong past your mist Depth.
- **Working in the wrong color space** — the compositor operates on the linear EXR
  (scene-referred). Keep the view transform (AgX/Filmic/Standard) consistent with
  what `color-grading` and delivery assume, or shots graded on different days
  won't match.

## Verify

1. Mute the comp's output chain and view **Combined**; then view your rebuilt
   `combine` node. They should match tonally before any grade — proving you
   recombined the passes correctly (not accidentally double-adding Emission).
2. Eyedrop the character in the Cryptomatte node and push its local
   `Color Balance` hard (e.g. gain → red). Only the character shifts, including
   hair edges; the set and sky are untouched.
3. Scrub the shot: depth fog is present on far geometry and absent on the
   character's face; DOF focus holds on the character as they move.
4. Toggle the FX layer's `Z Combine`: FX that should be behind the character is
   occluded, not floating.
5. Append the same mood comp group to a second shot in the sequence, set its
   cryptomatte + focus, and confirm the two shots read as one grade side by side.
