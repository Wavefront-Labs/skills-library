---
id: computing-software.computer-graphics-engineering.gpu-optimisation.xcode-metal-frame-debugger
name: xcode-metal-frame-debugger
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, xcode-gpu-debugger, metal, frame-capture, metal-system-trace, apple-gpu, shader-debugger]
level: practitioner
status: draft
description: "Debug and profile Metal with Xcode's GPU tools: frame capture, dependency viewer, shader debugger, performance counters and limiters, and Metal System Trace in Instruments."
sources: ["https://developer.apple.com/documentation/xcode/capturing-a-metal-workload-in-xcode", "https://developer.apple.com/documentation/xcode/optimizing-gpu-performance", "https://developer.apple.com/documentation/metal/debugging_tools"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Xcode Metal frame debugger

## 1. Capture
- Run from Xcode, click the Metal capture button (camera icon) in the debug bar, or capture
  programmatically:
```swift
let desc = MTLCaptureDescriptor(); desc.captureObject = device
desc.destination = .gpuTraceDocument; desc.outputURL = url    // .gputrace file for later
try MTLCaptureManager.shared().startCapture(with: desc)
// ... encode frame ...
MTLCaptureManager.shared().stopCapture()
```
Set `MTL_CAPTURE_ENABLED=1` when capturing outside Xcode. Label everything (`label` on encoders,
buffers, textures; `pushDebugGroup`).

## 2. Inspect
- **Summary** page: insights (e.g. "unused resource", "redundant binding", "large overdraw").
- **Dependency viewer**: graph of passes and resources; spot unnecessary loads/stores and passes.
- **Bound resources and attachments** per draw; geometry viewer for vertex input/output.
- **Shader debugger**: select a pixel or thread, step through source, view variable values per
  line (needs `-frecord-sources` or shader source in the library).
- **Shader source editing**: modify and reload to test fixes in the capture.

## 3. Performance
- **Counters / Performance** view: per-encoder and per-draw GPU time, limiter percentages (ALU,
  texture sample, memory read/write, tile memory, rasteriser, etc.) on Apple GPUs.
- **Shader cost graph / heat maps**: per-line cost in shaders (Apple silicon).
- **Instruments > Metal System Trace**: timeline of CPU encoding, GPU vertex/fragment/compute work,
  drawable presentation and frame pacing over many frames.

## 4. Apple GPU specifics to look for
- Load/store actions: avoid `.load`/`.store` when not needed (tile memory, TBDR).
- Memoryless render targets (`.memoryless` storage) for depth/MSAA that never leave tile memory.
- `half` precision usage in fragment shaders.

## Gotchas
- Capturing large frames in debug builds is slow; use release builds with labels.
- Performance counters require a physical device (not the Simulator).

## Verify
- [ ] Captures show labelled passes; dependency viewer has no stray store actions.
- [ ] Limiter percentages checked for the most expensive encoder.
