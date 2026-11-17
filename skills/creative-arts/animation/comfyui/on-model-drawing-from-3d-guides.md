---
id: creative-arts.animation.comfyui.on-model-drawing-from-3d-guides
name: on-model-drawing-from-3d-guides
category: creative-arts
field: animation
product: comfyui
tags: [comfyui, controlnet, controlnet-union, ip-adapter, sdxl, animagine, consistency, character-consistency, 3d-guide, frame-by-frame, head-swap, quality-gate, amd, directml]
level: advanced
status: draft
description: "Draw a 2D character frame by frame from 3D motion on SDXL: ControlNet union lineart guide, IP-Adapter identity, cel head swap, and a consistency gate that rejects drift."
sources: [https://huggingface.co/xinsir/controlnet-union-sdxl-1.0, https://github.com/cubiq/ComfyUI_IPAdapter_plus]
licence: Apache-2.0
version: 7
updated: 2026-11-17
aliases: []
---

# On-model drawing from 3D guides

**Goal:** frame-by-frame anime drawings whose motion comes from a 3D pass (correct walk, contact and hands)
and whose look stays on the character's model sheet. Generation on its own draws a different character
every frame. This skill is the set of constraints and the gate that make it usable.

## Stack (local, AMD on Windows via DirectML)

- Animagine XL 4.0 checkpoint.
- `xinsir/controlnet-union-sdxl-1.0` promax: one file covering openpose, depth and lineart modes, selected
  with the `SetUnionControlNetType` node.
- IP-Adapter plus SDXL with the ViT-H image encoder, via `ComfyUI_IPAdapter_plus`. Restart ComfyUI after
  installing the node.
- About 75 to 100 s per 832×1216 drawing on an RX 6900 XT.

## Guide from the 3D pass

Render the rigged character with a transparent film, a toon shader and outlines. Crop **all frames of a shot
with one union box**: a per-frame crop makes the figure jump. Then turn it into Canny edges, white on black,
for the union model's lineart mode.

## Settings that held (and the ones that didn't)

| Setting | Defaults | Held |
|---|---|---|
| ControlNet strength / end | 0.8 / 0.8 | **1.0 / 1.0** |
| IP-Adapter weight / type | 0.8 linear | **0.6, "style transfer precise"** |
| Prompt | character tags | + **"solo"**, "bold black outlines, thick lineart, flat colors" |
| Seed | — | fixed per shot |

With the defaults, the pose followed the guide, but the hair and face changed every frame, and the reference
image put **extra heads** in empty parts of the frame. The settings above produced one clean figure with a
steady outfit, but a generic face.

## Faces: don't generate them

Keep the generated body and replace the head with the character's existing cel head (the system that already
holds the face, expressions, mouths and blinks). Size it by the **design's head-to-figure ratio** measured on
the master. Find the neck as the narrowest row in the 8 to 22 % band of the figure, put the chin there and let
the head grow upward. Paint out the generated head first, so no stray hair pokes out. The face then came out
identical across frames.

## Body build drift

The 3D base body was slimmer than the stocky design, and the drawings followed the guide. Widening the guide
horizontally by 1.25× before drawing, with "stocky, heavyset" in the prompt, moved the build ratio from 0.65
to between 0.79 and 0.87 of the master's.

## Consistency gate (run on every drawing)

Score against the master:

- **palette:** the drawing's 8 dominant figure colours against the master's, matched both ways and weighted by
  share. On-model drawings scored 22 to 29; drifted ones 34 to 39. Pass at 30 or below.
- **outside_guide:** the share of the drawing's figure outside the dilated 3D guide silhouette. Frames with
  extra heads scored 0.34 to 0.37; clean frames 0 to 0.13. Pass at 0.08 or below. Measure it on the body
  **before** the head swap, because the design head is bigger than the 3D head.
- **stocky:** figure area divided by height squared, relative to the master. Pass between 0.7 and 1.3.
- **figures:** exactly one large blob. Attached extra heads don't count as separate blobs, which is why the
  guide-silhouette check is needed.

Regenerate failed drawings with a new seed, or fix the guide.

## Full scene test: five beats, 15 drawings (verified 10 Nov 2026)

Every beat of a 2-character grocery-drop scene was drawn from its 3D guide and put through the gate, then reviewed
independently against the scene rubric. What held and what did not:

