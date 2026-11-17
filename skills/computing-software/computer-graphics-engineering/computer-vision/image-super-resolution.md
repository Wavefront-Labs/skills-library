---
id: computing-software.computer-graphics-engineering.computer-vision.image-super-resolution
name: image-super-resolution
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, computational-imaging, super-resolution, real-esrgan, dnn-superres, multi-frame-super-resolution, edsr, hallucination, psnr, lpips]
level: practitioner
status: verified
description: "Upscale images and video with super-resolution: classical vs learned single-image SR (OpenCV dnn_superres, Real-ESRGAN), multi-frame SR, hallucination risks for measurement."
sources: ["https://szeliski.org/Book/", "https://docs.opencv.org/4.x/d5/d29/tutorial_dnn_superres_upscale_image_single.html", "https://github.com/xinntao/Real-ESRGAN", "https://sites.google.com/view/handheld-super-res"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image super-resolution

**Goal:** more pixels with real or plausible detail — knowing which one you're getting
(Szeliski 2e §10.3).

## 1. Decide what "detail" may mean
- **Measurement / forensic / OCR input / medical**: must not invent structure. Use
  interpolation (Lanczos/bicubic) or multi-frame SR that recovers real information.
- **Viewing / media remastering / textures**: learned generative SR (GAN/diffusion) produces
  sharp plausible detail that may be wrong (hallucinated text, faces, textures).

## 2. Learned single-image SR
OpenCV contrib `dnn_superres` (EDSR, ESPCN, FSRCNN, LapSRN; ×2/×3/×4):
```python
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel("FSRCNN_x2.pb"); sr.setModel("fsrcnn", 2)    # name must match the model
up = sr.upsample(img)
```
On the astronaut image (512x512 downscaled to 256x256 then upscaled x2) FSRCNN x2 gave 31.6 dB vs 30.6 dB for bicubic; a model name that does not match the file (`edsr` with the FSRCNN weights) fails with an assertion in the DNN layer. The opencv_contrib README lists x2/x3/x4 models for EDSR, ESPCN and FSRCNN, EDSR under 3 s and ESPCN under 0.01 s on 256x256 images (i7-9700K). `cv2.dnn_superres` needs an `opencv-contrib-python` build (absent from plain `opencv-python`). FSRCNN/ESPCN: real-time; EDSR: high PSNR, slow. **Real-ESRGAN** handles real-world
degradations (noise, JPEG, blur) and is the practical choice for photos/video frames; use
tiling (`-t`/`--tile`, e.g. `--tile 256`; 0 means no tiling) for large images on limited VRAM.

## 3. Multi-frame super-resolution
Several slightly shifted frames (handheld burst, video) contain sub-pixel samples of the
scene. Register them precisely (ECC, optical flow or block alignment), then fuse onto a finer grid with robust
weighting (Google's Handheld Multi-Frame SR, Wronski et al., ACM TOG 2019: merges a RAW burst, robust to local motion and
occlusion). Recovers genuine detail and reduces noise; it exploits aliasing that changes from frame to frame, so it
needs aliased input (no strong optical low-pass).

## 4. Video
Temporal consistency matters: per-frame GAN SR flickers. Use video SR models (BasicVSR++,
RealBasicVSR) or temporal smoothing; check with side-by-side playback, not stills.

## 5. Evaluation
- Fidelity: PSNR/SSIM vs ground truth (synthetic downscaling → beware: real degradations differ).
- Perceptual: LPIPS, user studies.
- Task metrics: OCR accuracy or detection mAP on SR output vs bicubic — the honest test for
  vision pipelines.

## Gotchas
- Models trained on bicubic-downsampled data fail on real camera images (noise/blur/JPEG).
- Upscaling before a detector rarely beats a detector run at higher input resolution or
  tiled inference.
- Colour shifts/over-sharpening halos: compare histograms and edges.

## Verify
- [ ] Task-level metric improved vs bicubic baseline on real (not synthetic) data.
- [ ] Hallucination review on text/faces for any measurement use (or SR disabled there).
- [ ] Video output checked for temporal flicker.

## Checked
opencv-contrib-python 5.0.0 (separate venv), scikit-image 0.26.0.
- Run: `DnnSuperResImpl_create`, `readModel("FSRCNN_x2.pb")` (downloaded from Saafke/FSRCNN_Tensorflow), `setModel("fsrcnn", 2)`, `upsample` (512x512 output, 31.6 dB vs 30.6 dB bicubic), and the mismatch failure.
- Fetched: opencv_contrib dnn_superres README (models, scales, speed), Real-ESRGAN README (tile option), Handheld Multi-Frame SR project page (aliasing, robustness, ACM TOG 38(4) 2019); RealBasicVSR and BasicVSR++ repositories exist (HTTP 200).
