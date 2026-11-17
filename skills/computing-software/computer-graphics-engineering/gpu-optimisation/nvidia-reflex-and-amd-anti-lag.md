---
id: computing-software.computer-graphics-engineering.gpu-optimisation.nvidia-reflex-and-amd-anti-lag
name: nvidia-reflex-and-amd-anti-lag
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, nvidia-reflex, anti-lag, input-latency, render-queue, streamline, latency-markers]
level: practitioner
status: draft
description: "Integrate latency reduction with NVIDIA Reflex or AMD Anti-Lag 2: sleep and markers APIs, what the render queue costs in latency, PC Latency measurement and pitfalls."
sources: ["https://developer.nvidia.com/performance-rendering-tools/reflex", "https://gpuopen.com/anti-lag-2/", "https://github.com/NVIDIAGameWorks/Streamline"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NVIDIA Reflex / AMD Anti-Lag integration

## 1. The problem
When GPU-bound, the CPU runs ahead and queues frames; input sampled at the start of a CPU frame is
displayed 2-3 frames later. Latency = queue depth x frame time + render time.

## 2. How Reflex works
The game calls a **sleep** function at the start of each frame; the driver delays the CPU so its
work finishes "just in time" for the GPU, keeping the render queue empty. Input is then sampled
later, cutting latency (often 30-50% when GPU-bound).
Integration via Reflex SDK (NVAPI) or Streamline:
```cpp
// once: NvAPI_D3D_SetSleepMode(device, &params) with bLowLatencyMode = true (and boost optional)
// each frame:
NvAPI_D3D_Sleep(device);                                 // before input sampling / simulation
NvAPI_D3D_SetLatencyMarker(device, SIMULATION_START), ... SIMULATION_END, RENDERSUBMIT_START, RENDERSUBMIT_END, PRESENT_START, PRESENT_END;
// INPUT_SAMPLE marker when reading input; TRIGGER_FLASH for click-to-photon test tools
```
Vulkan: `VK_NV_low_latency2`. Markers let the driver and tools (FrameView, GeForce overlay "PC
Latency") measure each stage.

## 3. AMD Anti-Lag 2
SDK with a similar in-game integration: call `AntiLag2::Update` (or the D3D12/Vulkan variants)
once per frame right before input polling; the driver delays the CPU to minimise queueing. Requires
supported Radeon drivers/GPUs. Integrate via the FidelityFX SDK.

## 4. Requirements and interactions
- Place the sleep/update call before input sampling, not after.
- Frame generation (DLSS FG / FSR FG) adds latency; Reflex/Anti-Lag are required/recommended
  alongside to offset it.
- Frame rate limiters: use the Reflex-aware limiter or let Reflex handle pacing; external limiters
  can conflict.

## 5. Measuring latency
- NVIDIA FrameView / overlay PC Latency (needs markers); LDAT or high-speed camera for end-to-end.
- Compare GPU-bound scenarios with Reflex off/on; CPU-bound scenes see little change.

## Gotchas
- Missing or misordered markers make metrics wrong and can reduce effectiveness.
- Anti-cheat/injection-based driver-level "Anti-Lag+" was withdrawn; use the SDK path (Anti-Lag 2).

## Verify
- [ ] PC latency reduced in GPU-bound tests with no frame rate loss beyond a few percent.
- [ ] Markers present for each stage in latency tools.
