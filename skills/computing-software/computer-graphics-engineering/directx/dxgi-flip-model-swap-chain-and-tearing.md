---
id: computing-software.computer-graphics-engineering.directx.dxgi-flip-model-swap-chain-and-tearing
name: dxgi-flip-model-swap-chain-and-tearing
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, swap-chain, flip-model, resizebuffers, allow-tearing, variable-refresh-rate, flip-discard, independent-flip, present]
level: practitioner
status: docs-checked
description: "Create a DXGI flip-model swap chain for D3D12/D3D11, resize it safely, and support tearing for VRR and uncapped modes with DXGI_FEATURE_PRESENT_ALLOW_TEARING."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-flip-model", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/variable-refresh-rate-displays", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/for-best-performance--use-dxgi-flip-model", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/swap-chains", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-resizebuffers", "https://github.com/GameTechDev/PresentMon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DXGI flip-model swap chains and tearing

**Goal:** a swap chain that gets independent flip (lowest latency, no compositor copy),
works with G-Sync/FreeSync, and survives resizes.

## 1. Create
```cpp
BOOL tearing = FALSE;
factory5->CheckFeatureSupport(DXGI_FEATURE_PRESENT_ALLOW_TEARING, &tearing, sizeof tearing);
DXGI_SWAP_CHAIN_DESC1 sd{};
sd.Width = w; sd.Height = h;
sd.Format = DXGI_FORMAT_R8G8B8A8_UNORM;            // documented flip-model formats: R16G16B16A16_FLOAT, B8G8R8A8_UNORM, R8G8B8A8_UNORM (+ R10G10B10A2_UNORM for HDR); no _SRGB
sd.SampleDesc = {1, 0};                             // MSAA is not supported in flip model: Count 1, Quality 0
sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
sd.BufferCount = 3;
sd.SwapEffect = DXGI_SWAP_EFFECT_FLIP_DISCARD;
sd.Flags = (tearing ? DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING : 0) | DXGI_SWAP_CHAIN_FLAG_FRAME_LATENCY_WAITABLE_OBJECT;
factory->CreateSwapChainForHwnd(commandQueue /*D3D12: the queue*/, hwnd, &sd, nullptr, nullptr, &sc1);
factory->MakeWindowAssociation(hwnd, DXGI_MWA_NO_ALT_ENTER);   // handle fullscreen yourself
```
**sRGB:** create the render target view with an `_SRGB` format on the UNORM buffer
(`rtvDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM_SRGB`) to get hardware encoding (see the back-buffer formats skill).

## 2. Present
```cpp
UINT flags = (vsyncOff && tearing && !exclusiveFullscreen) ? DXGI_PRESENT_ALLOW_TEARING : 0;
HRESULT hr = sc->Present(vsyncOff ? 0 : 1, flags);
if (hr == DXGI_ERROR_DEVICE_REMOVED || hr == DXGI_ERROR_DEVICE_RESET) handleDeviceLost();
```
- `SyncInterval 0` + `ALLOW_TEARING` = uncapped / VRR-friendly. With VRR displays, the
  monitor follows your frame rate inside its range without tearing.
- `DXGI_PRESENT_ALLOW_TEARING` can only be used with sync interval 0; Microsoft recommends passing it whenever
  sync interval is 0, tearing is supported and the app is windowed (including borderless).
- Borderless fullscreen windows can reach Independent Flip with flip model; Microsoft describes
  windowed flip as effectively equivalent or better than legacy exclusive fullscreen.

## 3. Resize
```cpp
// on WM_SIZE (non-zero size):
waitForGpuIdle();                                   // all frames using back buffers done
for (auto& bb : backBuffers) bb.Reset();            // release EVERY reference (RTVs hold none, but resources do)
sc->ResizeBuffers(0 /*keep count*/, newW, newH, DXGI_FORMAT_UNKNOWN /*keep*/, sameFlags);
for (UINT i = 0; i < 3; ++i) sc->GetBuffer(i, IID_PPV_ARGS(&backBuffers[i]));  // recreate RTVs
frameIndex = sc->GetCurrentBackBufferIndex();
```
`ResizeBuffers` fails with `DXGI_ERROR_INVALID_CALL` if any back-buffer reference is alive.
Pass the same `ALLOW_TEARING` flag to `ResizeBuffers` as at creation (documented for VRR); keep the other creation flags too.

## 4. Verify independent flip
PresentMon: `PresentMode` should read "Hardware: Independent Flip" (or "Hardware Composed:
Independent Flip" with overlays). "Composed: Flip" means DWM is compositing → extra latency;
causes include window not covering the monitor, overlapping windows, or wrong format.

## Gotchas
- Use `IDXGISwapChain3::GetCurrentBackBufferIndex()` to pick the back buffer each frame; the order of buffers from `GetBuffer` never changes.
- The buffer must be in `D3D12_RESOURCE_STATE_PRESENT` when you call `Present`, or `Present` fails with `DXGI_ERROR_INVALID_CALL`.
- Flip model needs `BufferCount` of at least 2 (2 to 16 documented); `ResizeBuffers` can pass 0 to keep the count.
- `DXGI_SWAP_EFFECT_DISCARD`/`SEQUENTIAL` (blt model) are legacy; D3D12 supports only `FLIP_SEQUENTIAL` and `FLIP_DISCARD`.

## Verify
- [ ] PresentMon shows Independent Flip in borderless fullscreen.
- [ ] Vsync-off mode tears/VRR-tracks; vsync-on caps to refresh rate.
- [ ] 100 rapid resizes: no `ResizeBuffers` failures, no leaks.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: flip-model format list, BufferCount 2-16, no MSAA, ALLOW_TEARING only with sync interval 0, same flag on ResizeBuffers, ResizeBuffers needs all back-buffer references released and accepts 0/UNKNOWN to keep count/format, D3D12 swap effects limited to the two flip effects, PRESENT-state requirement, and PresentMon PresentMode strings (Hardware: Independent Flip, Composed: Flip). Removed: claim that an sRGB swap-chain format returns a specific error, minimised-window and index-order advice that no page states.
Method: documentation only; no commands were run.
