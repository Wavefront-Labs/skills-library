---
id: computing-software.computer-graphics-engineering.directx.d3d12-device-creation-agility-sdk-and-feature-support
name: d3d12-device-creation-agility-sdk-and-feature-support
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-device, adapter-enumeration, checkfeaturesupport, agility-sdk, d3d12sdkversion, enumadapterbygpupreference, shader-model, feature-level]
level: practitioner
status: docs-checked
description: "Create a Direct3D 12 device on the right adapter, ship the Agility SDK for new features, and gate features with CheckFeatureSupport (shader model, DXR, mesh shaders, VRS)."
sources: ["https://microsoft.github.io/DirectX-Specs/d3d/D3D12Redistributable.html", "https://microsoft.github.io/DirectX-Specs/d3d/D3D12_FeatureLevel12_2.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-checkfeaturesupport", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_feature_data_shader_model"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 device creation, Agility SDK and feature support

**Goal:** the high-performance GPU, the newest D3D12 runtime regardless of Windows
version, and every optional feature checked rather than assumed.

## 1. Pick the adapter
```cpp
ComPtr<IDXGIFactory6> factory; CreateDXGIFactory2(debug ? DXGI_CREATE_FACTORY_DEBUG : 0, IID_PPV_ARGS(&factory));
ComPtr<IDXGIAdapter1> adapter;
for (UINT i = 0; factory->EnumAdapterByGpuPreference(i, DXGI_GPU_PREFERENCE_HIGH_PERFORMANCE,
                                                       IID_PPV_ARGS(&adapter)) != DXGI_ERROR_NOT_FOUND; ++i) {
    DXGI_ADAPTER_DESC1 d; adapter->GetDesc1(&d);
    if (d.Flags & DXGI_ADAPTER_FLAG_SOFTWARE) continue;     // skip WARP / Basic Render Driver
    if (SUCCEEDED(D3D12CreateDevice(adapter.Get(), D3D_FEATURE_LEVEL_12_0, __uuidof(ID3D12Device), nullptr))) break;
}
D3D12CreateDevice(adapter.Get(), D3D_FEATURE_LEVEL_12_0, IID_PPV_ARGS(&device));
```
Log the adapter description, `DedicatedVideoMemory` and the adapter LUID. Allow a user override by adapter LUID.

## 2. Agility SDK (new D3D12 without OS updates)
Ship `D3D12Core.dll` (and `D3D12SDKLayers.dll` for the debug layer) from the NuGet package
`Microsoft.Direct3D.D3D12` in a subfolder, and export two symbols from the **application exe**:
```cpp
extern "C" { __declspec(dllexport) extern const UINT D3D12SDKVersion = 614; }   // value from the package you ship
extern "C" { __declspec(dllexport) extern const char* D3D12SDKPath = u8".\\D3D12\\"; }
```
- `D3D12SDKVersion` declares the SDK version you target; `D3D12SDKPath` is a UTF-8 path to the D3D12 binaries,
  relative to the exe. Install `D3D12Core.dll` into that folder.
- You still call `D3D12CreateDevice` on the inbox `D3D12.dll`. If the requested version is the same as or older than
  the inbox runtime, the inbox runtime is used. If it is newer, the runtime loads `D3D12Core.dll` from
  `D3D12SDKPath` and checks that it matches the declared version.
- The redistributable model is serviced to every retail build of Windows 10 version 1909 (19H2) and later.
- Retrieve the version of a given `D3D12Core.dll` from its exported `D3D12SDKVersion` variable.

## 3. Check features before use
```cpp
D3D12_FEATURE_DATA_SHADER_MODEL sm{D3D_SHADER_MODEL_6_8};
device->CheckFeatureSupport(D3D12_FEATURE_SHADER_MODEL, &sm, sizeof sm);   // HighestShaderModel = highest supported <= requested
D3D12_FEATURE_DATA_D3D12_OPTIONS5 o5{}; device->CheckFeatureSupport(D3D12_FEATURE_D3D12_OPTIONS5, &o5, sizeof o5);
bool dxr = o5.RaytracingTier >= D3D12_RAYTRACING_TIER_1_1;
D3D12_FEATURE_DATA_D3D12_OPTIONS7 o7{};  // MeshShaderTier, SamplerFeedbackTier
D3D12_FEATURE_DATA_D3D12_OPTIONS6 o6{};  // VariableShadingRateTier
D3D12_FEATURE_DATA_D3D12_OPTIONS12 o12{}; // EnhancedBarriersSupported
D3D12_FEATURE_DATA_D3D12_OPTIONS o{};     // ResourceBindingTier (Tier 3 required for SM 6.6 dynamic resources)
```
Shader model: set `HighestShaderModel` to the highest model your application understands; `CheckFeatureSupport`
returns `E_INVALIDARG` when the current runtime does not know that value, so loop downward from the highest.
It also returns `E_INVALIDARG` for an unsupported data type or a size mismatch.

## 4. Feature levels vs options
Feature level 12_2 is defined as a set of capabilities queryable with `CheckFeatureSupport`: raytracing tier 1.1,
variable shading rate tier 2, mesh shader tier 1, sampler feedback tier 0.9, resource binding tier 3, tiled
resources tier 3, conservative rasterization tier 3, root signature tier 1.1 and depth bounds test support.
Prefer checking the individual options; use the level as the minimum spec.

## Gotchas
- Laptops: without the `HIGH_PERFORMANCE` preference you can get the integrated GPU.
- Preview or experimental SDK features are for development only; selecting an SDK version at runtime through the
  device-factory path works only in Windows Developer Mode. Do not ship that.

## Verify
- [ ] Startup log: adapter name, VRAM, feature level, shader model, DXR/mesh/VRS tiers.
- [ ] On a machine lacking a feature the fallback path is taken, no crash.
- [ ] A process module list shows `D3D12Core.dll` loaded from your app folder.

## Checked
Date: 2026-10-26. Documentation: DirectX-Specs D3D12 redistributable and feature level 12_2 specs (2026-10-22),
`ID3D12Device::CheckFeatureSupport`, `D3D12_FEATURE_DATA_SHADER_MODEL` and `D3D12_FEATURE_DATA_D3D12_OPTIONS`
(MicrosoftDocs/sdk-api, last commit 2026-10-08). Confirmed: the two exe exports and their meaning, relative path,
inbox-versus-redist selection rule, Windows 10 1909 servicing, shader-model E_INVALIDARG loop, feature level 12_2
tier list, developer-mode restriction on runtime SDK selection, Tier 3 plus SM 6.6 for dynamic resources. Removed
unconfirmed claims: "DirectX 12 Ultimate" labelling, "ignores a mismatched version silently", and the
UMD-version query.
Method: documentation only; no commands were run.
