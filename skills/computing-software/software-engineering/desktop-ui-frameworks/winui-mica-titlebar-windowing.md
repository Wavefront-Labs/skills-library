---
id: computing-software.software-engineering.desktop-ui-frameworks.winui-mica-titlebar-windowing
name: winui-mica-titlebar-windowing
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [winui-mica-titlebar-windowing, winui-windows-app-sdk, winui3, windows-app-sdk, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use SystemBackdrop MicaBackdrop, ExtendsContentIntoTitleBar and AppWindow in a WinUI 3 window."
sources:
  - https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/migrate-to-windows-app-sdk/guides/windowing
  - https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/release-notes/windows-app-sdk-1-3
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WinUI 3 windowing and Mica

**Goal:** modern window chrome.

```csharp
public MainWindow() {
    InitializeComponent();
    SystemBackdrop = new MicaBackdrop();      // code-behind only
    ExtendsContentIntoTitleBar = true;
    SetTitleBar(AppTitleBar);
    AppWindow.Resize(new Windows.Graphics.SizeInt32(1200, 800));
    AppWindow.SetIcon("Assets/app.ico");
}
```

**Gotcha:** In Windows App SDK 1.3 the backdrop can be set only in code-behind: setting `<Window.SystemBackdrop>` in markup gave a compile error. With `ExtendsContentIntoTitleBar` true, the platform still draws the Minimize/Maximize/Close buttons, and only a few `AppWindowTitleBar` button/background colours support transparency.

## Verify
- The title bar drags and caption buttons stay usable.

## Checked

2026-11-03. Confirmed in the Windows App SDK windowing migration guide (`AppWindow.Resize`, `AppWindow.SetIcon`, `ExtendsContentIntoTitleBar`, caption buttons, transparency limits) and the 1.3 release notes (`SystemBackdrop = new MicaBackdrop()`, code-behind-only). `SetTitleBar` confirmed in the 1.6 release notes. Removed: the claim that Window has no DataContext or Resources, which those pages do not state.

Method: documentation only; no commands were run.
