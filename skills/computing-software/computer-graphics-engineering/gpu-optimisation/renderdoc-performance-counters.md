---
id: computing-software.computer-graphics-engineering.gpu-optimisation.renderdoc-performance-counters
name: renderdoc-performance-counters
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, renderdoc-counters, renderdoc, performance-counters, event-timing, frame-debugger]
level: practitioner
status: draft
description: "Use RenderDoc's performance counter viewer: per-event GPU duration, vendor counters via AMD/NVIDIA/Intel integrations, and what RenderDoc timing can and cannot tell you."
sources: ["https://renderdoc.org/docs/window/performance_counter_viewer.html", "https://renderdoc.org/docs/how/how_view_texture.html", "https://renderdoc.org/docs/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RenderDoc performance counters

## 1. Where
After capturing a frame (F12/PrtScn in the app), open **Window > Performance Counter Viewer** and
click **Capture counters**. Select counters; RenderDoc replays the frame and reports values per
event (draw/dispatch).

## 2. Counters available
- Generic (all APIs/vendors): **GPU Duration** per event (timestamp-based), samples passed,
  input-assembler vertices/primitives, VS/PS/CS invocations, clipping counts.
- Vendor counters when supported: AMD (via GPUPerfAPI), NVIDIA (Nsight Perf SDK integration on
  supported drivers), Intel, Arm (Mali) - e.g. cache hit rates, ALU busy, occupancy.

## 3. Using it well
- Sort by GPU Duration to find expensive draws; correlate with Event Browser markers (name your
  passes with debug markers).
- **Samples passed / PS invocations vs pixels**: high ratios reveal overdraw.
- Compare invocations before/after culling or LOD changes.
- Export to CSV for diffing captures.
- Overlay modes in the Texture Viewer (Quad Overdraw, Triangle Size, Depth test, Clear before draw)
  complement counters for fill-rate issues.

## 4. Limits
- Timings come from replay, with RenderDoc's own state setup, often without the original async
  overlap or caches warmed the same way; absolute numbers differ from live frames. Use for relative
  comparisons between events.
- For timeline/overlap issues use PIX timing, Nsight GPU Trace, RGP or Instruments.

## Gotchas
- Per-event counters on very short draws are noisy; measure aggregate ranges (markers).
- Some counters require disabling RenderDoc API validation/vendor extensions in replay options.

## Verify
- [ ] Expensive events identified and confirmed in a vendor profiler.
- [ ] Overdraw ratio computed for the main pass.
