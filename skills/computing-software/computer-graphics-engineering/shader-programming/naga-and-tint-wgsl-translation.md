---
id: computing-software.computer-graphics-engineering.shader-programming.naga-and-tint-wgsl-translation
name: naga-and-tint-wgsl-translation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, naga, tint, wgsl, webgpu, wgpu, dawn, shader-translation, spir-v]
level: practitioner
status: docs-checked
description: "Translate and validate WGSL with Naga (wgpu) and Tint (Dawn): CLI usage, WGSL to SPIR-V/MSL/HLSL/GLSL, binding remaps, and common translation failures."
sources: ["https://github.com/gfx-rs/wgpu/tree/trunk/naga", "https://github.com/gfx-rs/wgpu/blob/trunk/naga-cli/src/bin/naga.rs", "https://github.com/google/dawn/blob/main/src/tint/cmd/tint/main.cc", "https://www.w3.org/TR/WGSL/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naga and Tint

WebGPU implementations never hand WGSL to the driver directly. wgpu uses **Naga**
(Rust); Dawn uses **Tint** (C++). Both parse WGSL, validate it against the spec, and emit
the native language: SPIR-V (Vulkan), MSL (Metal), HLSL (D3D12), GLSL (GL backend).

## 1. Naga CLI
```bash
cargo install naga-cli
naga shader.wgsl                         # validate only
naga shader.wgsl out.spv                 # WGSL -> SPIR-V
naga shader.wgsl out.metal --metal-version 2.4
naga shader.wgsl out.hlsl --shader-model 60
naga shader.wgsl out.vert.glsl --entry-point vs_main --profile es310
naga shader.spv out.wgsl                 # SPIR-V -> WGSL (porting existing shaders)
naga shader.frag out.wgsl --input-kind glsl --shader-stage frag
```
Output format is chosen by extension. Errors print with spans into the source, which is the
fastest way to see why `device.createShaderModule` reported a compilation error in the browser.

## 2. Tint CLI
Built from the Dawn repo (`tint` target). Output format is inferred from the extension (.spv, .spvasm, .wgsl, .metal, .hlsl) or set with `--format` (`spirv`, `spvasm`, `msl`, `hlsl`, `hlsl-fxc`, `glsl`, `wgsl`, depending on build options):
```bash
tint shader.wgsl --format spirv -o out.spv
tint shader.wgsl --format msl -o out.metal
tint shader.wgsl --format hlsl -o out.hlsl
tint shader.wgsl --format wgsl              # round-trip through the WGSL writer
tint shader.spv --format wgsl               # SPIR-V input (needs a Tint build with the SPIR-V reader)
```

## 3. Binding remapping
WGSL `@group(g) @binding(b)` does not map 1:1 onto Metal argument indices or HLSL registers.
- wgpu: the backend builds a binding map per pipeline layout; in Naga's API pass
  `back::msl::Options { per_entry_point_map, .. }` or `back::hlsl::Options { binding_map, .. }`.

When writing a custom native backend from WGSL, generate the map from the pipeline layout rather
than assuming `register(b{binding}, space{group})`.

## 4. Common failures
| Symptom | Cause |
|---|---|
| "uniformity analysis" error on `textureSample` | derivative op in non-uniform control flow; move it out or use `textureSampleLevel` |
| type mismatch on `vec3<f32>` in uniform struct | WGSL alignment: vec3 aligns to 16; add explicit padding fields |
| works with one implementation, fails with the other | the two compilers can differ in spec revision or bugs; check both and file the bug with a minimal repro |
| `f16` rejected | needs `enable f16;` and the `shader-f16` device feature |
| SPIR-V input rejected by Naga | unsupported capability or extension |

## Gotchas
- Naga's GLSL frontend (`--input-kind glsl`) does not cover all of GLSL; read the error spans.
- Naga picks the output backend from the output extension (.spv, .metal, .hlsl, .wgsl, .glsl/.vert/.frag/.comp) and the GLSL profile from `--profile` (`core<version>` or `es<version>`).

## Verify
- [ ] Shaders validate with both `naga` and `tint` in CI if you ship on the web.
- [ ] Generated MSL/HLSL inspected once per new feature (f16, storage textures, atomics).

## Checked

Checked 2026-10-26 against wgpu trunk naga-cli source (naga.rs, back/msl, back/hlsl), Dawn main src/tint/cmd/tint/main.cc (last commit 2026-10-24), WGSL and WebGPU specs (gpuweb main). Confirmed: Naga CLI options `--metal-version` (major.minor), `--shader-model` (values like 50, 51, 60..66, not `6.0`), `--entry-point`, `--profile` (`es310`, `core330` style), `--input-kind` (glsl, spv, wgsl), `--shader-stage`, and output selection by extension; `back::msl::Options::per_entry_point_map` and `back::hlsl::Options::binding_map`; Tint `--format`/`-f` names and extension inference, `--input-format`; WGSL `enable f16;` and the `shader-f16` feature; vec3 alignment 16; textureSample uniformity rule. Corrected: `--shader-model 6.0` is invalid, removed unconfirmed Dawn BindingRemapper, polyfill, robustness-clamp and Firefox/Chrome claims.

Method: documentation only; no commands were run.
