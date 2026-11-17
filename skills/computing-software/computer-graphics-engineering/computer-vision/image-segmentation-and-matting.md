---
id: computing-software.computer-graphics-engineering.computer-vision.image-segmentation-and-matting
name: image-segmentation-and-matting
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-vision, segmentation, matting, alpha-matte, green-screen, chroma-key, grabcut, watershed, semantic-segmentation, instance-segmentation, sam, segment-anything, trimap, edge-bleed, spill]
level: advanced
status: verified
description: "Get a clean alpha matte or segmentation mask: classical (GrabCut, watershed, chroma key) vs learned (SAM, matting networks), trimaps, and the edge/spill failure modes that ruin a composite."
sources: ["https://docs.opencv.org/4.x/d8/d83/tutorial_py_grabcut.html", "https://segment-anything.com/", "https://github.com/PeterL1n/BackgroundMattingV2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image segmentation and matting

**Goal:** produce a mask or alpha matte clean enough to composite, not just
"roughly covers the object" — the difference that matters is the transition at
edges (hair, motion blur, translucency), which binary segmentation can't represent.

## Segmentation vs matting — pick the right output
- **Binary/semantic segmentation** gives a hard mask (0/1 per pixel) — fine for
  detection, bounding boxes, "is this pixel part of object class X." Produces
  visible jagged edges if used directly for compositing.
- **Matting** gives a soft **alpha** (0–1, continuous) per pixel — required for
  believable compositing of hair, fur, motion-blurred edges, smoke, glass.
  Segmentation is a subset problem of matting with alpha forced to {0,1}.

## Classical tools
- **Chroma key** (green/blue screen): threshold in a colour space where the key
  colour separates cleanly (often a custom formula on R/G/B, not raw hue) +
  despill (subtract key-colour bleed from edge pixels) + edge erosion/blur to soften.
  Fails on green/blue clothing, reflective surfaces, and fine hair against detail.
- **GrabCut** (`cv2.grabCut`): iterative graph-cut using a user-provided rough
  rectangle/mask as a prior, GMM colour models for fg/bg. Good for a human-in-the-loop
  single image; too slow/manual for video or batch.
- **Watershed**: treats intensity gradient as a topographic map, floods from seed
  markers. Good for separating touching objects with clear boundaries (cell/blob
  segmentation); not natural-image matting.

## Learned
- **SAM / SAM2** (Segment Anything): prompt with points or boxes (the README does not list text
  prompts for the released models); gives high-quality masks zero-shot across domains. It's segmentation (hard-ish mask,
  though SAM's logits before thresholding do carry soft edge info) — still needs a
  dedicated matting pass for hair-level edges.
- **Dedicated matting networks** (BackgroundMattingV2, MODNet, RVM for video) output
  alpha directly. BackgroundMattingV2 needs an extra captured background image; RVM
  (Robust Video Matting) is built for human video matting, recurrent for temporal
  consistency, and its README lists 104 FPS at HD on a GTX 1080 Ti (FP32) — the right choice
  for live background replacement of people without a green screen.
- A **trimap** (background=0, foreground=1, unknown=0.5 band around the edge) is the
  classic input to matting algorithms (closed-form matting, KNN matting): generate
  it by eroding/dilating a coarse mask, solve alpha only in the unknown band.

## Failure modes
- **Colour spill**: foreground edge pixels tinted by the background/key colour
  bouncing onto the subject — visible as a green fringe on green-screen composites.
  Fix with despill (reduce the key-colour channel near edges) after matting, before compositing.
- **Temporal flicker** (video): per-frame independent matting gives a mask that
  jitters frame to frame even on a static subject — use a temporally-aware model
  (RVM) or blend/stabilise mattes across a short window.
- **Thin structures** (hair strands, fences) below the model's effective resolution
  get averaged away — upsample input or use matting models specifically trained at
  high resolution for hair-critical shots.
- Compositing an alpha matte with **premultiplied vs straight alpha** confusion
  produces a dark or bright halo at edges — know which convention your matte and
  compositor expect and convert consistently (`straight = premult / alpha`).

## Verify
- [ ] Composite over a solid, saturated test background (not just black) to reveal
      spill and halo artefacts the original background would hide.
- [ ] Edge zoom-in on hair/fur/motion-blur region shows a soft gradient, not a hard
      binary edge, if matting (not segmentation) was the goal.
- [ ] Video output checked for temporal flicker on a static subject across several
      consecutive frames.
- [ ] Premultiplied/straight alpha convention confirmed against the compositor used downstream.

## Checked
OpenCV 5.0.0, PyMatting 1.1.16, scikit-image 0.26.0.
- Run: `cv2.grabCut` with a rectangle on the astronaut image (mask values 0, 2, 3 as documented), distance-transform + `cv2.watershed` marker pipeline, `estimate_alpha_cf` and `estimate_alpha_knn` on a trimap built with the erode/dilate recipe (values 0, 128, 255), straight = premult / alpha arithmetic.
- Fetched: segment-anything README (points or boxes), RVM README (104 FPS HD GTX 1080 Ti FP32; human matting), BackgroundMattingV2 README (needs background image).
