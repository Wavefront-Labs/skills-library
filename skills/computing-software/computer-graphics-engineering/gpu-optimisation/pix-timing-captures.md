---
id: computing-software.computer-graphics-engineering.gpu-optimisation.pix-timing-captures
name: pix-timing-captures
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, pix-timing-capture, pix, d3d12, cpu-timeline, gpu-timeline, pix-events]
level: practitioner
status: draft
description: "Profile D3D12 titles with PIX Timing Captures: CPU/GPU timelines, PIX markers, queue overlap, file I/O and memory tracks, and finding CPU-bound vs GPU-bound frames."
sources: ["https://devblogs.microsoft.com/pix/timing-captures/", "https://devblogs.microsoft.com/pix/winpixeventruntime/", "https://learn.microsoft.com/en-us/gaming/tools/pix/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PIX timing captures

## 1. Instrument
Add PIX markers via WinPixEventRuntime (NuGet `WinPixEventRuntime`):
```cpp
#include <pix3.h>
PIXBeginEvent(PIX_COLOR_INDEX(1), L"Shadows");      // CPU-side scope
PIXBeginEvent(cmdList, PIX_COLOR(255,0,0), "Shadows");  // GPU-side scope on a command list
...
PIXEndEvent(cmdList); PIXEndEvent();
PIXSetMarker(L"Frame %u", frame);
PIXReportCounter(L"Visible objects", (float)count);
```
Define `USE_PIX` in profiling builds; markers compile out otherwise. Name threads
(`SetThreadDescription`) so timelines are readable.

## 2. Take a capture
PIX on Windows > Attach/Launch > **Timing Capture** (start/stop or a fixed duration). Options: CPU
samples (callstacks), file accesses, GPU timings, memory allocations (VirtualAlloc/heap tracking).
Programmatic: `PIXBeginCapture(PIX_CAPTURE_TIMING, &params)` / `PIXEndCapture` via
`WinPixGpuCapturer` style APIs.

## 3. Read it
- **Timeline**: per-thread CPU scopes, context switches, and GPU queues (graphics, compute, copy)
  with execution of each `ExecuteCommandLists`.
- CPU-bound: the GPU queue has gaps waiting on submissions; the render thread is busy end to end.
- GPU-bound: CPU threads wait on fences (`WaitForSingleObject` on frame fence) while the GPU queue is
  saturated.
- Async compute overlap shows as concurrent work on graphics and compute queues.
- **Present/vsync markers** show missed frames and frame pacing.
- Range selection gives aggregate CPU sample hot functions (with symbols configured).

## 4. GPU Captures vs timing
Timing captures show whole frames over time with low overhead; use **GPU Captures** (single frame
replay) for per-draw timing, occupancy and counters once you know which pass is slow.

## Gotchas
- Symbol paths must be configured (PDBs of the build) or callstacks show addresses.
- GPU timing granularity is per command list/scope; add more GPU markers to split passes.
- Profile release-like builds; debug layers distort timings massively.

## Verify
- [ ] Markers visible for every major pass on both CPU and GPU timelines.
- [ ] Frame classified as CPU- or GPU-bound with evidence from the capture.
