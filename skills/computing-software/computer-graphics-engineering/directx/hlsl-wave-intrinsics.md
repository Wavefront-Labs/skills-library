---
id: computing-software.computer-graphics-engineering.directx.hlsl-wave-intrinsics
name: hlsl-wave-intrinsics
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, wave-intrinsics, waveactivesum, waveprefixsum, wavereadlanefirst, shader-model-6, subgroup-operations, scalarization, atomic-aggregation]
level: advanced
status: docs-checked
description: "Use HLSL Shader Model 6 wave intrinsics for reductions, prefix sums, atomic aggregation and scalarisation, with portable wave-size assumptions and helper-lane rules."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_WaveSize.md", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_7_Wave_Ops_Include_Helper_Lanes.md", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_DynamicResources.md", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/hlsl-shader-model-6-0-features-for-direct3d-12"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL wave intrinsics

**Goal:** exploit the fact that the lanes of a wave execute together: reduce without shared
memory, cut atomics to one per wave, and keep divergent indices scalar.

## 1. Core intrinsics (SM 6.0)
| intrinsic | use |
|---|---|
| `WaveGetLaneCount()`, `WaveGetLaneIndex()` | lane count and this lane's index (wave sizes are powers of 2 from 4 to 128) |
| `WaveActiveSum/Min/Max/BitOr(x)` | reduction across active lanes |
| `WavePrefixSum(x)`, `WavePrefixCountBits(b)` | exclusive scan |
| `WaveActiveAnyTrue/AllTrue(b)`, `WaveActiveBallot(b)` | votes |
| `WaveReadLaneFirst(x)`, `WaveReadLaneAt(x, i)` | broadcast |
| `WaveIsFirstLane()` | elect one lane |
| `QuadReadAcrossX/Y/Diagonal` | pixel-quad exchange (derivatives, 2x2 filters) |

## 2. Atomic aggregation (append buffers, counters)
```hlsl
bool keep = visible;
uint laneOffset = WavePrefixCountBits(keep);
uint waveCount  = WaveActiveCountBits(keep);
uint base;
if (WaveIsFirstLane()) InterlockedAdd(gCounter[0], waveCount, base);
base = WaveReadLaneFirst(base);
if (keep) gOut[base + laneOffset] = item;
```
One atomic per wave instead of per thread.

## 3. Reductions
```hlsl
float waveSum = WaveActiveSum(v);
if (WaveIsFirstLane()) gsPartial[waveIdInGroup] = waveSum;   // then reduce the partials
```
Replaces the log2(N) shared-memory tree steps for the first level.

## 4. Scalarisation of divergent resource indices
```hlsl
uint idx = materialId;                 // varies per lane
[loop] while (true) {
    uint first = WaveReadLaneFirst(idx);
    if (first == idx) { color = Textures[NonUniformResourceIndex(first)].Sample(s, uv); break; }
}
```
Each unique index executes once with a uniform descriptor index; `NonUniformResourceIndex` is
required when the index is not uniform, otherwise the result may be undefined.

## 5. Compile and portability
- `dxc -T cs_6_0` minimum; Shader Model 6.6 adds the `[WaveSize(n)]` attribute on compute shader
  entry points (allowed sizes 4, 8, 16, 32, 64, 128; check `WaveLaneCountMin/Max` in
  `D3D12_FEATURE_DATA_D3D12_OPTIONS1`).
- Never hard-code the wave size: size shared arrays by `MAX_WAVES = groupSize / WaveLaneCountMin`.

## Gotchas
- **Active lanes only**: inside a branch, inactive lanes don't participate. Results differ
  from what a "whole wave" mental model expects.
- Pixel shaders: by default only non-helper lanes participate in wave operations; Shader Model
  6.7 adds the `WaveOpsIncludeHelperLanes` option to include helper lanes.

## Verify
- [ ] Compaction pass output equals a reference CPU implementation (count and set).
- [ ] Shader runs correctly at more than one wave size (test on two devices).
- GPU timing: atomic-heavy pass measured before and after aggregation.

## Checked

2026-10-26. Checked against the DirectX-Specs documents HLSL_SM_6_6_WaveSize (allowed sizes 4 to 128, compute entry points),
HLSL_SM_6_7_Wave_Ops_Include_Helper_Lanes (default: only non-helper lanes participate) and HLSL_SM_6_6_DynamicResources
(NonUniformResourceIndex), plus d3d12.h (WaveLaneCountMin/Max in D3D12_FEATURE_DATA_D3D12_OPTIONS1) (DirectX-Specs
and DirectX-Headers repositories, commits to 2026-10). Fixed the helper-lane statement (the original said quad
operations and WaveActive differ by rule; the spec states the default and the SM 6.7 option). Removed the vendor
wave-size list, the AMD scalarisation speed claim, the cross-primitive and float-order notes and the SPIR-V
extension mapping.
Method: documentation only; no commands were run.
