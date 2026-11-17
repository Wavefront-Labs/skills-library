---
id: computing-software.computer-graphics-engineering.directx.dxgi-frame-latency-waitable-swap-chain
name: dxgi-frame-latency-waitable-swap-chain
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, swap-chain, frame-latency-waitable, setmaximumframelatency, input-latency, presentmon, frame-pacing]
level: advanced
status: docs-checked
description: "Cut input latency in D3D12/D3D11 with a frame-latency waitable swap chain: wait before sampling input, set maximum frame latency, and measure with PresentMon."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-idxgiswapchain2-setmaximumframelatency", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_3/nf-dxgi1_3-idxgiswapchain2-getframelatencywaitableobject", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/for-best-performance--use-dxgi-flip-model", "https://github.com/GameTechDev/PresentMon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DXGI frame-latency waitable swap chain

**Goal:** the CPU starts a frame only when the swap chain can accept it, so input is
sampled as late as possible and the present queue never fills up with stale frames.

## 1. Enable
Create the swap chain with `DXGI_SWAP_CHAIN_FLAG_FRAME_LATENCY_WAITABLE_OBJECT`, then:
```cpp
ComPtr<IDXGISwapChain2> sc2; sc1.As(&sc2);
sc2->SetMaximumFrameLatency(1);                         // documented default is 1; larger values queue more frames
HANDLE waitable = sc2->GetFrameLatencyWaitableObject(); // auto-reset event
```
`SetMaximumFrameLatency` on the swap chain is valid only for swap chains created with this flag (otherwise `DXGI_ERROR_INVALID_CALL`).

## 2. Frame loop order
```cpp
while (running) {
    WaitForSingleObjectEx(waitable, 1000, TRUE);   // 1. block until a present slot frees
    pumpMessages(); sampleInput();                  // 2. input as late as possible
    simulate();
    waitForFrameFence(frameIndex);                  // 3. per-frame resource reuse (D3D12 fence)
    recordAndSubmit();
    sc->Present(syncInterval, flags);
}
```
Waiting *before* input is the whole point; waiting right before `Present` gains nothing.
Wait on the handle before every frame, including the first one the app renders with the swap chain. Close it with `CloseHandle` when done.

## 3. Choosing the latency value
`MaxLatency` is the number of back-buffer frames the swap chain may queue (documented default 1). Lower values
reduce queued frames at the cost of CPU/GPU overlap; measure before choosing. Expose it as a setting if useful.
Microsoft notes Independent Flip with the waitable object can reach one frame of latency on recent Windows 10 builds.

## 4. Measure
PresentMon columns: `MsBetweenPresents`, `MsUntilDisplayed`, `DisplayLatency`, `MsPCLatency` (2.x metrics),
or click-to-photon hardware. Compare before/after at the same frame rate.

## Gotchas
- Forgetting to wait on the object each frame removes the latency benefit.
- Combining this with a separate D3D12 frames-in-flight fence scheme can reintroduce queuing; keep per-frame resource count consistent with the latency value you set.
- `ALLOW_TEARING` can give lower latency than the waitable object on systems with multi-plane overlay support (Microsoft's flip-model page).

## Verify
- [ ] PresentMon shows lower display latency with no drop in average FPS (GPU-bound case).
- [ ] CPU timeline: wait occurs before input sampling each frame.
- [ ] No 1000 ms timeouts during normal play (would indicate a broken present loop).

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: waitable flag requirement and DXGI_ERROR_INVALID_CALL otherwise, SetMaximumFrameLatency default of 1, wait before every frame including the first, CloseHandle, PresentMon column names and 2.x flags. Removed: the claim that IDXGIDevice1 latency is ignored, the 'DXGI default 3' table, hardware vendor SDK advice and the 1000 ms timeout value as a recommendation.
Method: documentation only; no commands were run.
