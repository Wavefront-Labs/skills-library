---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-histogram-compute
name: gpu-histogram-compute
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, gpu-histogram, atomics, shared-memory, auto-exposure, luminance-histogram, compute-shader]
level: practitioner
status: draft
description: "Build histograms on the GPU with atomics: per-workgroup shared-memory bins merged into global, luminance histograms for auto-exposure, and contention and precision pitfalls."
sources: ["https://bruop.github.io/exposure/", "https://developer.download.nvidia.com/compute/cuda/1.1-Beta/x86_website/projects/histogram64/doc/histogram.pdf", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/interlockedadd"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU histograms with atomics

## 1. Two-level pattern
Global atomics from every pixel to 256 bins contend badly. Accumulate per workgroup in shared
memory, then merge:
```glsl
layout(local_size_x = 16, local_size_y = 16) in;
shared uint bins[256];
layout(std430, binding = 1) buffer Hist { uint global[256]; };

void main() {
    uint li = gl_LocalInvocationIndex;
    bins[li] = 0u;                         // 256 threads clear 256 bins
    barrier();
    ivec2 p = ivec2(gl_GlobalInvocationID.xy);
    if (all(lessThan(p, size))) {
        vec3 c = texelFetch(hdr, p, 0).rgb;
        float lum = dot(c, vec3(0.2126, 0.7152, 0.0722));
        uint bin = lum < 1e-5 ? 0u
                 : uint(clamp((log2(lum) - minLog2) * invLog2Range, 0.0, 1.0) * 254.0 + 1.0);
        atomicAdd(bins[bin], 1u);
    }
    barrier();
    atomicAdd(global[li], bins[li]);
}
```
Bin 0 reserved for near-black pixels so they don't drag the average.

## 2. Reduce the histogram
A second dispatch (one workgroup of 256) computes the weighted average bin with a shared-memory
reduction, converts back to luminance (`exp2(avgBin * range + min)`), and adapts exposure over
time (`lum = last + (target - last) * (1 - exp(-dt * tau))`). Clear the global bins in the same pass.

## 3. Variants
- Colour histograms (RGB 3x256): either 3 passes or 768 shared bins.
- Reduce contention for skewed data (sky = one bin) by privatising bins per wave
  (bins[waveIndex][256]) or using `WaveActiveSum` when all lanes hit the same bin
  (`WaveActiveAllEqual(bin)`).
- Downsample input (e.g. quarter res) for exposure; accuracy barely changes.

## Gotchas
- Float atomics are not universally supported; use uint counts.
- Center-weighted metering: weight samples by distance to centre by adding a weight instead of 1
  (scale to integers).
- Count overflow: 4K = 8.3 M pixels fits in uint32, but summing weighted values can overflow;
  divide or use 64-bit atomics where available.

## Verify
- [ ] Sum of bins equals the number of sampled pixels.
- [ ] Histogram matches a CPU histogram of a readback within rounding.
