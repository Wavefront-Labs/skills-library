---
id: computing-software.computer-graphics-engineering.directx.dxgi-composition-swap-chains
name: dxgi-composition-swap-chains
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, directcomposition, composition-swapchain, transparent-window, swapchainpanel]
level: advanced
status: docs-checked
description: "Create composition swap chains for DirectComposition, WinUI SwapChainPanel and per-pixel transparent windows: CreateSwapChainForComposition, alpha mode, scaling."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_2/nf-dxgi1_2-idxgifactory2-createswapchainforcomposition", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-idxgiswapchain2-setmatrixtransform", "https://learn.microsoft.com/en-us/windows/win32/api/dcomp/nf-dcomp-dcompositioncreatedevice", "https://learn.microsoft.com/en-us/windows/win32/api/dcomp/nf-dcomp-idcompositiondevice-createtargetforhwnd", "https://learn.microsoft.com/en-us/windows/win32/winmsg/extended-window-styles", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_2/ne-dxgi1_2-dxgi_alpha_mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composition swap chains

`CreateSwapChainForHwnd` binds a swap chain to a window. `CreateSwapChainForComposition`
creates one with no window; you attach it to a visual tree such as DirectComposition visuals or a XAML
swap-chain panel. Used for per-pixel transparent overlays and embedding 3D views in XAML UIs.

## Create
```cpp
DXGI_SWAP_CHAIN_DESC1 sd = {};
sd.Width = w; sd.Height = h;                              // explicit: no window to infer from
sd.Format = DXGI_FORMAT_B8G8R8A8_UNORM;
sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT; sd.BufferCount = 2; sd.SampleDesc.Count = 1;   // flip model: 2..16 buffers, no MSAA
sd.SwapEffect = DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL;         // required: composition supports only flip model, FLIP_SEQUENTIAL
sd.AlphaMode = DXGI_ALPHA_MODE_PREMULTIPLIED;             // transparency; DXGI_ALPHA_MODE_IGNORE for opaque
sd.Scaling = DXGI_SCALING_STRETCH;                        // required for composition swap chains
ComPtr<IDXGISwapChain1> sc;
factory->CreateSwapChainForComposition(commandQueue.Get(), &sd, nullptr, &sc);
```

## Transparent window with DirectComposition
```cpp
ComPtr<IDCompositionDevice> dcomp; DCompositionCreateDevice(dxgiDevice.Get() /* the DXGI device used to create DirectComposition surfaces */, IID_PPV_ARGS(&dcomp));
ComPtr<IDCompositionTarget> target; dcomp->CreateTargetForHwnd(hwnd, TRUE, &target);
ComPtr<IDCompositionVisual> visual; dcomp->CreateVisual(&visual);
visual->SetContent(sc.Get()); target->SetRoot(visual.Get()); dcomp->Commit();
```
Window: `WS_EX_NOREDIRECTIONBITMAP` (no GDI surface behind it). Render **premultiplied** alpha
(colour already multiplied by alpha); clear to (0,0,0,0) for fully transparent areas.

## XAML swap-chain panel
UWP XAML panels attach through `ISwapChainPanelNative::SetSwapChain` (`windows.ui.xaml.media.dxinterop.h`).
To scale a composition swap chain, `IDXGISwapChain2::SetMatrixTransform` accepts only scale and translation
and works only on swap chains made by `CreateSwapChainForComposition`; size the back buffer explicitly.
For WinUI 3 panels use the interop header and docs that ship with the Windows App SDK (not checked here).

## Gotchas
- `ResizeBuffers` cannot take width or height 0 on a composition swap chain (there is no window client area to infer from); pass explicit sizes.
- Premultiplied means each colour channel is already scaled by alpha; a channel greater than alpha blends additively.
- Check the presentation path with PresentMon rather than assuming composition swap chains get Independent Flip.

## Verify
- [ ] Transparent overlay shows desktop through unpainted pixels with clean anti-aliased edges (no dark halos = premultiplied correctly).

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: CreateSwapChainForComposition requires FLIP_SEQUENTIAL and DXGI_SCALING_STRETCH, ResizeBuffers rejects 0 sizes on composition swap chains, SetMatrixTransform is composition-only and scale/translate-only, DXGI_ALPHA_MODE_PREMULTIPLIED semantics, DCompositionCreateDevice and CreateTargetForHwnd signatures, WS_EX_NOREDIRECTIONBITMAP exists in the extended window styles page, ISwapChainPanelNative::SetSwapChain exists for UWP XAML. Removed: WinUI 3 panel code and CompositionScaleChanged advice, the claim that HWND swap chains ignore alpha, and DirectFlip/latency claims for overlays.
Method: documentation only; no commands were run.
