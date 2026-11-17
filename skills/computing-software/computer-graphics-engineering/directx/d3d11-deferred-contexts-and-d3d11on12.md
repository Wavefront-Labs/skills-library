---
id: computing-software.computer-graphics-engineering.directx.d3d11-deferred-contexts-and-d3d11on12
name: d3d11-deferred-contexts-and-d3d11on12
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, deferred-contexts, d3d11on12, command-lists, multithreaded-rendering]
level: advanced
status: docs-checked
description: "Record D3D11 command lists on deferred contexts from worker threads, and interop D3D11 code with D3D12 via D3D11On12 wrapped resources."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-render-multi-thread-render", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-11-on-12", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-map", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-render-multi-thread-support"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 deferred contexts and D3D11On12

## 1. Deferred contexts
```cpp
ComPtr<ID3D11DeviceContext> dc;
device->CreateDeferredContext(0, &dc);
// worker thread: set full state, draw
dc->OMSetRenderTargets(1, rtv.GetAddressOf(), dsv.Get());
dc->DrawIndexed(n, 0, 0);
ComPtr<ID3D11CommandList> cl;
dc->FinishCommandList(FALSE, &cl);
// main thread
immediate->ExecuteCommandList(cl.Get(), FALSE);
```
- Deferred contexts inherit **no** state: bind everything in each list.
- Check `D3D11_FEATURE_DATA_THREADING::DriverCommandLists`. The runtime supports command lists
  regardless of the driver, but when it is FALSE the driver does not support them natively.
- `Map` on a deferred context accepts only `D3D11_MAP_WRITE_DISCARD`, `D3D11_MAP_WRITE_NO_OVERWRITE`
  or both; other map types are not supported.
- A command list is recorded on a deferred context and can only be played back on an immediate context.

## 2. When it is worth it
CPU-bound scenes with many draws per frame. Profile immediate-context submit time first, before
adding threading.

## 3. D3D11On12 interop
```cpp
D3D11On12CreateDevice(d3d12Device, flags, nullptr, 0,
    reinterpret_cast<IUnknown**>(queue.GetAddressOf()), 1, 0, &d11Dev, &d11Ctx, nullptr);
d11Dev.As(&on12);
D3D11_RESOURCE_FLAGS f{D3D11_BIND_RENDER_TARGET};
on12->CreateWrappedResource(backBuffer12, &f,
    D3D12_RESOURCE_STATE_RENDER_TARGET, D3D12_RESOURCE_STATE_PRESENT, IID_PPV_ARGS(&wrapped));
on12->AcquireWrappedResources(wrapped.GetAddressOf(), 1);
// D3D11 / Direct2D drawing into wrapped
on12->ReleaseWrappedResources(wrapped.GetAddressOf(), 1);   // transitions to OutState
d11Ctx->Flush();                                            // submits to the D3D12 queue
```
Typical use: Direct2D/DirectWrite UI over a D3D12 renderer, or porting a D3D11 subsystem gradually.

## Gotchas
- Flush the D3D11 immediate context after releasing wrapped resources, before submitting more D3D12
  work to the same queue.
- Wrapped resource InState/OutState must match what the D3D12 side expects.
- Microsoft states D3D11On12 is not optimised for performance (moderate CPU overhead, significant memory
  overhead) and recommends it for simple scenes or 2D rendering, not complicated 3D scenes.

## Verify
- [ ] Debug layers clean on both APIs; the UI overlay appears on the correct frame.
- [ ] Profiler shows deferred-context lists executing with reduced main-thread time.

## Checked

2026-10-26. Checked against Microsoft Learn: multithreading overview and support pages, ID3D11DeviceContext::Map,
FinishCommandList and the Direct3D 11 on 12 page (win32 and sdk-api repositories, commits to 2026-10). Confirmed:
D3D11On12CreateDevice arguments, wrapped-resource acquire/release then flush sequence, deferred Map restriction to
DISCARD/NO_OVERWRITE, DriverCommandLists meaning, D3D11On12 performance statement. Fixed the claim that only DISCARD
is allowed on a deferred context; removed the unconfirmed first-map-must-discard, queries-only-immediate and
batching-beats-threading statements.
Method: documentation only; no commands were run.
