---
id: creative-arts.animation.art-direction.color-script
name: color-script
category: creative-arts
field: animation
product: art-direction
tags: [color-script, colour, palette, color-keys, mood, lighting-plan, sequence, emotion, value, temperature]
level: advanced
status: draft
description: "Plan a film's colour and value beat by beat: sequence-level color keys that drive mood, contrast and lighting before any shot is lit."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Color Script — the emotional map of the episode

A color script is a strip of small, loose paintings (one per beat/sequence) that fixes
the **value and colour arc of the whole episode before a single shot is lit.** It is
the difference between an episode that *feels* like it goes somewhere and one where
every scene is lit the same neutral way. Pixar builds one per film; a YouTube series
needs a lightweight one per episode. It is an art-direction deliverable, downstream of
the show bible's palette, upstream of per-shot lighting.

## 1. Why value first, colour second
- Thumbnail each beat in **greyscale** first. If the value composition (where the eye
  goes, foreground/background separation, contrast level) doesn't read in grey, colour
  won't save it. Most "flat" frames are value failures, not colour failures.
- Each key is tiny (160px) and loose — you are planning *relationships*, not painting.
  Squinting at the strip should show the episode's contrast rhythm.

## 2. The arc (plan contrast and temperature as a curve)
Lay the beats left-to-right and design deliberate change:
- **Temperature arc** — warm/safe scenes vs cool/threat scenes; a cold dread scene lands
  harder if the scene before it was warm. Map temperature to story, don't default it.
- **Contrast/key arc** — high-key (bright, low contrast) for ordinary, low-key (dark,
  high contrast) for tension/reveal. A reveal in the same key as the setup has no punch.
- **Saturation arc** — drain saturation for bleakness, spike one saturated accent
  (a signal colour) at the emotional hit so it pops. Reserve a colour for meaning.
- **Palette continuity** — pull every key from the show bible's locked swatches; the
  color script shifts their *lighting and ratio*, it does not invent new hues per scene.

## 3. From key to shot (what it drives)
Each color key becomes the brief for that sequence's lighting + comp:
- key light colour/temperature and intensity ratio to fill,
- background value (explicitly: NOT blown to white — a blown background is a value
  failure the color script should catch and forbid),
- the one accent/signal colour and where it appears,
- grade target (the comp pushes toward the key, it doesn't fight it).
Hand the key + the greyscale thumbnail to the lighter as the pass/fail reference.

## 4. For a cel show specifically
Cel shading uses discrete tone bands (see cel-shading), so the color script decides:
- the **shadow hue** per scene (cool shadows in a cold scene, warm in a sunset),
- the band ratio (how much of the frame is in shadow band = mood),
- the environment fill colour that tints everything (bounce), which keeps characters
  sitting *in* the scene instead of pasted on.

## Verify
- [ ] A one-strip color script exists for the episode, one key per sequence/beat.
- [ ] Each key reads in greyscale first (value composition holds without colour).
- [ ] Temperature/contrast/saturation change deliberately across the strip (not uniform).
- [ ] Every key's hues trace back to the show-bible palette (no rogue colours).
- [ ] No key has a blown-white background; each names its background value.
- [ ] Each lit sequence matches its key side-by-side (the key is the lighting brief).

See look-development (parent bar + palette), lighting (executes the key per shot),
compositing-grade (grades toward the key), cel-shading (tone bands + shadow hue).
