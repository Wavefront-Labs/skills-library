---
id: creative-arts.animation.motion-graphics.hud-engagement-counter
name: hud-engagement-counter
category: creative-arts
field: animation
product: motion-graphics
tags: [motion-graphics, hud, diegetic, engagement-counter, emissive, flicker, overlay, blender, compositor, ui]
level: advanced
status: draft
description: "The diegetic floating engagement-counter HUD: an emissive mint numeral + 'watching' tag that billboards by a character's head with analog flicker and drift."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hud-engagement-counter — the diegetic "watching" HUD

**Goal:** the show's signature diegetic element — a soft-edged mint `#5fe39b`
numeral + a pulsing dot + the word `watching`, hanging at head height, screen-right
of a subject. It reads as a thing *in the world* (a view-count hovering over a
person like a left-on TV), not a graphics overlay. Only one character begins to see
them; they live in a "blind spot" until an Act-3 reveal. Emissive, with analog
flicker and a never-clean drift.

## In this pipeline

The mint `#5fe39b` is the show's HUD/seam colour (shared with the title-card accent
in `series/production/build_fx.py`). The glow that sells it is **not** baked into
the element — it comes from the shared beauty comp,
`series/production/blender/shotkit.py` → `beauty_comp()`, whose Fog Glow
(`threshold=1.0`, `mix=0.10`) blooms the emissive numeral exactly like any other
hot source in the frame. So: author the HUD at the right emission strength, render
it in the shot pass, and let the existing glare bloom it — don't add a second glow.
The 2D-overlay fallback (below) uses the same `drawtext` craft and Windows fontfile
escaping as `title_card()`.

## Two ways to place it (choose by whether it must stick to a moving head)

**A — 3D-anchored billboard (correct for moving subjects).** Build it in Blender so
it tracks and takes the shot's comp/grade:

- An **Empty** parented to (or copy-location-constrained to) the character's head
  bone, offset screen-right and slightly behind the look direction (the blind spot).
- Parent to that Empty: a **Text object** (the number), a small **disc** (the dot),
  and a smaller **Text** (`watching`).
- **Billboard** each toward the camera with a `TRACK_TO` constraint (track Z to the
  active camera, up = world Z) — or `LOCKED_TRACK` if you want it to yaw but stay
  upright. Without this it edge-ons as the subject turns and vanishes.
- **Mint Emission material**: shader = Emission, colour `#5fe39b`, `strength ≈ 6`.
  Emission (not a lit diffuse) so it's self-lit and consistent regardless of the
  scene light rig, and so it clears the Fog Glow `threshold=1.0` and blooms.
- It renders in the **same pass as the shot**, so it tracks pixel-perfect and the
  beauty comp glows/grades/grains it identically to the world. This is the one that
  looks real.

**B — 2D overlay (fast, for near-static subjects).** Composite a mint number +
`watching` over the shot — Blender compositor Text node, or ffmpeg `drawtext`
positioned by hand per shot:

```bash
drawtext=fontfile='C\:/Windows/Fonts/consola.ttf':text='1,204':fontcolor=0x5fe39b:
fontsize=46:x=w*0.62:y=h*0.30:alpha='0.9+0.1*sin(2*PI*t*7)'
```

Note the escaped drive colon (as in title-cards). Cheap, but it does **not** track a
moving head and won't sit under the same lens distortion — use only when the subject
is locked off.

## The look (sell "left-on TV")

- **Colour** mint `#5fe39b`; let the beauty-comp glare bloom it slightly — do not
  pre-blur it, the glow belongs to the frame, not the asset.
- **Analog flicker** — animate Emission strength with a tiny noise/sine so it never
  sits still, e.g. a driver `strength = 6 * (0.9 + 0.1*sin(2*pi*frame/fps*7))`, plus
  an occasional **1-frame near-dropout** (strength → ~1) every second or two. The
  dropout is what makes it read "electronic," not "glowing paint."
- **Drift, never a clean count** — the number slowly increments/jitters; animate the
  displayed value so it ticks irregularly (e.g. +1 every 10–40 frames, sometimes a
  small backwards flicker), and let the whole element **drift** a few px in position
  on a slow noise so it floats rather than locks.
- **Readability guardrails**: keep it legible despite the flicker — floor the alpha
  (never below ~0.75 except the deliberate 1-frame dropout), keep `fontsize` large
  enough to survive the 1080p→phone downscale, and keep it off busy background
  detail so the mint always separates.

## Animating value changes

- For an **anchored** HUD, drive the number from a text property / driver so a single
  value updates everywhere; step it on 2s or 3s (not every frame) so it reads as a
  counter, not a stopwatch blur.
- For a **big jump** (a beat where attention spikes), snap the value and punch
  emission strength up ~1 frame, then settle — a tiny "notification" kick.
- Keep digit width stable (a mono face, or tabular figures) so the number doesn't
  jitter horizontally every time a digit changes.

## Compositing it right (rendered-separately route)

If the HUD is rendered on its own layer (a separate view layer / render pass) rather
than in the main beauty pass, composite it back with an **Alpha Over**, placed
*before* the beauty comp's glare so the Fog Glow blooms the comped-in mint the same
as everything else — comp it after the grade and it reads as a flat sticker.

- **Occlusion**: decide per shot whether the subject's head/hair should pass in front
  of the HUD. For a believable "floating behind the ear" placement, give the head a
  **holdout** on the HUD layer (or Z-composite using the mist/Z pass from
  `creative-arts.animation.blender.multipass-compositing`) so the character can
  briefly eclipse the element — a HUD that never occludes looks pasted on.
- **Emission value under Standard**: the comp assumes `view_transform='Standard'`
  (see `creative-arts.animation.blender.compositing-grade`); tune emission strength so
  the mint sits just above the glare `threshold=1.0` — strong enough to bloom, not so
  hot it clips to white and loses the colour.
- **Blind-spot masking**: an ellipse/garbage mask can hold pre-reveal counters at low
  opacity in the frame edge so they're half-seen, then be keyed off on the reveal
  shot — one asset, two visibility states.

## Reveal logic

- **Pre-reveal**: counters present on extras but framed in blind spots / low opacity,
  so the audience half-notices without clocking them. Keep them screen-right and
  slightly behind the look direction.
- **Reveal shot**: push one to full strength, in focus, allowed **dead-centre** — the
  first time the HUD is unambiguous. After that, framing can treat them as normal
  diegetic elements.

## Verify

- [ ] Mint `#5fe39b`, emissive `strength ≈ 6`, soft glow coming from the beauty-comp
      glare (not a baked blur) — reads as "on top of" the world.
- [ ] Anchored version **billboards** to camera and tracks the head across the whole
      shot without sliding or edge-oning.
- [ ] Flickers (sine + occasional 1-frame dropout) and **drifts/jitters** — never a
      crisp static number.
- [ ] Still legible at play speed and at phone scale (alpha floored, large enough,
      off busy detail).
- [ ] Digit width stable as the value changes (no horizontal jitter).
- [ ] Hidden in the blind spot pre-reveal; pushed full/centre only on the reveal shot.

status draft: the design is locked (mint element, flicker/drift, blind-spot reveal)
and the glow path is verified (blooms via `shotkit.beauty_comp`), but the 3D-anchored
billboard is not yet built in Blender for a shot. See
`creative-arts.animation.blender.compositing-grade`,
`creative-arts.animation.blender.camera-cinematography`,
`creative-arts.animation.motion-graphics.title-cards`.