- **Per-frame generation flickers even with the head swapped in.** The face and pose hold across a 6-frame walk; the
  costume details (badge, tie, cuffs, shoes), the held bag's colour and the trouser shading redraw every frame, so it
  reads as six drawings of one man. IP-Adapter at 0.6 plus a prompt is not a character lock. Next thing to test: fixed
  seed per shot, img2img from the previous drawing at low denoise, and compositing onto the real background plate
  instead of the generated backdrop (the reviewer's single biggest lever; not yet verified).
- **A pair reference blends the two people.** Drawing a two-shot from one reference image holding both masters put the
  old man's cardigan on the woman and her hair turned white. Draw each character on their own guide and reference, then
  composite; never a shared reference.
- **Cropped frames (legs and falling props only) draw well** and follow the guide; the gate had to change for them, see
  below. Hands were illegible in every set at 1344x768: hands need their own pass or a close-up guide.
- **A painted plate from the 3D layout works for a prop beat:** lineart ControlNet at 1.0 from the layout render, no
  character reference (IP weight 0), scenery prompt; the 3D prop frames (orange, rendered with the grate as holdout) are
  alpha-composited over it. Occlusion by the bars needs a motion strip to judge; stills do not show it.
- **One job at a time, foreground:** 6 drawings took 19 m 43 s with up to three gate retries each (about 2 min per
  drawing); 1 drawing 3 m 52 s; 2 cropped drawings 10 m 37 s; a 3-frame two-shot 15 m 53 s. Free system RAM stayed
  between 2.5 and 6.4 GB with ComfyUI on `--highvram --cache-lru 2`, and nothing was killed.

## Two-shots: one character per pass (verified 10 Nov 2026)
The blended pair from a shared reference is fixed by splitting the shot in the 3D layer: render the motion frames twice with
the other rig hidden (`hide_render` on the armature, its children and every mesh whose armature modifier targets it), build
each character's guide set from its own renders (the per-set union crop keeps that character's framing stable), draw each
with its own master as the IP-Adapter image and a solo prompt, then composite both cut-outs on the plate at the 3D
positions. On the crouch beat both came back on model (cardigan and brown trousers on him, brown bob and cream top on
her) where the shared reference had swapped them. Each still drifts alone (a skirt became trousers; a deep crouch hid the
face), and hands stay blobs. Gate note: a kneeling or crouching figure cannot be scored for build against a standing
master (`GATE_BUILD=0`), and a prop in frame (the can) counts as a second figure, so allow it.

## Hands: a hi-res pass cannot add fingers the guide does not have (verified 10 Nov 2026)
Hands were illegible in every 1344x768 / 1216x832 drawing. The obvious fix, crop the hand region from guide and drawing,
upscale to 1024, redraw with lineart ControlNet from the guide crop and img2img (denoise 0.55) from the drawing crop, then
paste back feathered, changed almost nothing: the motion-layer rig's hand is a fingerless mitten, so the guide offers no
finger lines and the model paints a smooth club. Two practical notes: take the crop position from the guide for both
images (the drawing may contain a stray second prop that fools a colour search), and centre the crop on the wrist, not on
the prop the hand reaches for, or most of the crop is empty background at the frame edge. Hands need either finger
geometry in the 3D layer (a hand mesh with bones) or drawn hand cels placed over the wrist, as the body-part program does.

## Gate rules per set type (verified 10 Nov 2026)
The whole-figure gate (one figure, palette <= 30, build 0.7-1.3, outside-guide <= 0.08) is wrong for two kinds of set:
- **Partial frames** (a low camera on legs and props): figure count and build are meaningless, and the props add colours
  the master never had, so the palette cap must be 1.6x (30 -> 48). With that, a good legs frame passed at palette 45;
  a bad one still failed on outside-guide 0.28 (an extra figure).
- **Two-shots:** the pass condition is figures == 2, build is skipped (it is per pair), palette is scored against a
  two-person reference. The blended-identity frames then fail honestly on palette (36-54).
Pass the set type to the gate (environment `GATE_PARTIAL=1`, `GATE_FIGURES=2`) rather than loosening the default.

## Character lock by img2img does not work for moving poses (verified 10 Nov 2026)
The flicker fix everyone reaches for first, feeding an earlier drawing in as the img2img latent with the same seed, was tested
four ways on a 6-frame walk (ControlNet lineart 1.0, IP-Adapter 0.85, seed fixed). Consecutive-frame palette distance and
aligned silhouette IoU (baseline 24.7 / 0.81, retried frames had new seeds):
- **IP-Adapter 0.85 + fixed seed, no init:** 22.0 / 0.72. No change; the adapter is not a lock.
- **Chain, init = previous drawing, denoise 0.6:** 21.6 / 0.82. The costume, bag and boots stayed identical for four
  frames (nothing else achieved that), then the errors compounded: by frame five the backdrop was noise and a ghost head
  appeared. Outside-guide rose 0.07 -> 0.60 along the chain.
- **Anchor, init = frame 1, denoise 0.65:** 16.1 / 0.98, the best numbers, and useless: the drawings kept frame 1's
  pose and ignored the guide (outside-guide 0.58 by the last frame).
- **Anchor, denoise 0.85:** 19.5 / 0.77. Pose follows the guide again but the anchor's silhouette ghosts through as a
  translucent second figure.
- **IP-Adapter with two images (master + previous drawing, `ImageBatch`, concat embeds), weight 0.85:** 22.1 / 0.77. The
  costume held for four frames, then the adapter started inventing (a tail, a stack of boxes). No lock either.
So the img2img latent carries pose as strongly as colour: low denoise freezes the pose, high denoise ghosts it. Use it
only between frames whose pose barely changes (holds, dialogue) or for colour-only passes. For moving shots the
consistency has to come from a temporal model (AnimateDiff-class, which needs CUDA/ROCm, not DirectML), or from drawing
fewer keys and moving them on a rig. Five variants, about 55 min of GPU, settled this; do not spend more on single-frame tricks. Two mechanics that bit: a VAEEncode of an 832x1216 init ran out of VRAM every second frame on a 16 GB card under
DirectML (use VAEEncodeTiled, 512/64), and ComfyUI's LoadImage caches by filename, so give each init file a unique name.
Graph node ids must not collide with the existing decode/save nodes when adding the init branch.

## Still open

Garment details (a cardigan read as a shirt or a vest) and hands still drift. Next levers are a per-character
LoRA, a hand pass, and chaining img2img from the previous frame to cut flicker.

See `pipeline.cel-character-from-generated-master` for the head system, `pipeline.cutout-rig-from-flat-character-master`,
and `methods.reverse-engineer-drawing-style-from-benchmark`.
