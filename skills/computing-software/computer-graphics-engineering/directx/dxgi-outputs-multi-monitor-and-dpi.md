---
id: computing-software.computer-graphics-engineering.directx.dxgi-outputs-multi-monitor-and-dpi
name: dxgi-outputs-multi-monitor-and-dpi
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, dxgi-output, dpi-awareness, multi-monitor, hdr-detection]
level: practitioner
status: docs-checked
description: "Enumerate DXGI outputs for multi-monitor apps: which monitor the window is on, its refresh rate, HDR capability, Per-Monitor-V2 DPI awareness and moving windows."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiadapter-enumoutputs", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_6/nf-dxgi1_6-idxgioutput6-getdesc1", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgifactory1-iscurrent", "https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DXGI outputs, multi-monitor and DPI

## Find the output the window is on
```cpp
ComPtr<IDXGIOutput6> BestOutput(IDXGIAdapter1* adapter, HWND hwnd) {
    RECT wr; GetWindowRect(hwnd, &wr);
    ComPtr<IDXGIOutput> out; ComPtr<IDXGIOutput6> best; long bestArea = -1;
    for (UINT i = 0; adapter->EnumOutputs(i, &out) != DXGI_ERROR_NOT_FOUND; ++i) {
        DXGI_OUTPUT_DESC d; out->GetDesc(&d);
        RECT is; IntersectRect(&is, &wr, &d.DesktopCoordinates);
        long area = (is.right - is.left) * (is.bottom - is.top);
        if (area > bestArea) { bestArea = area; out.As(&best); }
    }
    return best;
}
DXGI_OUTPUT_DESC1 d1; output->GetDesc1(&d1);
bool hdr = d1.ColorSpace == DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020;   // HDR mode on
float maxNits = d1.MaxLuminance;
```
Outputs are enumerated per adapter, so on multi-GPU systems enumerate all adapters' outputs to find the one under the window.
Fall back to `MonitorFromWindow` + `GetMonitorInfo` if you only need the monitor rectangle.

## Re-check on moves
Handle `WM_SIZE`/`WM_DPICHANGED` and query `IDXGIFactory1::IsCurrent()` each frame: it returns FALSE when adapters
change, and Microsoft's HDR guidance is then to re-create the factory, re-enumerate outputs by bounds and re-read `DXGI_OUTPUT_DESC1`.

## Refresh rate
`IDXGIOutput::GetDisplayModeList` lists modes; for current refresh use
`EnumDisplaySettings(monitorName, ENUM_CURRENT_SETTINGS, &dm)` -> `dm.dmDisplayFrequency`, or
DisplayConfig APIs for fractional rates (59.94).

## DPI awareness
Declare Per-Monitor V2 in the app manifest:
```xml
<dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
```
Otherwise Windows bitmap-scales your swap chain on high-DPI monitors (blurry). Then:
- Back buffer = client size in physical pixels.
- On `WM_DPICHANGED`, resize the window to the suggested rect and scale UI by
  `GetDpiForWindow(hwnd) / 96.0f`; resize buffers.

## Gotchas
- Toggling HDR on a monitor changes the output's `ColorSpace`; re-read `DXGI_OUTPUT_DESC1` when `IsCurrent` reports FALSE and switch tone mapping paths.
- Windows that span monitors cannot be DirectFlipped (the window must cover the screen); check with PresentMon.

## Verify
- [ ] Dragging the window between a 100% SDR and 150% HDR monitor updates scale, HDR mode and back buffer size with no blur.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: IDXGIOutput6::GetDesc1 fields, DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020 as the HDR-on value, IsCurrent semantics and the re-create-factory guidance, WM_SIZE guidance, DirectFlip requirement that the window cover the screen. Also confirmed in the Win32 high-DPI pages: the dpiAwareness PerMonitorV2 manifest element (Windows 10 version 1607 and later, namespace SMI/2016), WM_DPICHANGED passing a suggested RECT in lParam to apply with SetWindowPos, GetDpiForWindow with a base DPI of 96, and DEVMODE dmDisplayFrequency via EnumDisplaySettings. Removed: hybrid-laptop EnumOutputs behaviour and the Win+Alt+B shortcut.
Method: documentation only; no commands were run.
