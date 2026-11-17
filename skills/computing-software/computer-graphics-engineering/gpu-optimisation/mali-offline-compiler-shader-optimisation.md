---
id: computing-software.computer-graphics-engineering.gpu-optimisation.mali-offline-compiler-shader-optimisation
name: mali-offline-compiler-shader-optimisation
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, mali-offline-compiler, mobile-shader-optimisation, arm-mali, fp16, malioc, mobile-gpu]
level: practitioner
status: draft
description: "Optimise shaders for mobile GPUs with Arm Mali Offline Compiler: reading cycle counts per pipeline (arithmetic, load/store, varying, texture), fp16, and register spilling."
sources: ["https://developer.arm.com/documentation/101863/latest/", "https://developer.arm.com/documentation/101897/latest/", "https://developer.arm.com/Tools%20and%20Software/Mali%20Offline%20Compiler"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile shader optimisation with Mali Offline Compiler

## 1. Run it
Mali Offline Compiler (`malioc`) ships with Arm Performance Studio.
```bash
malioc --core Mali-G78 shader.frag
malioc --core Mali-G715 --vulkan shader.frag.spv
malioc --list                      # supported GPUs
malioc --format json -o report.json --core Mali-G710 shader.frag
```
GLSL ES or SPIR-V input; stage from extension (`.vert/.frag/.comp`) or `--vertex` etc.

## 2. Read the report
```
                                A      LS       V       T    Bound
Total instruction cycles:     2.50   0.00    0.25    1.00        A
Shortest path cycles:         1.25   0.00    0.25    1.00        A
Longest path cycles:          2.50   0.00    0.25    1.00        A
A = Arithmetic, LS = Load/Store, V = Varying, T = Texture
Work registers: 32   Uniform registers: 16   Stack spilling: false   16-bit arithmetic: 85%
```
- The highest column is the bottleneck pipe ("Bound"). Optimise that pipe first.
- **Work registers** > 32 (Valhall: 64 is the max, occupancy halves above 32) reduce thread count.
- **Stack spilling: true** is a red flag: reduce live variables.
- **16-bit arithmetic %**: higher is better; fp16 doubles ALU throughput on Mali.

## 3. Typical fixes
- Use `mediump` (fp16) for colours, normals in view space, UVs on small textures; keep `highp` for
  positions, depth, large UV ranges.
- Varying cycles: pack varyings, use `mediump` varyings (half the interpolation cost), remove
  unused ones.
- Texture cycles: fewer samples, avoid trilinear/anisotropic where invisible, avoid 3D/cube with
  high precision formats.
- Arithmetic: hoist uniform math to the CPU (malioc reports "uniform computation" separately in some
  versions).
- Load/store: avoid dynamic indexing into local arrays, reduce SSBO traffic.

## 4. Confirm on device
Offline cycles ignore memory bandwidth and caches. Validate with Arm Streamline (Performance
Studio) hardware counters on a real device.

## Gotchas
- Results differ a lot between Mali generations (Midgard, Bifrost, Valhall, 5th Gen); target the
  GPUs your users have.
- `mediump` in GLSL is a hint; on desktop it is ignored, so test on device for precision artefacts.

## Verify
- [ ] Bound pipe cycles reduced; no stack spilling; work registers <= 32 where possible.
- [ ] Streamline shows lower fragment shader cycles per frame.
