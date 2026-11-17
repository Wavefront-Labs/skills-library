---
id: computing-software.software-engineering.desktop-ui-frameworks.winui-unpackaged-self-contained
name: winui-unpackaged-self-contained
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [winui-unpackaged-self-contained, winui-msix-packaging, winui3, windows-app-sdk, msix, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Ship a WinUI 3 app without MSIX using WindowsPackageType None and WindowsAppSDKSelfContained."
sources:
  - https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/self-contained-deploy/deploy-self-contained-apps
  - https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/deploy-unpackaged-apps
  - https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/packaging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WinUI 3 unpackaged deployment

**Goal:** classic installer deployment.

```xml
<PropertyGroup>
  <WindowsPackageType>None</WindowsPackageType>
  <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  <RuntimeIdentifier>win-x64</RuntimeIdentifier>
</PropertyGroup>
```

**Gotcha:** Unpackaged apps have no package identity, so features that require identity (the packaging overview lists notifications and background tasks among those to check) are unavailable unless you add identity with packaging with external location (sparse packages). `WindowsAppSDKSelfContained` extracts the Windows App SDK framework package into the build output; .NET apps must also be published as self-contained to be fully self-contained. Framework-dependent unpackaged apps need the bootstrapper, and `<WindowsPackageType>None</WindowsPackageType>` is the simplest way to load the runtime.

## Verify
- The exe runs on a machine without the Windows App SDK runtime installed (self-contained build).

## Checked

2026-11-03. Confirmed in the self-contained deployment page (`WindowsAppSDKSelfContained`, .NET self-contained note), the deploy-unpackaged-apps page (bootstrapper, `WindowsPackageType` None) and the packaging overview (no package identity, sparse packages). Removed: the app-data redirection claim and the explicit `RuntimeIdentifier` rationale, which those pages do not state.

Method: documentation only; no commands were run.
