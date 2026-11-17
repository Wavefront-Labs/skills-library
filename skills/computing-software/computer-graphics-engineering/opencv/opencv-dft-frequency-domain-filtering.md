---
id: computing-software.computer-graphics-engineering.opencv.opencv-dft-frequency-domain-filtering
name: opencv-dft-frequency-domain-filtering
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, dft, frequency-domain, getoptimaldftsize]
level: advanced
status: verified
description: "Use cv::dft for frequency-domain work: optimal padding, complex spectrum layout, shifting quadrants, magnitude display, notch filtering of periodic noise, and fast convolution."
sources: ["https://docs.opencv.org/4.x/d8/d01/tutorial_discrete_fourier_transform.html", "https://docs.opencv.org/4.x/de/dbc/tutorial_py_fourier_transform.html", "https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gadd6cf9baf2b8b704a11b5f04aaf4f39d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFT and frequency-domain filtering

## Forward transform with padding
```python
gray = gray.astype(np.float32)
h, w = gray.shape
H, W = cv2.getOptimalDFTSize(h), cv2.getOptimalDFTSize(w)     # sizes of 2^a 3^b 5^c: much faster
pad = cv2.copyMakeBorder(gray, 0, H - h, 0, W - w, cv2.BORDER_CONSTANT, value=0)
F = cv2.dft(pad, flags=cv2.DFT_COMPLEX_OUTPUT)                # H x W x 2 (re, im)
F = np.fft.fftshift(F, axes=(0, 1))                           # DC to centre
mag = 20 * np.log(cv2.magnitude(F[..., 0], F[..., 1]) + 1)
vis = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
```

## Notch filter for periodic noise (scan lines, moire)
1. Display the log magnitude; periodic noise appears as bright symmetric peaks off-centre.
2. Build a mask (1 everywhere, 0 small discs at the peaks and their mirror positions), blur the
   mask edges to avoid ringing.
3. Multiply both real and imaginary parts, inverse shift, inverse transform:
```python
mask = np.ones((H, W), np.float32)
for (u, v) in peaks: cv2.circle(mask, (u, v), 6, 0, -1); cv2.circle(mask, (W - u, H - v), 6, 0, -1)
mask = cv2.GaussianBlur(mask, (0, 0), 2)
G = F * mask[..., None]
g = cv2.idft(np.fft.ifftshift(G, axes=(0, 1)), flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)[:h, :w]
```

## Fast convolution / correlation
For large kernels (about 11x11 or larger per the OpenCV header), `cv2.filter2D` switches to DFT internally; for repeated
correlation with the same template, precompute its spectrum and use `cv2.mulSpectrums(A, B, 0,
conjB=True)` then `idft` (phase correlation is `cv2.phaseCorrelate`).

## Gotchas
- Input must be float32/64 (uint8 raises an error). `DFT_SCALE` on the inverse divides by N; without it
  values are N times larger (64x64 input: ratio 4096.0, checked; round trip error 4e-7).
- `DFT_REAL_OUTPUT` on inverse assumes conjugate-symmetric input (true if you only applied a
  symmetric real mask).
- Without a window (Hann via `cv2.createHanningWindow`), image borders create a strong cross in the spectrum.

## Verify
- [ ] `idft(dft(x))` reproduces the input within 1e-4; notch-filtered image removes the stripes without visible ringing.
