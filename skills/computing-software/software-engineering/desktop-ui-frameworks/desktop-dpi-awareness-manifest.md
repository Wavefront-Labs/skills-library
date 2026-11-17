---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-dpi-awareness-manifest
name: desktop-dpi-awareness-manifest
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-dpi-awareness-manifest, desktop-dpi-scaling, dpi, windows, cross-platform, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Declare PerMonitorV2 awareness so windows scale crisply across monitors."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows
  - https://learn.microsoft.com/en-us/windows/win32/sbscs/application-manifests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows DPI awareness manifest

**Goal:** sharp UI on mixed-DPI setups.

```xml
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0" xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
  <asmv3:application>
    <asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">
      <dpiAwareness>PerMonitorV2, unaware</dpiAwareness>
    </asmv3:windowsSettings>
  </asmv3:application>
</assembly>
```

- `dpiAwareness` needs Windows 10 version 1607 or later; it overrides `dpiAware` there, and the first recognised item in a comma-separated list wins, so a fallback such as `unaware` can follow `PerMonitorV2`. Per-Monitor V2 itself needs Windows 10 1703 (Creators Update); `dpiAware` (`true`, `true/pm`, `per monitor`) covers older systems.
- Desktop apps are DPI unaware by default: Windows bitmap-stretches them to the display scale, which looks blurry. System awareness is crisp at only one scale factor and blurs when the DPI changes.
- Declaring Per-Monitor V2 means the app is told about DPI changes (top-level and child windows), is never bitmap-scaled, and gets automatic DPI scaling of the non-client area, `CreateDialog` dialogs and theme-drawn common-control bitmaps. The app must still resize itself on `WM_DPICHANGED`, using the suggested rectangle that message supplies. Most desktop UI frameworks (comctl32, Windows Forms, WPF) need developers to resize and reposition contents themselves; check each framework's own documentation for what it automates.
- In general the DPI awareness of a process cannot be changed after process initialization, so declare it in the manifest.

**Gotcha:** layout code that runs only at startup and cached font sizes or DPI values go stale when the DPI changes; re-evaluate them on `WM_DPICHANGED`.

## Verify
- Drag the window between monitors with different scale factors, start the app on each, and change the scale while it runs; text stays crisp and layout adapts.

## Checked

Checked 2026-11-09 against Microsoft Learn "High DPI Desktop Application Development on Windows" (read in full) and "Application manifests" (dpiAware and dpiAwareness sections).
Confirmed: every point above, including the manifest element, namespace and example.
Removed as unconfirmed: the claims that Qt 6 and Electron are automatic, and the per-framework WPF manifest instruction.

Method: documentation only; no commands were run.
