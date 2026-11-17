---
id: computing-software.computer-graphics-engineering.directx.d3d11-device-context-and-state-objects
name: d3d11-device-context-and-state-objects
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, direct3d-11, d3d11-device-context, immediate-context, state-objects, rasterizer-state, blend-state, depth-stencil-state, d3d11-debug-layer, srv-rtv-hazard]
level: practitioner
status: docs-checked
description: "Set up a Direct3D 11 device and immediate context, cache immutable state objects, bind resources per stage, and avoid SRV/RTV hazards and state leakage between passes."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-devices-intro", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-devices-layers", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-d3d11createdevice", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createrasterizerstate", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-omsetrendertargetsandunorderedaccessviews"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 device, immediate context and state objects

**Goal:** a D3D11 renderer (still the pragmatic choice for tools, mid-size games and
interop) with explicit, cached state and no accidental leaks between passes.

## 1. Create device
```cpp
UINT flags = D3D11_CREATE_DEVICE_BGRA_SUPPORT;            // Direct2D/DirectWrite interop
#ifdef _DEBUG
flags |= D3D11_CREATE_DEVICE_DEBUG;                       // needs Graphics Tools optional feature
#endif
D3D_FEATURE_LEVEL levels[] = { D3D_FEATURE_LEVEL_11_1, D3D_FEATURE_LEVEL_11_0 };
D3D11CreateDevice(adapter, adapter ? D3D_DRIVER_TYPE_UNKNOWN : D3D_DRIVER_TYPE_HARDWARE,
                  nullptr, flags, levels, 2, D3D11_SDK_VERSION, &device, &fl, &ctx);
device.As(&device1); ctx.As(&ctx1);                       // 11.1 interfaces for CB offsets, discard views
```
With an explicit adapter pass `D3D_DRIVER_TYPE_UNKNOWN`: a non-NULL adapter with `D3D_DRIVER_TYPE_HARDWARE`
returns E_INVALIDARG.
Break on debug-layer errors: `ID3D11InfoQueue::SetBreakOnSeverity(D3D11_MESSAGE_SEVERITY_ERROR, TRUE)`.

## 2. State objects: create once, look up by description
```cpp
D3D11_RASTERIZER_DESC rd = CD3D11_RASTERIZER_DESC(CD3D11_DEFAULT{});
rd.CullMode = D3D11_CULL_NONE;
device->CreateRasterizerState(&rd, &rsNoCull);
```
Rasterizer, blend, depth-stencil and sampler states are immutable. Creating a state with the same
description as an existing one returns the same interface, and a device holds at most 4096 unique
rasterizer states (the Learn pages for the other state types give their own limits). Cache them
and never create them per frame.

## 3. Binding is per stage
`VSSetShaderResources`, `PSSetShaderResources`, `CSSetUnorderedAccessViews`,
`PSSetConstantBuffers`... A texture bound to PS is invisible to VS. Keep a table of your
own slot conventions.

## 4. The read/write hazard rule
A resource can't be bound as SRV and RTV/UAV simultaneously: the `OM*` set calls unbind
conflicting resources (SRVs, compute-shader UAVs, stream-output targets), so a shader then reads
nothing. Before rendering to a texture used as input last pass:
```cpp
ID3D11ShaderResourceView* nulls[8] = {};
ctx->PSSetShaderResources(0, 8, nulls);
ctx->OMSetRenderTargets(1, &rtv, dsv);
```

## 5. Avoid state leakage
Treat every pass as setting all state it relies on (or call `ctx->ClearState()` at frame
start in debug builds to expose leaks). Middleware (UI, video) may change state —
save/restore around it or re-apply after.

## Gotchas
- `D3D11_CREATE_DEVICE_DEBUG` fails when the SDK layers DLL is missing (on Windows 10 enable the
  "Graphics Tools" optional feature) — retry without the flag.
- Check `D3D11_FEATURE_DATA_THREADING` (`DriverCommandLists`, `DriverConcurrentCreates`) before
  relying on deferred contexts or concurrent resource creation.
- Downlevel (feature level 10_x) hardware has no pixel-shader UAVs and only restricted
  compute (see the compute-shader skill).

## Verify
- [ ] Debug layer output is empty during a full frame.
- [ ] No `Create*State` calls after load in a CPU profile.
- [ ] `ClearState()` at frame start (debug) doesn't change the rendered image.

## Checked

2026-10-26. Checked against Microsoft Learn: D3D11CreateDevice, CreateRasterizerState, OMSetRenderTargetsAndUnorderedAccessViews,
the device-layers page and the multithreading support page (win32 and sdk-api repositories, commits to 2026-10).
Confirmed: E_INVALIDARG for adapter plus HARDWARE driver type, 4096 unique rasterizer states with dedupe, Graphics
Tools optional feature for the debug layer, OM set calls unbinding conflicting views. Removed the exact debug-layer
message text and the unconfirmed deferred-context speed claim.
Method: documentation only; no commands were run.
