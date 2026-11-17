---
id: computing-software.web-development.webassembly.audioworklet-and-webgl
name: audioworklet-and-webgl
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, audio-worklet, webgl-wasm, wgpu-web, wasm]
level: practitioner
status: docs-checked
description: "Run Wasm DSP inside an AudioWorkletProcessor, which processes audio in 128-frame blocks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletProcessor/process
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_AudioWorklet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AudioWorklet with Wasm

Goal: connect Wasm to the Web Audio API.
- An `AudioWorkletProcessor`'s `process()` method receives audio data blocks that are currently always 128 frames long (128 32-bit float samples per channel of each input); parameter arrays hold either 1 or 128 values. Call your Wasm DSP from `process()` on those blocks.
- MDN notes that building the audio processing algorithm with WebAssembly can improve performance markedly.
Verify: audio is glitch-free at the target buffer size.

## Checked
Read the intro and parameter sections of the MDN AudioWorkletProcessor.process() page and the WebAssembly note in the Using AudioWorklet page on 2026-11-08; neither page was read end to end. Confirmed the 128-frame block size, the 1-or-128 parameter values, and the Wasm performance note. Removed: the avoid-allocation-in-the-audio-thread advice, the WebGL (Emscripten GL layer) and WebGPU (wgpu / Dawn) claims, and the generic spec, component-model and WASI sources, none read for this skill. The skill name still mentions WebGL; see the webgpu-from-wasm skill for GPU work.
Method: docs-only read of cited pages, 2026-11-08
