---
id: computing-software.computer-graphics-engineering.directx.directx-pix-debugging-and-gpu-captures
name: directx-pix-debugging-and-gpu-captures
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [directx, d3d12, pix, gpu-capture, frame-debugging, gpu-validation, debug-layer, timing-capture, shader-debugging, event-markers, winpixeventruntime, nsight-graphics]
level: advanced
status: draft
description: "Use PIX on Windows to capture and diagnose a D3D12 frame: GPU captures vs timing captures, event markers, shader debugging, and reading the debug/GPU-based validation layers before reaching for PIX."
sources: ["https://devblogs.microsoft.com/pix/", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/graphics-debugging-with-pix"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PIX debugging and GPU captures (D3D12)

**Goal:** find the actual cause of a wrong frame or a slow frame on D3D12/Windows
without guessing — PIX is the tool, but most of the value is knowing which capture
type answers which question, and reading the cheaper signals (debug layer) first.

## Cheapest first: debug layer and GPU-based validation
Before opening PIX, enable in order of cost:
1. `ID3D12Debug::EnableDebugLayer()` — catches resource-state mismatches, invalid
   API usage, missing barriers. Always on in dev builds; near-zero cost.
2. **GPU-based validation** (`ID3D12Debug1::SetEnableGPUBasedValidation`) — catches
   invalid shader resource access (reading unbound/wrong-typed descriptors),
   heavier runtime cost but catches bugs the debug layer alone misses.
3. `D3D12_MESSAGE_SEVERITY` filtering via an info queue so messages don't scroll
   past unnoticed in a busy log.
Most "my texture is black/garbage" bugs resolve here before a capture is needed.

## PIX capture types
- **GPU capture** (a single frame, full command stream + resources): for
  correctness bugs — wrong color, missing geometry, wrong pipeline state. Lets you
  select any draw/dispatch and inspect bound resources, vertex/index data, render
  target contents at that point, and the actual shader bytecode/source.
- **Timing capture** (CPU+GPU trace over a window of frames, like a profiler
  timeline): for performance bugs. Shows CPU command-list recording cost, GPU
  engine occupancy (3D/compute/copy queues), and where frame time actually goes —
  use this before a GPU capture when the problem is "too slow," not "looks wrong."
- **Counter capture**: hardware performance counters per draw (occupancy, cache hit
  rate, ALU utilisation) — vendor-specific depth (NVIDIA/AMD/Intel counters differ);
  cross-check against Nsight Graphics or Radeon GPU Profiler for vendor-specific detail
  PIX's generic view doesn't surface.

## Event markers
```cpp
PIXBeginEvent(cmdList, PIX_COLOR(255,0,0), L"ShadowPass");
// ... draws ...
PIXEndEvent(cmdList);
```
- Without markers, a capture timeline is an undifferentiated wall of draw calls —
  markers are what makes "which pass is this 4ms in" answerable at a glance.
  Nest them per pass/sub-pass; name resources too (`SetName`) so captures show
  readable labels instead of `ID3D12Resource 0x...`.
- `WinPixEventRuntime` works in both debug and release-with-markers builds — ship
  with markers enabled behind a cheap runtime flag; the overhead is negligible
  compared to the diagnostic value in the field.

## Shader debugging in PIX
- PIX supports **shader debugging** on a specific pixel/thread within a captured
  draw/dispatch: step through HLSL source, inspect register values per-instruction.
  Requires debug info in the shader (`-Zi` with DXC, or skip stripping it in the
  packaged build you're debugging).
- For a wrong-pixel bug, pick the exact pixel coordinate from the capture's render
  target view, then shader-debug only that invocation rather than guessing from code review.

## Gotchas
- PIX capture of a frame that uses DXR or mesh shaders needs a PIX version that
  supports those features — older PIX silently shows incomplete data for newer
  pipeline stages.
- Captures can be large (GBs) on complex frames — capture the minimal repro
  (isolate the failing pass if possible) rather than a full open-world frame when
  iterating repeatedly.
- PIX only sees what the API records: a bug in content (wrong UV authored in the
  asset) looks identical in a capture to a bug in code — rule out the asset first
  with a known-good test mesh/texture.

## Verify
- [ ] Debug layer and GPU-based validation checked clean before reaching for PIX.
- [ ] Correctness bug → GPU capture; performance bug → timing capture first (don't
      default to GPU capture for a "too slow" report).
- [ ] Event markers present per render pass so the capture timeline is self-explanatory.
- [ ] Repro isolated to the smallest frame/scene that still shows the bug before
      capturing, to keep capture size and triage time down.
