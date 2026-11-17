---
id: computing-software.computer-graphics-engineering.shader-programming.shader-debugprintf
name: shader-debugprintf
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, debugprintf, shader-printf, gl-ext-debug-printf, vk-khr-shader-non-semantic-info, validation-layers, renderdoc, hlsl-printf]
level: practitioner
status: docs-checked
description: "Print values from GPU shaders: Vulkan debugPrintfEXT via the validation layer or RenderDoc, HLSL printf through DXC to SPIR-V, filtering to one pixel or thread."
sources: ["https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/debug_printf.md", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GLSL_EXT_debug_printf.txt", "https://github.com/baldurk/renderdoc/blob/v1.x/docs/how/how_debug_shader.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader debugPrintf

**Goal:** inspect actual values inside shaders — compute kernels especially — without
writing debug buffers by hand.

## 1. In the shader
```glsl
#version 460
#extension GL_EXT_debug_printf : enable
void main() {
    uvec2 p = gl_GlobalInvocationID.xy;
    if (p == uvec2(512, 300))                                        // filter to ONE invocation
        debugPrintfEXT("p=%v2u depth=%f n=%v3f\n", p, depth, normal);
}
```
HLSL (DXC → SPIR-V): `printf("x=%f\n", x);` compiles to the same NonSemantic.DebugPrintf
instruction. Format specifiers like C plus vectors (`%v3f`, `%v4u`; form `%[0][width][.precision]v[2|3|4]specifier`), `%lu`/`%lx` for 64-bit.
The call compiles to `NonSemantic.DebugPrintf` instructions; some older compiler stacks handle unknown
NonSemantic instructions badly, so remove printf from release shaders.

## 2. Getting the output
- **Validation layer**: use Vulkan Configurator (`vkconfig`) with the `Debug Printf Only` preset, or set
  `VK_LAYER_PRINTF_ONLY_PRESET=1` (Vulkan SDK 1.4.304 or later; turns off the other validation). To keep
  other validation on, use `VK_LAYER_PRINTF_ENABLE=1` (`printf_enable` layer setting). Messages arrive in
  the debug callback, or on stdout with `VK_LAYER_PRINTF_TO_STDOUT=1` (`printf_to_stdout`).
- **RenderDoc**: release 1.14 or later consumes debug printf for captured events, no layer configuration.
- `VK_KHR_shader_non_semantic_info` should be supported (core in 1.3); the layers enable it for you, and strip the
  printf instructions from the instrumented shader if it is unavailable. Vulkan 1.1 or later is required, and the
  layers need `fragmentStoresAndAtomics`, `vertexPipelineStoresAndAtomics` and `timelineSemaphore` (they enable
  them when the device supports them).

## 3. Practical tips
- Always filter by pixel/thread/ID — unfiltered printf from a full-screen pass floods the buffer
  (the layer's printf buffer defaults to 1024 bytes; raise it with `VK_LAYER_PRINTF_BUFFER_SIZE` / `printf_buffer_size`).
- Print in compute kernels at specific `gl_WorkGroupID` / `gl_LocalInvocationIndex` to debug
  reductions and barriers.
- Pair with a mouse-picked pixel uniform: print whatever is under the cursor live.

## 4. Alternatives
- RenderDoc / PIX / Nsight shader step debugging for full variable state at one pixel.
- Debug output buffers (atomics + struct records) when you need lots of data or a non-Vulkan API: write to
  a storage buffer and read it back.

## Gotchas
- printf changes timing and register allocation — race conditions may disappear.
- Debug printf also consumes the last descriptor set (`maxBoundDescriptorSets - 1`) and device memory, so it fails if the app uses every descriptor set.

## Verify
- [ ] A filtered printf in a compute shader appears in the validation callback.
- [ ] Release shader builds strip printf (define-guarded).
- [ ] RenderDoc 1.14 or later shows the printf output for a captured frame.

## Checked

Checked 2026-10-26 against Vulkan-ValidationLayers docs/debug_printf.md (main) and GL_EXT_debug_printf. Confirmed: layer environment variables and settings (`VK_LAYER_PRINTF_ONLY_PRESET`, `VK_LAYER_PRINTF_ENABLE`, `VK_LAYER_PRINTF_TO_STDOUT`, `VK_LAYER_PRINTF_BUFFER_SIZE`, default 1024 bytes), vector specifier grammar and `%lu`, HLSL/Slang `printf` support, feature requirements and limitations (last descriptor set, Vulkan 1.1+, RenderDoc 1.14+). Corrected: buffer default was 1 MB; removed the unconfirmed GPU-assisted-validation, Metal, WebGPU and OpenGL remarks and the old validation-feature enum.

Method: documentation only; no commands were run.
