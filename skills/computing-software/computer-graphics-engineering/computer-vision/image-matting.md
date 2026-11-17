---
id: computing-software.computer-graphics-engineering.computer-vision.image-matting
name: image-matting
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, image-matting, alpha-matte, trimap, video-matting, compositing]
level: practitioner
status: verified
description: "Extract soft alpha mattes: trimap-based (closed-form, ViTMatte), trimap-free portrait/video matting (RVM, MODNet), foreground colour estimation and compositing checks."
sources: ["https://pymatting.github.io/", "https://github.com/PeterL1n/RobustVideoMatting", "https://huggingface.co/docs/transformers/model_doc/vitmatte", "https://people.csail.mit.edu/alevin/papers/Matting-Levin-Lischinski-Weiss-CVPR06.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image matting

Segmentation gives a hard mask; matting solves `I = alpha F + (1 - alpha) B` for fractional alpha
(hair, fur, motion blur, glass).

## Trimap-based
1. Trimap: definite foreground (255), background (0), unknown band (128). From a segmentation mask:
   erode for FG, dilate for BG, band width 10 to 30 px depending on resolution and hair.
```python
k = np.ones((3, 3), np.uint8)            # mask is uint8 0/255
fg = cv2.erode(mask, k, iterations=5); bg = cv2.dilate(mask, k, iterations=15)
trimap = np.full(mask.shape, 128, np.uint8); trimap[fg > 0] = 255; trimap[bg == 0] = 0
```
2. Solve alpha:
   - Classical: `pymatting.estimate_alpha_cf(img, trimap)` (closed-form), `estimate_alpha_knn`.
   - Learned: ViTMatte (transformers `VitMatteForImageMatting`), better on hair.

## Trimap-free
- Portraits / video calls: MODNet, RobustVideoMatting (recurrent, temporally stable; its README lists 104 FPS at HD on a GTX 1080 Ti, FP32).
- General objects: segmentation model (SAM, BiRefNet) + learned matting refinement.

## Foreground colour
Compositing with the original image colours leaves halos of the old background. Estimate F:
`pymatting.estimate_foreground_ml(img, alpha)`, then composite `alpha F + (1 - alpha) B_new`.

## Gotchas
- Work in linear light for compositing correctness (motion blur edges).
- Premultiplied vs straight alpha in exported PNG/EXR: PNG is straight alpha.
- Video: per-frame image matting flickers; use temporal models or smooth alpha with flow.

## Verify
SAD/MSE/gradient error against ground-truth alpha (Composition-1k style) or composite
onto contrasting solid colours (pure green, pure magenta) and inspect edges at 200 percent.

## Checked
PyMatting 1.1.16, OpenCV 5.0.0.
- Run: the trimap recipe (the skill used `k` without defining it; values 0/128/255 result), `estimate_alpha_cf`, `estimate_alpha_knn`, `estimate_foreground_ml` on a 128x128 image: alpha in [0, 1], foreground shape (128, 128, 3).
- Fetched: W3C PNG spec (colour values are not premultiplied: straight/unassociated alpha), Hugging Face ViTMatte page (`VitMatteForImageMatting`, expects image and trimap, evaluated on Composition-1k), RVM README (FPS table), BiRefNet and MODNet repositories exist (HTTP 200).
