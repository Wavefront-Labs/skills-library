---
id: computing-software.software-engineering.desktop-ui-frameworks.maui-windows-macos-targets
name: maui-windows-macos-targets
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [maui-windows-macos-targets, maui-desktop, maui, dotnet, winui3, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Target Windows and Mac Catalyst from a .NET MAUI project and write platform-specific code with #if."
sources:
  - https://learn.microsoft.com/en-us/dotnet/maui/supported-platforms
  - https://learn.microsoft.com/en-us/dotnet/maui/mac-catalyst/cli
  - https://learn.microsoft.com/en-us/dotnet/maui/mac-catalyst/user-interface-idiom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MAUI desktop targets

**Goal:** one codebase for desktop targets.

```xml
<TargetFrameworks>net9.0-windows10.0.19041.0;net9.0-maccatalyst</TargetFrameworks>
<!-- Mac Catalyst run: dotnet build -t:Run -f net9.0-maccatalyst -->
<!-- platform code: #if WINDOWS ... #elif MACCATALYST ... #endif -->
```

**Gotcha:** macOS support is Mac Catalyst, and apps use the iPad user interface idiom by default (the UI is scaled and keeps an iPad-like look). The Mac idiom does not scale the UI and some UIKit controls (such as the stepper, picker view and refresh control) are not supported in it, so adopting it needs extra changes.

## Verify
- The app runs on both targets and window resizing works.

## Checked

2026-11-03. Confirmed in the .NET MAUI supported platforms page (Android, iOS, macOS using Mac Catalyst, Windows using WinUI 3; no Linux listed), the Mac Catalyst CLI page (`dotnet build -t:Run -f <maccatalyst TFM>`), the Mac Catalyst idiom page (iPad vs Mac idiom, unsupported controls), and the `net9.0-windows10.0.19041.0` and `net9.0-maccatalyst` target framework monikers in the docs' Notes tutorial project files. Removed: the Windows `dotnet build -t:Run` line, the Avalonia/Qt-for-Linux recommendation and the AppKit comparison, which those pages do not state.

Method: documentation only; no commands were run.
