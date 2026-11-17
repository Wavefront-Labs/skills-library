---
id: computing-software.computer-graphics-engineering.shader-programming.offline-shader-build-pipeline-and-caching
name: offline-shader-build-pipeline-and-caching
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, shader-build-pipeline, shader-cache, pso-cache, dxc, glslang, ninja, content-hash]
level: advanced
status: docs-checked
description: "Design an offline shader build pipeline: permutation enumeration, content-hash caching, include tracking, parallel compiles, debug/release artefacts and runtime PSO caches."
sources: ["https://github.com/microsoft/DirectXShaderCompiler/blob/main/include/dxc/Support/HLSLOptions.td", "https://github.com/KhronosGroup/glslang/blob/main/StandAlone/StandAlone.cpp", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#pipelines-cache", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/managing-graphics-pipeline-state-in-direct3d-12"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline shader build pipeline

Goal: every shader binary the game loads is built ahead of time, reproducibly, and rebuilt only
when something that affects it changed.

## 1. Inputs that define a binary
Hash all of them into the cache key:
- Preprocessed source (after includes) or source + the hash of every included file.
- Entry point, stage, target profile (`ps_6_6`, `spirv1.5`, `vulkan1.3`).
- Permutation defines (sorted `KEY=VALUE` list).
- Compiler binary version and flags (`-O3`, `-Zpc`, `-HV 2021`, `-fspv-target-env`).

`key = sha256(compiler_ver | flags | stage | entry | defines | preprocessed_source)`.
Preprocess with `dxc -P` (preprocess to file) or `glslangValidator -E` to get a canonical text to hash.

## 2. Build graph
- Emit one build edge per (shader, permutation, platform) into Ninja/FASTBuild or a custom job
  system; let it parallelise across cores.
- Generate depfiles (`dxc -MD` / `-MF <file>`, `glslangValidator --depfile <file>`) so editing a shared
  header rebuilds dependants only.
- Share a remote cache (S3, network drive) keyed by the hash; CI fills it, developers download.

## 3. Permutation control
- Enumerate permutations from material usage, not the full cartesian product. Log which variants
  are requested at runtime but missing; fail the build on new misses in CI.
- Keep a manifest: permutation key -> binary hash; the runtime looks up by key.

## 4. Artefacts per binary
| Artefact | Use |
|---|---|
| stripped, optimised binary | ship |
| PDB / debug SPIR-V (`-Zi -Qembed_debug`, `-g`) | source-level debugging in capture tools |
| reflection JSON (bindings, push constants, inputs) | build root signatures/descriptor layouts |
| disassembly + register/VGPR stats | perf review, diff in code review |

Name debug artefacts by the binary hash so a capture can locate them (DXC `-Fd` with a directory path
writes an automatically named PDB).

## 5. Runtime pipeline caches
Compiled bytecode is not the end: drivers compile again into ISA at PSO creation.
- Vulkan: `VkPipelineCache`, serialised with `vkGetPipelineCacheData`; validate the header
  (vendorID, deviceID, pipelineCacheUUID) before reuse.
- D3D12: `ID3D12PipelineLibrary` or cached PSO blobs (`GetCachedBlob`); cached data can be rejected by a different driver or adapter, so keep the fallback to a full compile.
- Pre-warm: record the PSO descriptions used in a playthrough, ship the list, create them during
  loading screens. This is the main fix for first-use hitching.

## Gotchas
- Timestamps in the hash, absolute paths in `#line` directives or embedded PDB paths make builds
  non-reproducible and destroy cache hit rates; normalise paths.
- Forgetting the compiler version in the key serves stale binaries after a toolchain upgrade.
- A single "uber include" touched by every shader turns every edit into a full rebuild; split it.

## Verify
- [ ] Clean build twice; second build is 100% cache hits and byte-identical outputs.
- [ ] Runtime log shows zero missing permutations over a full test run.
- [ ] PSO pre-warm list removes shader compile hitches in a fresh-install capture.

## Checked

Checked 2026-10-26 against DXC HLSLOptions.td and glslang StandAlone help text (main, 2026-10-23), Vulkan-Docs pipelines chapter, Microsoft D3D12 pipeline state docs. Confirmed: dxc flags `-P`, `-MD`, `-MF`, `-HV`, `-Zpc`, `-fspv-target-env=`, `-Zi`, `-Qembed_debug`, `-Fd`; glslang `-E` and `--depfile`; the `VkPipelineCache` header fields vendorID, deviceID and pipelineCacheUUID. Removed as unconfirmed: the claim that `dxc -P` also yields an include list, the PIX/Nsight tool names, and the exact D3D12 invalidation rule (now a hedge).

Method: documentation only; no commands were run.
