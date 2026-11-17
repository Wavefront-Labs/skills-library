---
id: creative-arts.animation.comfyui.background-master-from-blockout
name: background-master-from-blockout
category: creative-arts
field: animation
product: comfyui
tags: [comfyui, img2img, background, scenery, painted-background, blockout, layout, locked-camera, denoise, hires-fix, animagine-xl, anime, master-plate, draw-once, consistency, directml]
level: practitioner
status: verified
description: "Paint one anime-quality master background per camera setup by img2img over the locked-camera blockout render: denoise 0.80 keeps the layout, a 0.35 hires pass adds detail for close-up crops."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Background master from a blockout (img2img, one per setup)

Verified on three locations (alley, kitchen, main street) beside Dragon Ball Daima
frames. Procedural per-surface painters produced flat plates judged "not
appealing"; this route produced painted backgrounds a cold viewer placed in the same
medium as the benchmark, while keeping the 3D set's layout so every character mark
and eyeline still lands.

## Why it stays consistent
Scenery is painted ONCE per camera setup (the widest framing of a location), and
every shot of that setup is a crop, pan or push of the one image. Nothing is
regenerated per shot, so there is no drift. One location needs 1–3 masters (one per
locked camera), not one per shot.

## Graph (API JSON)
CheckpointLoaderSimple → CLIPTextEncode ×2 → LoadImage(blockout) → ImageScale
(1344×768 lanczos) → VAEEncode → KSampler → VAEDecode → SaveImage.
Sampler `dpmpp_2m`, scheduler `karras`, cfg 5.5, 30 steps (see
`creative-arts.animation.comfyui.anime-character-master-on-amd-directml` for the
install and the stripe-artifact fix).

## Denoise is the whole decision
- **0.55**: stays a tinted blockout — flat grey walls, no paint. Useless.
- **0.75–0.80**: the sweet spot. Walls, dumpster, pipes, posters, light and haze are
  painted; the camera, horizon and big masses follow the blockout. Use 0.80 for a
  wide master.
- **0.90**: beautiful but the layout drifts (a deep alley became a flat wall with a
  row of bins). Only for reference moods.

## Prompt shape
`anime background art, <location in 6–10 nouns: walls, props, fixtures>, <time of day
light: "late afternoon sunlight raking across the wall, long warm shadows, soft haze">,
detailed painted background, scenery, no humans, masterpiece, high score, great score,
absurdres`. Negative: `people, 1boy, 1girl, person, character, text, watermark,
signature, lowres, worst quality, low quality, jpeg artifacts, blurry, 3d render,
photo, realistic`. Name the props the set actually has; the model keeps them where
the blockout puts them.

## Hires pass for close-ups
Feed the chosen master back as the image at 1.5× (2016×1152) with **denoise 0.35**,
same prompt and seed. ~150 s on an RX 6900 XT via DirectML. Crops for CLOSE setups
come from this image (a 1716×965 crop scaled to 1920×1080 held up at full screen).

## When the blockout is the problem (refining a weak master)
A master that reads flat (one orange wall, no light, naive lines) cannot be rescued by
more denoise over the same blockout: at 0.45 nothing changes, at 0.65-0.75 props and a
sky appear but the flat colour and missing light stay, because the blockout IS the
colour and light. Decide by what is wrong:
- **Soft / too small** (1344 wide stretched to 1920): hires pass at 2016×1152, denoise
  0.35, same prompt and seed. Same picture, crisp. (~225 s per image on the RX 6900 XT.)
- **Lighting flat but layout right** (a frontal storefront row): 0.5 with a lighting
  prompt ("late afternoon golden sunlight raking across the facades, long warm shadows,
  cool blue shade") and "sketchy lines, messy lines, text, signage text" in the
  negative. 0.6 gains light but the lines go scratchy and the cars lose their shape.
- **Design wrong** (no light source, no materials, nothing to look at): generate a NEW
  master by txt2img at 1344×768 with the lighting in the prompt ("strong late afternoon
  sunlight streaming through the window, long shadows across the counter"), two or
  three seeds, pick one, then the 0.3 hires pass to 2016. Staging only needs the
  counter height and the window; it does not need the old layout. Keep the location's
  nationality in the prompt ("American small town main street"): without it the model
  paints European lanes with foreign signage.
- A 2016×1152 `VAEDecode` can fail with "not enough GPU video memory"; use
  `VAEDecodeTiled` (tile 512, overlap 64), identical output.
- Generated masters carry a signature scrawl bottom-right; paste a feathered patch of
  neighbouring ground over it before any wide shot crops it in.

## Turning a master into a shot plate
For a close-up: crop so the wall sits behind the head and a prop anchors the lower
corner; Gaussian blur radius ≈ 2 px (shallow focus); 8 % warm overlay matching the
key; soft vignette (dark corners, opacity ~0.5). Characters are then composited sharp
over it — the sharp/soft split is most of the "cinematic" read.

## Verify
Beside a benchmark background at 640 px: a cold viewer names the same medium;
`look_metrics` shadow share within 1.5× of the benchmark; the character marks from
the shotlist still land on floor, not wall. Keep the base render next to the master
so the layout can be checked.
