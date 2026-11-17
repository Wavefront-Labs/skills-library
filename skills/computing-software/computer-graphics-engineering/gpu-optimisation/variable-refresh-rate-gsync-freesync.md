---
id: computing-software.computer-graphics-engineering.gpu-optimisation.variable-refresh-rate-gsync-freesync
name: variable-refresh-rate-gsync-freesync
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, g-sync, freesync, variable-refresh-rate, vrr, tearing, swapchain]
level: practitioner
status: docs-checked
description: "Make games behave well on VRR displays (G-Sync, FreeSync, HDMI VRR): swap chain flags, tearing support, LFC range, frame caps below refresh and fullscreen vs windowed."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/variable-refresh-rate-displays", "https://www.nvidia.com/en-us/geforce/products/g-sync-monitors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRR / G-Sync / FreeSync

## 1. What VRR does
The display waits for the next frame instead of refreshing on a fixed clock, within the range
the panel supports. Varying frame times appear smooth without tearing or vsync's quantisation to
refresh multiples.

## 2. D3D12/DXGI setup
```cpp
BOOL allowTearing = FALSE;
factory5->CheckFeatureSupport(DXGI_FEATURE_PRESENT_ALLOW_TEARING, &allowTearing, sizeof(allowTearing));
swapDesc.SwapEffect = DXGI_SWAP_EFFECT_FLIP_DISCARD;
swapDesc.Flags = allowTearing ? DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING : 0;
// present: vsync off path
swapChain->Present(0, allowTearing ? DXGI_PRESENT_ALLOW_TEARING : 0);
```
- Microsoft's VRR page: VRR displays require tearing ("vsync-off") support. `ResizeBuffers` must be passed the same `DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING` flag as at creation, and `DXGI_PRESENT_ALLOW_TEARING` is only valid with sync interval 0. Pass it whenever interval 0 is used, tearing is supported and the app is windowed (including borderless fullscreen).

## 3. Best practice
- Frame-rate caps and low-framerate behaviour are vendor-specific: check the display and driver vendor documentation.
- Keep frame pacing consistent: VRR hides variation, not hitches.

## 4. Testing
- Display OSD refresh counter or NVIDIA "G-SYNC indicator"; ensure it tracks frame rate.
- Test borderless windowed and exclusive fullscreen; multi-monitor setups with mixed refresh rates.

## Gotchas
- In-game frame limiters that sleep with coarse timers jitter; use high-resolution waitable timers.

## Verify
- [ ] Display refresh follows frame rate inside the range with no tearing.
- [ ] Frame cap keeps the game below max refresh.

## Checked
2026-11-01. Confirmed on Microsoft Learn, Variable refresh rate displays (DXGI): tearing requirement, `DXGI_FEATURE_PRESENT_ALLOW_TEARING` via `CheckFeatureSupport`, `DXGI_SWAP_CHAIN_FLAG_ALLOW_TEARING`, `DXGI_PRESENT_ALLOW_TEARING` with sync interval 0, matching `ResizeBuffers` flag. The page also confirms the `DXGI_SWAP_EFFECT_FLIP_*` requirement (Windows 10 with the Anniversary Update or KB3156421). Removed unconfirmed: example refresh range and frame times, LFC ratio, 141 fps cap, Reflex auto-cap, blt-model claim, Vulkan present-mode statement, AMD page (unreadable).
Method: documentation only; no commands were run.
