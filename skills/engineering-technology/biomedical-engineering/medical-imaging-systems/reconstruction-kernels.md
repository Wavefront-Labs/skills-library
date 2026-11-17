---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.reconstruction-kernels
name: reconstruction-kernels
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [reconstruction-kernel, ct-reconstruction, filtered-backprojection, ramp-filter, ram-lak, shepp-logan, convolution-kernel, mtf-ct]
level: practitioner
status: draft
description: "Choose CT reconstruction kernels: ramp filter and window functions, sharp versus smooth kernels, noise-resolution trade-off, and matching kernels to clinical tasks."
sources: ["Kak and Slaney, Principles of Computerized Tomographic Imaging", "Bushberg et al., The Essential Physics of Medical Imaging (CT chapter)", "Hsieh, Computed Tomography: Principles Design Artifacts and Recent Advances"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CT reconstruction kernels

**Goal:** understand what a reconstruction kernel does so you can choose or tune it for a task and predict the noise-resolution trade-off.

## Filtered backprojection (FBP)
Projection data are filtered along each detector row by a **ramp filter** |omega| in the frequency domain (or an equivalent convolution kernel) and then backprojected. The pure ramp filter amplifies high-frequency noise, so it is multiplied by a window.

## Kernel family
- **Ram-Lak:** ramp to the Nyquist frequency; sharpest, noisiest.
- **Shepp-Logan:** ramp with a sinc window; slightly smoother.
- **Hamming, Hann, cosine, Butterworth:** progressively more smoothing windows with parameter control.
- Vendors name kernels (soft, standard, bone, lung or numbered series); the names are proprietary, and kernels with the same name differ between manufacturers.

## Trade-offs
- Sharp kernel: high spatial resolution (MTF extends to higher frequency), higher noise; bone, lung, inner ear and stent imaging.
- Smooth kernel: lower noise, lower resolution; soft tissue and low-contrast detectability.
- Noise magnitude roughly scales with the integrated kernel response; to halve noise by smoothing alone you lose resolution; iterative reconstruction attempts a better trade (see iterative-reconstruction).

## Practical steps
1. Define the task (lesion detection in liver versus fracture detail in bone).
2. Measure the MTF of the kernel with a wire or edge phantom and the noise power spectrum on a uniform phantom.
3. Compare kernels at equal dose; choose the one that meets the resolution need with the lowest noise.
4. Pair with slice thickness and pixel size (do not over-sharpen with a pixel too large).
5. Dual reconstructions (sharp and smooth) are common to serve different tasks.

## Verify
- [ ] MTF50 and noise (HU standard deviation) recorded for each kernel at fixed dose.
- [ ] Hounsfield accuracy not affected by kernel (mean HU stays within tolerance).
- [ ] Artefact check at high-contrast edges (overshoot ringing).
