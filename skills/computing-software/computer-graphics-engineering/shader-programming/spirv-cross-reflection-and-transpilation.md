---
id: computing-software.computer-graphics-engineering.shader-programming.spirv-cross-reflection-and-transpilation
name: spirv-cross-reflection-and-transpilation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, spirv-cross, shader-reflection, spirv-reflect, cross-compilation]
level: advanced
status: docs-checked
description: "Reflect SPIR-V resources and cross-compile to GLSL, HLSL and MSL with SPIRV-Cross (CLI and C++ API), including binding remaps and common breakages."
sources: ["https://github.com/KhronosGroup/SPIRV-Cross", "https://github.com/KhronosGroup/SPIRV-Cross/blob/main/main.cpp", "https://github.com/KhronosGroup/SPIRV-Cross/blob/main/spirv_cross.hpp", "https://github.com/KhronosGroup/SPIRV-Reflect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPIRV-Cross reflection and transpilation

## 1. CLI
```bash
glslangValidator -V shader.frag -o shader.spv          # or dxc -spirv / slangc
spirv-cross shader.spv --reflect                        # JSON: inputs, outputs, ubos, ssbos, textures, push constants
spirv-cross shader.spv --version 330 --no-es --output shader.gl.frag
spirv-cross shader.spv --es --version 300 --output shader.es.frag
spirv-cross shader.spv --hlsl --shader-model 50 --output shader.hlsl
spirv-cross shader.spv --msl --msl-version 20100 --output shader.metal
```

## 2. C++ reflection
```cpp
spirv_cross::CompilerGLSL comp(spirvWords);
auto res = comp.get_shader_resources();
for (auto& ub : res.uniform_buffers) {
  uint32_t set = comp.get_decoration(ub.id, spv::DecorationDescriptorSet);
  uint32_t bnd = comp.get_decoration(ub.id, spv::DecorationBinding);
  size_t size = comp.get_declared_struct_size(comp.get_type(ub.base_type_id));
}
for (auto& s : res.sampled_images) { /* name, set, binding */ }
```
Use this to build descriptor set layouts / root signatures automatically. SPIRV-Reflect (KhronosGroup/SPIRV-Reflect) is a
separate reflection-only library.

## 3. Remapping for GL / Metal
- GL has no descriptor sets: flatten `set*N + binding` and call `comp.set_decoration(id, Binding, b)`
  then `unset_decoration(id, DescriptorSet)`.
- Combined image samplers for GL: `comp.build_combined_image_samplers()` then name them.
- Metal: `CompilerMSL::add_msl_resource_binding` to map set/binding to buffer/texture indices;
  argument buffers via `msl_options.argument_buffers`.
- Push constants become a plain uniform struct in GLSL by default; pass `--glsl-emit-push-constant-as-ubo` (API: `emit_push_constant_as_uniform_buffer`) to get a UBO block, and give it a binding.

## Gotchas
- Resource names come from `OpName`; if the module was stripped, key reflection on set/binding instead.
- `--hlsl-enable-compat` allows point size and point coord in HLSL output even though they will not work as expected (PointSize is ignored, PointCoord returns (0.5, 0.5)).
- Matrix layout: check row/column-major decorations in the output against a known transform.

## Verify
- [ ] Reflected sizes equal C++ struct sizes (`static_assert`).
- [ ] Transpiled shaders compile on each target and render the same reference frame.

## Checked

Checked 2026-10-26 against SPIRV-Cross main (last commit 2026-10-14), main.cpp CLI help and headers. Confirmed: CLI flags `--reflect`, `--version`, `--es`, `--no-es`, `--output`, `--hlsl`, `--shader-model`, `--hlsl-enable-compat`, `--msl`, `--msl-version` (MMmmpp, 20100 = MSL 2.1), `--msl-argument-buffers`, `--glsl-emit-push-constant-as-ubo`; API names `get_shader_resources`, `get_declared_struct_size`, `set_decoration`/`unset_decoration`, `build_combined_image_samplers`, `CompilerMSL::add_msl_resource_binding`, `Options::argument_buffers`. Corrected: push constants are not a UBO by default; `--hlsl-enable-compat` is about point size/coord only.

Method: documentation only; no commands were run.
