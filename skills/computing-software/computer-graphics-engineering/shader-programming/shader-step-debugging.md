---
id: computing-software.computer-graphics-engineering.shader-programming.shader-step-debugging
name: shader-step-debugging
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, shader-step-debugging, renderdoc, pix-shader-debugger, nsight]
level: advanced
status: gated
description: "Step through shaders line by line in RenderDoc, PIX and Nsight: pick a pixel/vertex/thread, build with debug info, inspect variables, and work around limits."
sources: ["https://renderdoc.org/docs/how/how_debug_shader.html", "https://github.com/microsoft/DirectXShaderCompiler/wiki/Using-dxc.exe-and-dxcompiler.dll", "https://github.com/KhronosGroup/glslang", "https://github.com/shader-slang/slang/blob/master/docs/command-line-slangc-reference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stepping shaders in RenderDoc, PIX and Nsight

## 1. Build with debug info
- DXC (DXIL): `-Zi` for debug info, `-Od` to disable optimisation, `-Fd` for a separate PDB.
- Vulkan: RenderDoc reads source-level info from NonSemantic.Shader.DebugInfo.100; generate it
  with glslang `-gVS` or DXC SPIR-V `-fspv-debug=vulkan-with-source`.
- Slang: `-g3` is a documented debug level (`-g` takes a level or format).
Without it you step through disassembly/SPIR-V only.

## 2. RenderDoc
1. Capture (F12), pick the draw in Event Browser.
2. Texture Viewer: select a pixel, then Debug, or open Pixel History (every modification of the
   pixel) and debug any triangle that changed it. With overdraw, Debug directly uses the last
   fragment that passed the depth test.
3. Mesh Viewer: select an input vertex, right-click, Debug Vertex. Compute: in the compute shader
   section of the pipeline state viewer, enter the group and thread ID.
4. Step forward/back (F10 / Shift+F10), run to cursor (Ctrl+F10), run (F5), breakpoint (F9),
   hover registers, add watch expressions.
Shader debugging is supported on D3D11, D3D12 and Vulkan only; geometry and tessellation shaders
are not yet debuggable.

## 3. PIX (D3D12)
PIX has its own shader debugger for D3D12 captures; its page could not be fetched (gated: unconfirmed, source is paywalled or blocked).

## 4. Nsight Graphics
Nsight Graphics has a shader debugger; its user guide could not be read here (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Not every shader can be debugged (for example when an unsupported Vulkan extension is used).
- For the best experience build with `-Od`; RenderDoc enables HLSL-level debugging by default for unoptimised shaders and offers a toggle between assembly and HLSL.

## Verify
- [ ] You can stop on the line computing the wrong value and see the bad input.

## Checked
- 2026-10-28. Confirmed in the RenderDoc "How do I debug a shader?" page: supported APIs, debug pixel/vertex/compute-thread flow, shortcuts F5/F9/F10/Ctrl+F10, `-gVS` and `-fspv-debug=vulkan-with-source`. Confirmed in the DXC usage page: `-Zi`, `-Od`, `-Fd`. Confirmed in the slangc reference: `-g` levels incl. `-g3`.
- Removed: `-Qembed_debug` (not in the DXC page), glslang plain `-g`, CPU-emulation and denormal claims, quad-simulation claim, PIX edit-and-continue and Nsight live-breakpoint claims (PIX page 404, Nsight guide stub).
Method: documentation only; no commands were run.
