---
id: computing-software.computer-graphics-engineering.gpu-optimisation.diagnosing-stutter-and-hitching
name: diagnosing-stutter-and-hitching
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, stutter-diagnosis, hitching, frame-time, pso-compilation, shader-cache, streaming]
level: practitioner
status: draft
description: "Diagnose stutter and hitches: frame-time graphs vs averages, shader/PSO compilation, streaming and GC spikes, present pacing problems, and capturing the offending frame."
sources: ["https://www.gdcvault.com/play/1027025/", "https://github.com/GameTechDev/PresentMon", "https://docs.unrealengine.com/5.3/en-US/psocaching-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing stutter (hitches)

## 1. Measure frame times, not averages
- Record per-frame times with **PresentMon** (`PresentMon --process_name game.exe --output_file
  out.csv`) or Intel PresentMon UI / CapFrameX / FrameView; look at the frame-time graph and 1% /
  0.1% lows.
- Distinguish: single spikes (hitches), periodic spikes (GC, streaming ticks, autosave), and
  alternating pattern (pacing problem, e.g. 16/33 ms alternation).

## 2. Common causes
| Pattern | Likely cause | Where to look |
|---|---|---|
| spike first time an effect/area appears | shader/PSO compilation | driver compile time in CPU profiler, PSO creation logs |
| spikes while moving through the world | streaming I/O, texture uploads, decompression on main thread | I/O tracks, upload sizes |
| regular spikes every N seconds | garbage collection, periodic tasks | managed heap events, task schedulers |
| spikes on spawning | allocation, physics init, material instance creation | CPU profiler |
| alternating frame times with vsync | frame rate just below refresh, no VRR | present mode; target a stable rate |
| GPU spikes | resource eviction (VRAM over budget), large first-use resource init | VRAM budget, GPU timeline |

## 3. Capture the bad frame
- Tracy/Superluminal/PIX with continuous capture; mark spikes (`if (frameTime > 2 * avg)` log and
  snapshot zone stats).
- Unreal: `stat unitgraph`, `-csvprofile`, Insights traces; Unity: Profiler with "deep profile" off,
  record and find spikes.

## 4. Fixes
- PSO precaching / pre-warming (UE PSO precache and bundled PSO caches; Vulkan pipeline cache
  shipped and warmed; D3D12 pipeline libraries), async PSO compilation with fallback.
- Move I/O, decompression and asset init off the main/render threads; budget uploads per frame.
- Pool objects to avoid allocation/GC; incremental GC where available.
- Keep VRAM under budget to avoid driver paging.

## Gotchas
- Average fps hides stutter completely; always report percentiles.
- Fresh driver install / cleared shader caches reproduce compilation hitches that developers
  rarely see; test on clean caches.

## Verify
- [ ] 0.1% low frame time within ~2x median on a clean-cache playthrough.
- [ ] Each remaining spike has an identified cause.
