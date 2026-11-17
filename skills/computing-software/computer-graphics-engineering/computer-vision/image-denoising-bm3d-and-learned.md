---
id: computing-software.computer-graphics-engineering.computer-vision.image-denoising-bm3d-and-learned
name: image-denoising-bm3d-and-learned
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, bm3d, image-denoising, dncnn, nafnet, noise-estimation]
level: practitioner
status: gated
description: "Denoise images with BM3D and learned models: noise level estimation, bm3d package and OpenCV xphoto, DnCNN/NAFNet/Restormer, raw vs sRGB domain, and avoiding over-smoothing."
sources: ["https://pypi.org/project/bm3d/", "https://webpages.tuni.fi/foi/GCF-BM3D/", "https://docs.opencv.org/4.x/de/daa/group__xphoto.html", "https://github.com/megvii-research/NAFNet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image denoising (BM3D, learned)

## Estimate the noise first
```python
from skimage.restoration import estimate_sigma
sigma = estimate_sigma(img_float01, channel_axis=-1, average_sigmas=True)
```
Denoisers need sigma; wrong sigma = over-smoothing or residual noise. Real camera noise is
signal-dependent: estimate per intensity or use a variance-stabilising transform.

## BM3D
```python
import bm3d
den = bm3d.bm3d(noisy_float01, sigma_psd=sigma, stage_arg=bm3d.BM3DStages.ALL_STAGES)
# colour: bm3d.bm3d_rgb(img, sigma_psd=sigma)
```
- Groups similar patches, collaborative filtering in a 3D transform domain; still a strong classical
  baseline, slow on large images (bm3d 4.0.3 took 1.9 s for a 512x512 grayscale and 5.2 s for a 512x512 colour image on this CPU, so tens of seconds per megapixel for colour). On a 128x128 crop with sigma 0.1 noise `bm3d_rgb` raised PSNR from 20.4 to 35.3 dB.
- OpenCV contrib: `cv2.xphoto.bm3dDenoising(gray_u8, h=sigma*255)` takes a 1-channel 8/16-bit image, but the stock `opencv-contrib-python` 5.0.0 wheel raises "This algorithm is patented and is excluded in this configuration" (needs a build with `OPENCV_ENABLE_NONFREE`). `cv2.fastNlMeansDenoisingColored` is in core OpenCV (faster, weaker: 25.2 dB vs 35.3 dB for BM3D on the crop above).
- Correlated noise (after demosaic/JPEG): pass a noise PSD (a 2D array) as `sigma_psd` instead of a scalar. With NumPy 2.5.4, bm3d 4.0.3 failed on the PSD path with `AttributeError: module 'numpy' has no attribute 'trapz'` (inside the bundled bm4d); setting `np.trapz = np.trapezoid` before `import bm3d` made it run. Scalar sigma is unaffected.

## Learned denoisers
| Model | Notes |
|---|---|
| DnCNN / FFDNet | Light, FFDNet takes a noise-level map (FFDNet README confirms the map input) |
| NAFNet, Restormer | Strong results on SIDD/real noise (gated: unconfirmed, source is paywalled or blocked) |
| SwinIR | General restoration |
Train or fine-tune on **realistic** noise (raw-space Poisson-Gaussian synthesis, or real pairs
like SIDD); Gaussian-on-sRGB training transfers poorly to phone images.

## Domain
Denoise in raw/linear space before demosaic when possible: noise is simpler and independent per
pixel. In sRGB, noise is correlated and amplified in shadows.

## Avoid
- Over-smoothing that removes texture (grass, hair): judge on crops at 100 percent, not on PSNR alone.
- Denoising after aggressive sharpening.

## Verify
PSNR/SSIM on synthetic noise with known clean images; on real images, a no-reference look at flat
areas (residual noise) vs textured areas (detail kept), and the method-noise image (input minus
output should look like noise without structure).

## Checked
scikit-image 0.26.0, bm3d 4.0.3, OpenCV 5.0.0 and opencv-contrib-python 5.0.0 (separate scratch venvs), NumPy 2.5.4.
- Run: `estimate_sigma` (0.098 for true 0.1), `bm3d.bm3d` with `BM3DStages.ALL_STAGES` on a 3-channel array, `bm3d_rgb`, `fastNlMeansDenoisingColored`, the PSD call (fails as described, works with the shim), `xphoto.bm3dDenoising` error text, timings above; printed the `bm3d` and `bm3d_rgb` signatures.
- Not confirmed: the SIDD claim for NAFNet/Restormer (README fetch returned nothing), so that row carries the gated marker and the skill is gated.
