---
id: computing-software.computer-graphics-engineering.computer-vision.low-light-image-enhancement
name: low-light-image-enhancement
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, low-light-enhancement, retinex, zero-dce, clahe, night-photography]
level: practitioner
status: gated
description: "Brighten low-light images without amplifying noise: gamma/CLAHE baselines, Retinex-style (LIME), learned Zero-DCE/RetinexFormer, raw-domain pipelines and denoise ordering."
sources: ["https://arxiv.org/abs/2001.06826", "https://ieeexplore.ieee.org/document/7782813", "https://cchen156.github.io/SID.html", "https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Low-light enhancement

## Prefer capture fixes
Longer exposure, bigger aperture, burst merging and raw capture beat any post-process. Multi-frame
averaging of N frames reduces noise by sqrt(N) (measured: sigma 10.0, 5.03, 2.50 for N = 1, 4, 16).

## Classical baselines
```python
# gamma on luminance
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
L = lab[..., 0].astype(np.float32) / 255
lab[..., 0] = np.uint8(255 * L ** 0.5)
# local contrast
lab[..., 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[..., 0])
out = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
```
- **LIME** (Retinex): estimate the illumination map as max(R,G,B), refine it with structure-aware
  smoothing, divide `I / T^gamma`. Good results, noise amplified in dark regions (gated: unconfirmed, source is paywalled or blocked). The paper is behind IEEE Xplore, so this description is from memory.

## Learned
| Model | Notes |
|---|---|
| Zero-DCE / Zero-DCE++ | Curve estimation, no paired data, tiny and fast |
| RetinexFormer, SNR-Aware | Paired training (LOL dataset), best quality |
| SID (Learning to See in the Dark) | Raw-to-RGB network on very dark raw frames |
Paired datasets (LOL) are small; models overfit their camera. Validate on your sensor. Only the Zero-DCE title (arXiv 2001.06826, "Zero-Reference Deep Curve Estimation") was confirmed; the other rows are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## Noise
Brightening multiplies noise. Denoise **before** or jointly with enhancement (raw domain ideal);
enhancing then denoising sRGB results in blotchy colour noise. Apply chroma denoising separately.

## Colour
Very dark scenes have colour casts (sodium lamps, low SNR in blue): white balance after
brightening and clamp saturation boost.

## Verify
For paired data: PSNR/SSIM/LPIPS. For unpaired: NIQE plus visual review of shadows (noise), highlights
(clipping) and faces (skin colour).

## Checked
OpenCV 5.0.0, NumPy 2.5.4.
- Run: the Lab gamma + CLAHE snippet on the astronaut image scaled to 15 percent brightness (mean 16.8 to 60.7); frame averaging of N = 1, 4, 16 noisy frames (sigma 10 gives 10.0, 5.03, 2.50).
- Fetched: arXiv API title for 2001.06826 (Zero-DCE).
- Not confirmed: LIME details (IEEE paywall), RetinexFormer, SNR-Aware, SID, LOL notes; marked gated, so the skill is gated.
