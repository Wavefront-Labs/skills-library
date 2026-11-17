---
id: computing-software.computer-graphics-engineering.directx.dxgi-fullscreen-modes-and-alt-enter
name: dxgi-fullscreen-modes-and-alt-enter
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, borderless-fullscreen, alt-enter, makewindowassociation]
level: practitioner
status: docs-checked
description: "Implement fullscreen for D3D12/DXGI flip-model apps: borderless windowed fullscreen, handling Alt+Enter yourself, and when exclusive mode still matters."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/swap-chains", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/for-best-performance--use-dxgi-flip-model", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgifactory-makewindowassociation", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-setfullscreenstate", "https://devblogs.microsoft.com/directx/demystifying-full-screen-optimizations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fullscreen modes and Alt+Enter

## Prefer borderless windowed fullscreen
With flip-model swap chains, a window whose client area covers the screen can reach **DirectFlip / Independent Flip**
(buffers matching the screen size, or within a hardware scaling range): Microsoft describes this as efficient as fullscreen exclusive,
with faster Alt-Tab and better integration with display features. D3D12 does not support full-screen exclusive mode: when
the game is the only visible app the OS applies full-screen optimisations, and `SetFullscreenState` in D3D12 only changes
resolution and refresh rate (and `ResizeBuffers` must follow it).

```cpp
void SetBorderlessFullscreen(HWND hwnd, bool on) {
    static RECT saved; static LONG savedStyle;
    if (on) {
        savedStyle = GetWindowLong(hwnd, GWL_STYLE); GetWindowRect(hwnd, &saved);
        MONITORINFO mi = { sizeof(mi) };
        GetMonitorInfo(MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST), &mi);
        SetWindowLong(hwnd, GWL_STYLE, savedStyle & ~(WS_CAPTION | WS_THICKFRAME | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX));
        SetWindowPos(hwnd, HWND_TOP, mi.rcMonitor.left, mi.rcMonitor.top,
                     mi.rcMonitor.right - mi.rcMonitor.left, mi.rcMonitor.bottom - mi.rcMonitor.top,
                     SWP_FRAMECHANGED | SWP_NOOWNERZORDER);
    } else {
        SetWindowLong(hwnd, GWL_STYLE, savedStyle);
        SetWindowPos(hwnd, nullptr, saved.left, saved.top, saved.right - saved.left, saved.bottom - saved.top,
                     SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOOWNERZORDER);
    }
}
```
Handle `WM_SIZE` -> `ResizeBuffers` with the new client size.

## Alt+Enter
DXGI's default Alt+Enter handler toggles DXGI fullscreen state, which fights your borderless
logic. Disable and handle it:
```cpp
factory->MakeWindowAssociation(hwnd, DXGI_MWA_NO_ALT_ENTER);
// WM_SYSKEYDOWN with VK_RETURN and (lParam & (1<<29)) -> toggle borderless
```
`MakeWindowAssociation` must be called on the factory associated with the target swap chain; the docs suggest
`IDXGIObject::GetParent` on the swap chain to find it. `DXGI_MWA_NO_ALT_ENTER` blocks the Alt+Enter handling; `NO_WINDOW_CHANGES` stops DXGI monitoring the message queue.

## When exclusive-style mode changes matter
- Changing display resolution/refresh rate (e.g. 1080p on a 4K panel for performance): prefer
  rendering at lower internal resolution and upscaling instead of a mode change.
- Legacy D3D11 apps: `SetFullscreenState(TRUE)` + `ResizeTarget` with a supported mode from
  `IDXGIOutput::GetDisplayModeList`.

## Gotchas
- DirectFlip needs the window client region to cover the screen; check with PresentMon whether you get `Hardware: Independent Flip` or `Composed: Flip`.
- Other desktop content on top can force composition; verify with PresentMon.
- Multi-monitor: use the monitor the window is on, not the primary.

## Verify
- [ ] PresentMon reports `PresentMode = Hardware: Independent Flip` in fullscreen; Alt+Enter toggles your mode without DXGI errors.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: D3D12 has no full-screen exclusive mode and SetFullscreenState only changes mode, ResizeBuffers is required after the transition, DirectFlip scenarios and their conditions, MakeWindowAssociation factory rule and DXGI_MWA_* flags, PresentMon PresentMode strings. Removed: specific overlay product names and the exact-1-pixel-gap claim, which the pages do not state.
Method: documentation only; no commands were run.
