---
id: computing-software.computer-graphics-engineering.rendering-techniques.path-tracer-denoising-oidn-svgf
name: path-tracer-denoising-oidn-svgf
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, denoising, oidn, svgf, a-trous-wavelet, path-tracing, optix-denoiser]
level: sme
status: gated
description: "Denoise path-traced images: Intel Open Image Denoise with albedo/normal AOVs offline, and SVGF temporal accumulation plus a-trous filtering in real time."
sources: ["https://github.com/RenderKit/oidn/blob/master/doc/api.md", "https://research.nvidia.com/publication/2017-07_spatiotemporal-variance-guided-filtering-real-time-reconstruction-path-traced", "https://github.com/NVIDIA-RTX/NRD"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path tracer denoising: OIDN and SVGF

## 1. Offline/interactive: Open Image Denoise
```cpp
oidn::DeviceRef dev = oidn::newDevice();          // picks CPU, CUDA, SYCL, HIP or Metal
dev.commit();
oidn::FilterRef f = dev.newFilter("RT");          // "RTLightmap" for lightmaps
f.setImage("color",  colorBuf,  oidn::Format::Float3, w, h);
f.setImage("albedo", albedoBuf, oidn::Format::Float3, w, h);   // optional, first-hit albedo
f.setImage("normal", normalBuf, oidn::Format::Float3, w, h);   // optional
f.setImage("output", outBuf,    oidn::Format::Float3, w, h);
f.set("hdr", true);                                // linear HDR input
f.set("quality", oidn::Quality::High);
f.commit(); f.execute();
const char* err; if (dev.getError(err) != oidn::Error::None) fprintf(stderr, "%s\n", err);
```
- For perfect specular (delta) surfaces such as mirrors, follow the path to the first non-delta hit for albedo and normal.
- `cleanAux=true` only when aux buffers are noise-free (or prefiltered with their own filters, see the OIDN prefiltering example).
- HDR colour values must be passed with `hdr` set to true; all images must have the same dimensions, and in-place denoising (output = colour) is supported.
- Memory from the system allocator (`malloc`) raises an error on GPU devices; allocate with `dev.newBuffer` (host and device accessible by default) or use device allocations.

## 2. Real time: SVGF
The NVIDIA publication page only carries the abstract (about 10 ms per 1080p frame, reported 5-47% SSIM improvement); the algorithm constants below come from the paper PDF, which was not read.
1. Path trace 1 spp; demodulate albedo (`illum = color / albedo`).
2. **Temporal accumulation**: reproject with motion vectors, validate with depth/normal/mesh-id, blend with
   `alpha = max(1/historyLen, 0.2)` (gated: unconfirmed, source is paywalled or blocked); also accumulate first and second luminance moments.
3. **Variance** from moments (spatial estimate for the first 4 frames of history, gated: unconfirmed, source is paywalled or blocked).
4. **A-trous wavelet**: 5 iterations of a 5x5 B-spline kernel at step 1,2,4,8,16 (gated: unconfirmed, source is paywalled or blocked), edge-stopping on depth
   gradient, normal (`pow(max(0,dot),128)`, gated: unconfirmed, source is paywalled or blocked) and luminance scaled by `sqrt(variance)`. Feed iteration 1 back
   as next frame's history.
5. Remodulate albedo, then TAA.

## Gotchas
- Filtering before demodulation blurs texture detail.
- Disocclusions restart history and look noisy; A-SVGF adds gradient-based rejection for lighting changes.
- Production real-time alternative: NVIDIA Real-Time Denoisers (NRD, includes ReBLUR).

## Verify
- [ ] Denoised low-spp image vs a converged reference: report SSIM or FLIP; no smearing of albedo detail.
- [ ] Moving lights leave no ghost trails longer than a few frames.

## Checked

2026-10-26: OIDN doc/api.md (RenderKit/oidn master, CHANGELOG at v2.5.1, read 2026-10-26). Confirmed: RT and RTLightmap filter names, color/albedo/normal/output images, hdr and cleanAux and quality parameters (OIDN_QUALITY_HIGH default), in-place denoising, GPU devices reject system-allocator memory, device types CPU/SYCL/CUDA/HIP/Metal, delta-surface first-hit guidance. Wrong claim fixed: normal does not require albedo in the parameter table. The SVGF constants (alpha 0.2, 4 frames, five a-trous iterations, 5x5 kernel, exponent 128) are only in the paper PDF, which was not read, so they are marked gated. NRD README lists ReBLUR; ReLAX and DLSS Ray Reconstruction were not confirmed and were dropped.

Method: documentation only; no commands were run.
