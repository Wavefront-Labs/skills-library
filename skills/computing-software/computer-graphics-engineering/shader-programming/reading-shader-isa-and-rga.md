---
id: computing-software.computer-graphics-engineering.shader-programming.reading-shader-isa-and-rga
name: reading-shader-isa-and-rga
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-optimisation, shader-isa, radeon-gpu-analyzer, vgpr, occupancy, disassembly]
level: sme
status: docs-checked
description: "Read compiled shader ISA with Radeon GPU Analyzer, Nsight SASS views or Mali Offline Compiler to find register pressure, spills, waitcnts and wasted instructions."
sources: ["https://github.com/GPUOpen-Tools/radeon_gpu_analyzer", "https://github.com/GPUOpen-Tools/radeon_gpu_analyzer/blob/master/documentation/source/help_manual.rst", "https://github.com/GPUOpen-Tools/radeon_gpu_analyzer/blob/master/source/common/rga_cli_defs.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading compiler output (ISA)

## 1. Get the ISA
| Vendor | Tool |
|---|---|
| AMD | Radeon GPU Analyzer (RGA): `rga -s vk-offline-spv --asic <target> --isa <file> --livereg <file> ...` for SPIR-V binary input (run `rga -s vk-offline-spv -h` for the stage and input options; `-s` picks the mode, e.g. `dx12`, `vulkan`, `opencl`) |
| Other vendors | use the vendor's own offline compiler or profiler; check its documentation |
| Any | DXC `-Fc` writes a DXIL listing, not GPU ISA |

## 2. What to read first
- **Register usage** (vector/scalar registers on AMD): crossing an occupancy step reduces the waves in flight; RGA can
  show the point of peak vector-register pressure and map it back to source lines when debug info is present.
- **Spills** (scratch memory loads/stores): reduce live values.
- **Waits** right after a load: latency not hidden; move independent math between load and use.
- Instruction count of the hot path; transcendental instructions cost more than plain arithmetic.

## 3. Typical fixes
- Hoist uniform math out of the shader (precompute on CPU or in a constant).
- Shorten live ranges: compute values right before use; avoid large arrays indexed dynamically
  (they go to scratch).
- Use half precision where the hardware has packed fp16 (see the fp16 skill).
- Replace divergent loops with fixed-count unrolled loops when small.

## Gotchas
- RGA's offline mode produces less accurate ISA and resource statistics than compiling through the live driver; match
  the pipeline state to your shaders where you can.
- Fewer instructions is not always faster if it increases registers.

## Verify
- [ ] Before/after ISA diff: registers, spills and cycle estimates improved, frame time confirmed.

## Checked

Checked 2026-10-26 against Radeon GPU Analyzer README, help manual and CLI option definitions (GPUOpen-Tools/radeon_gpu_analyzer, last commit 2026-10-06). Confirmed: RGA `-s` modes (`vk-offline-spv` for SPIR-V binary input, `vk-offline`, `vulkan`, `dx12`, `opencl`), `--isa`, `--livereg`, `--asic` option names; offline mode gives less accurate ISA than the live driver; peak VGPR pressure navigation and source-to-ISA correlation with debug info. Corrected: the mode name is `vk-offline-spv` (not `vk-spv-offline`). Removed as unconfirmed (vendor documentation not readable): the NVIDIA, Arm Mali, Qualcomm and Intel rows, specific ISA mnemonics and occupancy thresholds.

Method: documentation only; no commands were run.
