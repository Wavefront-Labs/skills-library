---
id: computing-software.computer-graphics-engineering.rendering-techniques.thin-lens-camera-and-film-models
name: thin-lens-camera-and-film-models
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, thin-lens, depth-of-field, camera-model, film-reconstruction, pixel-filter, f-stop]
level: practitioner
status: draft
description: "Model cameras in ray tracers: pinhole and thin-lens depth of field from aperture and focus distance, f-stop and sensor size, pixel filters and film reconstruction."
sources: ["https://pbr-book.org/4ed/Cameras_and_Film/Projective_Camera_Models", "https://pbr-book.org/4ed/Cameras_and_Film/Film_and_Imaging", "https://raytracing.github.io/books/RayTracingInOneWeekend.html#defocusblur"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thin lens camera and film models

## 1. Pinhole
```cpp
vec2 ndc = ((pixel + jitter) / resolution) * 2.0f - 1.0f;   // jitter for AA, inside pixel
vec3 dirCam = normalize(vec3(ndc.x * tanHalfFovX, -ndc.y * tanHalfFovY, -1.0f));
Ray r = { camPos, camToWorld * dirCam };
```

## 2. Thin lens (depth of field)
Points on the focal plane are sharp; others blur into a circle of confusion.
```cpp
vec3 pFocus = dirCam * (focusDistance / -dirCam.z);    // point on focal plane (camera space)
vec2 lens = apertureRadius * sampleUniformDisk(u2);    // concentric disk mapping for low distortion
vec3 origin = vec3(lens.x, lens.y, 0.0f);
vec3 dir = normalize(pFocus - origin);
Ray r = { camToWorld * origin, camToWorldDir * dir };
```
- `apertureRadius = focalLength / (2 * fNumber)`. With a 50 mm lens at f/2: radius 12.5 mm.
- Relate FOV and focal length via sensor size: `fovY = 2 atan(sensorHeight / (2 f))` (35 mm full
  frame sensor 36x24 mm).
- Bokeh shape: sample a polygon (blades) or a texture instead of a disk; cat's-eye vignetting needs
  a real lens model (PBRT RealisticCamera).

## 3. Film and pixel reconstruction
- Each sample contributes to nearby pixels weighted by a reconstruction filter: box (sharp,
  aliases), tent, Gaussian (r ~1.5 px, soft), Mitchell-Netravali / Blackman-Harris (balanced).
- PBRT-v4 instead importance-samples the filter when generating camera rays (filter importance
  sampling), so each sample adds to one pixel with weight ~1 - simpler and parallel-friendly.
- Film stores linear radiance (spectral -> sensor RGB with sensor response, white balance); output
  EXR, then tonemap separately.

## 4. Exposure
Physical: `exposure = shutter * (1 / fNumber^2) * ISO/100` scaled; tie EV100 to the real-time
renderer for consistent look across raster and path traced references.

## Gotchas
- Focus distance measured along the view axis, not ray length (otherwise curved focal surface).
- Uniform random disk sampling with `sqrt(u)` is fine; naive `r = u` clusters samples in the centre.
- AA jitter and lens samples must use different sampler dimensions (avoid correlation).

## Verify
- [ ] Objects at focus distance sharp; blur radius matches the CoC formula at other depths.
- [ ] Changing f-stop scales blur without shifting focus.
