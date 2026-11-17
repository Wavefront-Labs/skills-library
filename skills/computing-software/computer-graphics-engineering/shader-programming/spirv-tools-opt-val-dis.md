---
id: computing-software.computer-graphics-engineering.shader-programming.spirv-tools-opt-val-dis
name: spirv-tools-opt-val-dis
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, spirv-opt, spirv-val, spirv-dis, spirv-tools, spir-v, vulkan, shader-compilation]
level: practitioner
status: docs-checked
description: "Use SPIRV-Tools on shader binaries: spirv-val to catch invalid modules, spirv-opt passes for size/perf, spirv-dis/as for reading and patching, spirv-reduce for repros."
sources: ["https://github.com/KhronosGroup/SPIRV-Tools", "https://github.com/KhronosGroup/SPIRV-Tools/blob/main/tools/opt/opt.cpp", "https://github.com/KhronosGroup/SPIRV-Tools/blob/main/tools/val/val.cpp", "https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPIRV-Tools: validate, optimise, disassemble

SPIRV-Tools ships with the Vulkan SDK (and most distro `spirv-tools` packages). It operates on
`.spv` binaries produced by glslang, DXC (`-spirv`), slangc or clspv.

## 1. Validate before you ship
```bash
spirv-val --target-env vulkan1.3 shader.spv            # exit 0 = valid
spirv-val --target-env vulkan1.2 --scalar-block-layout shader.spv   # match enabled device features
spirv-val --relax-block-layout --before-hlsl-legalization shader.spv
```
- Always pass the same `--target-env` the app's `VkApplicationInfo.apiVersion` uses; a module valid
  for 1.3 may use instructions illegal for 1.1.
- Layout flags (`--scalar-block-layout`, `--relax-block-layout`, `--uniform-buffer-standard-layout`)
  must match the device features you enable, otherwise validation lies in either direction.
- The validation layers call the same validator at `vkCreateShaderModule`; running it offline in CI
  catches errors before the driver does.

## 2. Optimise
```bash
spirv-opt -O shader.spv -o shader.opt.spv        # performance recipe
spirv-opt -Os shader.spv -o shader.small.spv     # size recipe
spirv-opt --legalize-hlsl in.spv -o out.spv      # what DXC runs on HLSL output
spirv-opt --strip-debug --strip-nonsemantic -O in.spv -o release.spv
spirv-opt --print-all -O in.spv -o out.spv 2> passes.log    # dump after every pass
```
Individual passes are useful on their own: `--eliminate-dead-code-aggressive`, `--merge-blocks`,
`--scalar-replacement=100`, `--loop-unroll`, `--set-spec-const-default-value "1:42"` (bake a
specialisation constant), `--compact-ids` (renumber result ids from %1 with no gaps) and `--canonicalize-ids` (better compression of shipped
binaries; run `--strip-debug` after it because it uses `OpName`).

Drivers run their own optimiser; measure before assuming a runtime win from `-O`.

## 3. Read and patch
```bash
spirv-dis shader.spv -o shader.spvasm --raw-id   # raw numeric ids instead of friendly names
spirv-as shader.spvasm -o shader.spv --target-env vulkan1.3
spirv-cfg shader.spv                              # control-flow graph in Graphviz dot form (marked experimental)
```
Disassembly is the ground truth for "what decorations did the compiler emit": check
`OpDecorate %x Binding 3`, `DescriptorSet`, `Offset`, `ArrayStride`, `RelaxedPrecision`, and
`OpExecutionMode %main LocalSize 64 1 1`.

## 4. Shrink a crashing shader for a driver bug report
```bash
spirv-reduce crash.spv -o reduced.spv -- ./still_crashes.sh   # script exits 0 when bug reproduces
spirv-fuzz ...   # optional tool, off by default in builds (SPIRV_BUILD_FUZZER=ON); see spirv-fuzz --help
```

## 5. Link
`spirv-link a.spv b.spv -o linked.spv` links modules with `Export`/`Import` linkage decorations.

## Gotchas
- `spirv-opt` without `--target-env` defaults to spv1.5 rules and can emit
  instructions older drivers reject; pass `--target-env=vulkan1.1` etc.
- Stripping debug info breaks RenderDoc/Nsight source-level debugging; keep a debug build of each
  module keyed by hash.
- `spirv-val` passing does not mean the driver supports every capability declared; check
  `OpCapability` lines against device features.

## Verify
- [ ] CI runs `spirv-val --target-env <your env>` over every built `.spv`.
- [ ] Release modules optimised and stripped; debug copies archived by hash.

## Checked

Checked 2026-10-26 against SPIRV-Tools main (commit of 2026-10-24), tools/*/ CLI help text. Confirmed: spirv-val, spirv-opt, spirv-dis, spirv-as, spirv-reduce and spirv-cfg flag names and help text (`--target-env`, `--relax-block-layout`, `--scalar-block-layout`, `--uniform-buffer-standard-layout`, `--before-hlsl-legalization`, `--legalize-hlsl`, `--strip-debug`, `--strip-nonsemantic`, `--print-all` to stderr, `--set-spec-const-default-value`, `--compact-ids`, `--canonicalize-ids`); the spirv-opt default target environment is spv1.5; spirv-reduce takes the interestingness script after `--`; spirv-fuzz and spirv-link are listed in the README, the fuzzer is built only with `SPIRV_BUILD_FUZZER=ON`. Corrected: default env (was 1.6), removed the non-existent `--remap-ids`/`spirv-remap` claim.

Method: documentation only; no commands were run.
