---
id: computing-software.computer-graphics-engineering.computer-vision.light-fields-and-view-interpolation
name: light-fields-and-view-interpolation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-based-rendering, light-field, view-interpolation, depth-image-based-rendering, multiplane-images, frame-interpolation]
level: sme
status: gated
description: "Synthesise novel views from images: two-plane light fields, depth-image-based warping with hole filling, multiplane images, and learned frame interpolation."
sources: ["https://szeliski.org/Book/", "https://graphics.stanford.edu/papers/light/", "https://arxiv.org/abs/1805.09817", "https://github.com/google-research/frame-interpolation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# View interpolation and light fields

## 1. Light fields
- A 4D light field `L(u,v,s,t)` (two-plane parameterisation) records rays through a camera plane (u,v) and a
  focal plane (s,t). Captured by camera arrays, a moving gantry, or plenoptic cameras (microlens arrays).
- Rendering a new view = resampling rays: quadrilinear interpolation of the nearest cameras' pixels.
- Synthetic refocus: shift each sub-aperture image proportional to its (u,v) offset and average; the shift
  amount selects the focal depth (checked: five horizontally shifted copies of an image, 4 px per view, averaged after
  undoing the shifts gave zero error for the plane at that disparity and a mean error of 14.8 grey levels with no shift).
- Sampling: camera spacing must keep disparity between neighbours under ~1 px at the depths of interest, or
  interpolation ghosts; a depth proxy relaxes this (lumigraph) (gated: unconfirmed, source is paywalled or blocked).

## 2. Depth-image-based rendering (DIBR)
1. Per-pixel depth for reference views (stereo, MVS, or sensor).
2. Forward-warp pixels to the target camera: unproject with depth, transform, project; z-buffer conflicts.
3. Blend the two nearest references weighted by angular distance.
4. Fill disocclusion holes from the other reference, then inpaint the remainder from the background side
   (never from the foreground).
Splatting points with a small footprint avoids cracks from forward mapping.

## 3. Multiplane images (MPI)
Represent the scene as D fronto-parallel RGBA planes in a reference frustum, predicted by a network from a
few views; render novel views by homography-warping each plane and over-compositing back to front. Real-time
on GPUs, good for small baselines (stereo magnification, 3D photos) (gated: unconfirmed, source is paywalled or blocked).

## 4. Temporal view interpolation
Video frame interpolation (FILM, RIFE) synthesises in-between frames from flow; it is view interpolation in
time. Large motion and occlusions are the failure cases.

## Gotchas
- Depth edges misaligned with colour edges cause "flying pixels" and halos: refine depth with edge-aware
  filtering and dilate foreground depth slightly.
- Specular and transparent surfaces break single-depth warping; light fields or neural methods handle them.
- For wide baselines use NeRF or Gaussian splatting instead.

## Verify
- [ ] Render a held-out real camera position and compare (PSNR/SSIM); inspect depth edges for halos.

## Checked
OpenCV 5.0.0, NumPy 2.5.4.
- Run: shift-and-add refocus on a synthetic five-view horizontal light field.
- Fetched: arXiv API title for 1805.09817 (Stereo Magnification: Learning View Synthesis using Multiplane Images); google-research/frame-interpolation repository exists (HTTP 200).
- Not confirmed: sampling-rate rule, MPI real-time claim; gated.
