---
id: computing-software.computer-graphics-engineering.directx.dxgi-debug-and-live-object-reporting
name: dxgi-debug-and-live-object-reporting
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-debugging, reportliveobjects, dxgi-debug, com-leaks]
level: practitioner
status: docs-checked
description: "Find leaked D3D12/D3D11/DXGI COM objects at shutdown with IDXGIDebug1::ReportLiveObjects, named objects and refcount discipline with ComPtr."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dxgidebug/nf-dxgidebug-idxgidebug-reportliveobjects", "https://learn.microsoft.com/en-us/windows/win32/api/dxgidebug/ne-dxgidebug-dxgi_debug_rlo_flags", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-dxgigetdebuginterface1", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/nf-d3d12sdklayers-id3d12debugdevice-reportlivedeviceobjects", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-createdxgifactory2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DXGI debug and live object reporting

Leaked COM references keep GPU memory alive, prevent device recreation after removal, and
crash on shutdown. The debug layer can list every object still alive.

## At shutdown
```cpp
// after releasing everything you own
#if defined(_DEBUG)
ComPtr<IDXGIDebug1> dxgiDebug;
if (SUCCEEDED(DXGIGetDebugInterface1(0, IID_PPV_ARGS(&dxgiDebug))))
    dxgiDebug->ReportLiveObjects(DXGI_DEBUG_ALL,
        DXGI_DEBUG_RLO_FLAGS(DXGI_DEBUG_RLO_DETAIL | DXGI_DEBUG_RLO_IGNORE_INTERNAL));
#endif
```
The report lists the live objects (with refcounts) in the debugger output window. Exact message text varies by runtime version.
`ID3D12DebugDevice::ReportLiveDeviceObjects(D3D12_RLDO_DETAIL)` gives the device's view
(call it before releasing the last device reference).

Enable DXGI's debug for factories: `CreateDXGIFactory2(DXGI_CREATE_FACTORY_DEBUG, ...)`.

## Finding the owner
- Names (`SetName`) are what make the report actionable.
- Refcount > 1 on one object but you hold one: something else (a view, a cached list, a lambda
  capture of a ComPtr) holds it. Search for copies of that ComPtr.
- Common culprits: swap chain back buffers held across `ResizeBuffers` (it cannot succeed while any direct or indirect
  reference to a back buffer remains), descriptor caches, async loader threads,
  deferred-deletion queues not flushed at shutdown.

## Discipline
- Use `Microsoft::WRL::ComPtr` everywhere; never call `AddRef/Release` manually.
- `.Get()` to pass raw pointers; `.As()` for QueryInterface; `.Reset()` to release early.
- Flush GPU (signal + wait fence) and process deferred deletions before teardown.
- Release order: resources -> heaps/PSOs/root signatures -> queues/allocators -> swap chain ->
  device -> factory, then ReportLiveObjects.

## Gotchas
- `DXGI_DEBUG_RLO_IGNORE_INTERNAL` (0x4) hides runtime-internal objects; `DXGI_DEBUG_RLO_SUMMARY` is 0x1, `DETAIL` 0x2, `ALL` 0x7. The D3D12 equivalents are `D3D12_RLDO_SUMMARY`, `DETAIL` and `IGNORE_INTERNAL`.
- Live-object reporting depends on the debug interfaces being available on the machine (the D3D12 debug layer ships as the Graphics Tools optional feature on Windows).

## Verify
- [ ] Debug build exits with no "Live ID3D12*" warnings except the expected device line; resize stress test leaks nothing.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: IDXGIDebug::ReportLiveObjects and the DXGI_DEBUG_RLO_* flag values, DXGIGetDebugInterface1, ID3D12DebugDevice::ReportLiveDeviceObjects and D3D12_RLDO_* flags, and the ResizeBuffers reference rule. Removed: the sample warning line with specific field layout and the claim about the device's own refcount line.
Method: documentation only; no commands were run.
