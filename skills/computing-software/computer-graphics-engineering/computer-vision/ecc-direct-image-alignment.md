---
id: computing-software.computer-graphics-engineering.computer-vision.ecc-direct-image-alignment
name: ecc-direct-image-alignment
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-alignment, image-registration, ecc-alignment, findtransformecc, direct-alignment, phase-correlation, multi-modal-registration, image-pyramid]
level: practitioner
status: verified
description: "Align images precisely without features using direct methods: OpenCV findTransformECC with motion models and pyramids, phase correlation for translation."
sources: ["https://szeliski.org/Book/", "https://docs.opencv.org/4.x/dc/d6b/group__video__track.html#ga1aa357007eaec11e9ed03500ecbcbe47", "https://docs.opencv.org/4.x/d7/df3/group__imgproc__motion.html#ga552420a2ace9ef3fb053cd630fdb4952", "https://ieeexplore.ieee.org/document/4515873"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECC and direct image alignment

**Goal:** sub-pixel registration of images of the same scene — burst stacking, multi-channel
microscopy, before/after inspection, colour channel alignment (Prokudin-Gorsky plates) —
where features are scarce or imprecise (Szeliski 2e).

## 1. Enhanced Correlation Coefficient (ECC)
Maximises a correlation measure invariant to brightness/contrast changes, iteratively
(Evangelidis & Psarakis 2008).
```python
warp_mode = cv2.MOTION_EUCLIDEAN            # TRANSLATION, EUCLIDEAN, AFFINE, HOMOGRAPHY
warp = np.eye(2, 3, dtype=np.float32)       # 3x3 for HOMOGRAPHY
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
cc, warp = cv2.findTransformECC(template_gray, input_gray, warp, warp_mode, criteria,
                                inputMask=None, gaussFiltSize=5)
aligned = cv2.warpAffine(input_img, warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
```
Note `WARP_INVERSE_MAP`: ECC returns the map from template to input coordinates (tested: input made
with a known rotation of 3 degrees plus shift gave back the same matrix to 0.1 px at a 10 px offset,
residual 2.3 grey levels with `WARP_INVERSE_MAP` against 40 without).

## 2. Make it converge
- ECC is local, so give it a reasonable initial guess (in a test a pure 60 px translation of a
  512x512 photo still converged from the identity, but do not rely on that for rotation, scale or
  textureless scenes). Use a
  **coarse-to-fine pyramid**: estimate at 1/8 scale, scale translation by 2 each level, refine.
- Or initialise from phase correlation (translation) or a feature-based homography.
- Use the simplest motion model that explains the data — more DOF = slower and less stable.
- Mask out moving/saturated regions with `inputMask`.
- Exceptions (`cv2.error: ... The algorithm stopped before its convergence`) are expected for
  bad pairs — catch and fall back.

## 3. Phase correlation (pure translation, fast)
```python
(shift_x, shift_y), response = cv2.phaseCorrelate(np.float32(a), np.float32(b), window=cv2.createHanningWindow(a.shape[::-1], cv2.CV_32F))
```
Sub-pixel, robust to uniform lighting changes; response was 1.03 for a real 7.3 px shift (estimated 7.25, -2.76 for a true (7.3, -2.6)) and about
0.015 for unrelated images, so a response below about 0.1 indicates an unreliable estimate (a
rule of thumb, not an OpenCV constant).

## 4. Direct vs feature-based
| case | prefer |
|---|---|
| small motion, low texture, need sub-pixel precision | ECC / direct |
| large motion, rotation, scale changes | features + RANSAC, then refine with ECC |
| different modalities (IR vs visible) | mutual-information or edge/gradient-based alignment; learned matchers |

## Gotchas
- Different exposures: ECC tolerates global gain/offset, not non-linear tone differences — use
  gradient images.
- Large textureless regions provide no constraint; the solution can drift along them.
- Homography mode needs well-distributed texture across the image.

## Verify
- [ ] Residual difference image after alignment shows no edge ghosting.
- [ ] Estimated transforms on synthetic shifts/rotations accurate to < 0.1 px.
- [ ] Failure cases caught and logged with fallback.
