---
id: computing-software.computer-graphics-engineering.gpu-optimisation.driver-overhead-and-api-choice
name: driver-overhead-and-api-choice
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, cpu-overhead, driver-overhead, api-choice, azdo, vulkan, d3d12, opengl]
level: advanced
status: draft
description: "Weigh driver overhead when choosing a graphics API: implicit vs explicit APIs, AZDO-style OpenGL, D3D11 deferred contexts, Vulkan/D3D12/Metal costs, and porting for CPU wins."
sources: ["https://gdcvault.com/play/1020791/Approaching-Zero-Driver-Overhead-in", "https://developer.nvidia.com/blog/vulkan-dos-donts/", "https://gpuopen.com/learn/rdna-performance-guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Driver overhead and API choice

## 1. Implicit vs explicit
| API | Driver does | CPU overhead per draw | Multithreaded recording |
|---|---|---|---|
| OpenGL / D3D11 | hazard tracking, memory management, shader compilation on state change, validation | high | limited (D3D11 deferred contexts rarely win; GL single context) |
| Vulkan / D3D12 / Metal | little: app manages sync, memory, descriptors, PSOs | low | yes, by design |

Explicit APIs move work to the app: if the app re-implements implicit tracking naively, gains
vanish.

## 2. Getting most from OpenGL (AZDO)
"Approaching Zero Driver Overhead" (GDC 2014): persistent mapped buffers, `glMultiDrawElementsIndirect`
with draw parameters in buffers, bindless textures (`ARB_bindless_texture`) or texture arrays, and
sparse textures. Reduces GL to a few calls per frame; often enough without porting.

## 3. Explicit API pitfalls that reintroduce overhead
- Creating PSOs at draw time (hitches; driver compile).
- Updating descriptor sets per draw instead of using bindless or dynamic offsets.
- Too many command buffers/submissions (each `vkQueueSubmit`/`ExecuteCommandLists` has cost);
  batch submits per frame.
- Over-conservative barriers (full pipeline barriers everywhere) costing GPU idle time.

## 4. When to port
- CPU-bound in the driver with many draws, needing multithreaded recording -> Vulkan/D3D12/Metal.
- Need for async compute, explicit memory aliasing, ray tracing, mesh shaders -> explicit APIs.
- GPU-bound or modest scenes -> porting rarely helps; optimise content instead.
- Mobile Android: Vulkan reduces CPU (and power) noticeably vs GLES on many devices but driver
  quality varies; keep a GLES fallback.

## 5. Translation layers
ANGLE, MoltenVK, DXVK/VKD3D-Proton, Zink: add some overhead but are production-quality; choose them
for portability, profile the translated path.

## Gotchas
- Benchmarks of API "draws per second" are best cases; real overhead depends on your binding model.
- D3D11 on modern drivers is very optimised; a naive D3D12 port can be slower.

## Verify
- [ ] Driver time vs engine time measured before deciding to port.
- [ ] After port, CPU time per frame reduced in representative scenes.
