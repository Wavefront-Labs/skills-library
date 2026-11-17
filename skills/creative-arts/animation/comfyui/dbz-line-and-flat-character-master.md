---
id: creative-arts.animation.comfyui.dbz-line-and-flat-character-master
name: dbz-line-and-flat-character-master
category: creative-arts
field: animation
product: comfyui
tags: [comfyui, animagine-xl, sdxl, anime, dragon-ball, toriyama, 1990s-anime, cel, line-art, flat-color, character-master, bust, full-body, paper-colour, consistency, txt2img, img2img, head-turn]
level: practitioner
status: verified
description: "Prompt Animagine XL 4.0 for a 1990s Dragon Ball style line+flat character master (closed outlines, flat fills, Toriyama eyes): bust and body framings, paper colour, what fails (head turns)."
sources: [https://huggingface.co/cagliostrolab/animagine-xl-4.0]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# DBZ line-and-flat character master from Animagine XL

Verified 22 Oct 2026 (RX 6900 XT, DirectML, ComfyUI v0.3.59; ~80 s per 1024×1024,
~50 s per 832×1216). Setup and sampler: `anime-character-master-on-amd-directml`.

## Why this instead of a painted master
A painted/soft anime still (default Animagine look) cannot be turned into a cel
drawing afterwards: colour tracing gives blobs, no outline layer, and parametric
features stacked on painted skin read as two styles. Asking the model for the
**line + flat** style directly gives a master that already is a cel: closed black
outlines, flat fills, one shadow tone, Toriyama eye construction (thick upper lid,
small dark iris, one highlight), drawn ear, nose and jaw.

## The tags that do it
Append to the character description:

```
toriyama akira \(style\), dragon ball z, 1990s \(style\), retro artstyle, anime screencap,
flat color, bold black outlines, cel shading, simple background, <paper colour> background
```

Keep the sampler from the base skill (`dpmpp_2m` + `karras`, cfg 5). With these style
tags `flat color` / `cel shading` are correct and necessary; the earlier warning
against them applied to the painted look only.

## Framing per use
| Use | Add to prompt | Size | Result |
|---|---|---|---|
| Bust (close-ups) | `portrait, upper body, facing viewer, looking at viewer` | 1024×1024 | head ≈ 600 px tall, shoulders in frame |
| Body (medium/wide) | `cowboy shot, standing, arms at sides, full body visible to the knees, small head` | 832×1216 | whole figure, head ≈ 150–310 px |

- Elderly/wrinkled descriptions pull the model to a **tight head** even with "upper
  body": accept the head-only bust and take shoulders from the body master.
- "Dark skin" needs reinforcing (`dark skin, brown skin, very dark skin`) or the
  model lightens it; "kind/gentle closed-mouth smile, warm expression" prevents the
  villain grin it defaults to for old men.

## Hi-res head pass
Crop the body master's head tight, scale to 1024, img2img denoise 0.3, same tags +
`portrait, face`: a crisp close-up head identical to the full figure's (~85 s).
Denoise 0.3 keeps every line; the paper comes back textured, so cut by silhouette.

## Mascots
`cute simple mascot robot, head is a cream vintage CRT television set, ... solo, 1robot`
plus the style tags gives a Dr. Slump-style robot; 3 of 6 seeds added gadgets or
extra figures, one was clean.

## Paper colour
Ask for `light blue background` whenever the hair or costume is white/cream (the
cut-out cannot separate white hair from white paper). Pure white paper is fine for
dark-haired characters. Avoid off-white paper: the model shades it per region and the
pockets beside the head come out cream, not white.

## What does NOT work (measured)
- **Head turns.** Same seed + "three-quarter view" changed hair and eye colour; img2img
  from the front master at denoise 0.55–0.70 kept identity but stayed front-facing;
  a horizontally squeezed/sheared copy as img2img base at 0.75 gave a slight turn with a
  different eye. Treat the front master as the only head; fake 3/4 downstream.
- **Colour across generations drifts** (a "light blue hoodie" came out mint in the
  body master, blue in the bust). Recolour body flats to the bust palette afterwards
  (`pipeline.cel-character-from-generated-master`).
- Seeds give different faces: generate 2–4, pick one, never regenerate.

## Verify
- 100 % zoom: every outline closed, no gradients inside fills, iris is a flat dark
  shape with one highlight.
- Border pixels are paper colour on at least the top corners (needed for the cut-out).
- Side by side with a Dragon Ball frame at the same head size: line weight and eye
  construction match before any animation work starts.
