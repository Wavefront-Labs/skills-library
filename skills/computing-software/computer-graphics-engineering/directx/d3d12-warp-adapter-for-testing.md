---
id: computing-software.computer-graphics-engineering.directx.d3d12-warp-adapter-for-testing
name: d3d12-warp-adapter-for-testing
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-device, warp-adapter, software-rasterizer, graphics-ci]
level: practitioner
status: docs-checked
description: "Use the WARP software adapter for D3D12/D3D11 CI and golden-image tests: creating it, Agility SDK WARP versions, feature coverage, and determinism."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3darticles/directx-warp", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgifactory4-enumwarpadapter", "https://www.nuget.org/packages/Microsoft.Direct3D.WARP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WARP adapter for testing

WARP is Microsoft's software rasterizer for Direct3D (Direct3D 12 support is included starting with
Windows 10). It runs on build agents with no GPU, which makes it a basis for rendering unit tests and
golden-image CI on Windows.

## Create
```cpp
ComPtr<IDXGIFactory4> factory; CreateDXGIFactory2(0, IID_PPV_ARGS(&factory));
ComPtr<IDXGIAdapter> warp; factory->EnumWarpAdapter(IID_PPV_ARGS(&warp));
ComPtr<ID3D12Device> device;
D3D12CreateDevice(warp.Get(), D3D_FEATURE_LEVEL_11_0, IID_PPV_ARGS(&device));
// D3D11: D3D11CreateDevice(nullptr, D3D_DRIVER_TYPE_WARP, ...)
```
Expose `--warp` on the command line so developers can reproduce CI results locally.

## Newer WARP via NuGet
The OS WARP can lag newer features. The NuGet package `Microsoft.Direct3D.WARP` provides WARP binaries
for testing: place `d3d10warp.dll` next to the application .exe. Microsoft states these DLLs cannot be
redistributed, so use them for development and CI only.

## Golden-image tests
1. Render a fixed scene with fixed time, resolution and seed.
2. Read back the render target (readback heap copy) and compare against a stored PNG with a
   tolerance (per-channel abs diff or PSNR > threshold), since WARP updates can change
   rounding slightly.
3. Store diffs as CI artefacts.
Pin the WARP package version in CI so results do not change between runs.

## Uses beyond CI
- Reference rasterizer to tell driver bugs from app bugs: if WARP renders correctly and a GPU
  doesn't, collect a repro for the vendor.

## Gotchas
- Software rendering is slow for heavy scenes; keep test scenes small.
- Optional features may be absent; query `CheckFeatureSupport` and skip tests accordingly.
- Timing tests on WARP do not reflect GPU performance.

## Verify
- [ ] CI job runs rendering tests on WARP with no GPU and fails on a deliberate shader change beyond tolerance.

## Checked

2026-10-26. Checked against the Microsoft Learn WARP guide (Direct3D 12 on Windows 10, NuGet binaries, d3d10warp.dll placement,
non-redistributable) and IDXGIFactory4::EnumWarpAdapter (win32 and sdk-api repositories, commits to 2026-10).
Removed the unconfirmed feature-level 12_1 claim, determinism claim, 4K timing claim, debug-layer-on-WARP claim and
the list of newer features supplied by the package.
Method: documentation only; no commands were run.
