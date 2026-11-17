---
id: computing-software.software-engineering.desktop-ui-frameworks.winui-msix-packaged-app
name: winui-msix-packaged-app
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [winui-msix-packaged-app, winui-msix-packaging, winui3, windows-app-sdk, msix, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Build a packaged WinUI 3 MSIX with MSBuild GenerateAppxPackageOnBuild and sign it with a certificate."
sources:
  - https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/ci-for-winui3
  - https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WinUI 3 MSIX packaged app

**Goal:** a signed MSIX that installs cleanly.

```powershell
# command-line MSBuild arguments that generate the MSIX
msbuild App.sln /p:Configuration=Release /p:Platform=x64 `
  /p:AppxPackageDir="Packages" /p:UapAppxPackageBuildMode=SideloadOnly `
  /p:AppxBundle=Never /p:GenerateAppxPackageOnBuild=true
# or in Visual Studio: right-click the project > Package and Publish > Create App Packages
```

**Gotcha:** MSIX apps must be signed to install. A test certificate can be created in the Create App Packages wizard (choose the publisher name on the signing page), which adds a .pfx to the project. `dotnet publish` produces a folder or EXE, not an MSIX.

## Verify
- The MSIX is produced under the Packages folder, is signed, and installs and launches.

## Checked

2026-11-03. Confirmed in the WinUI 3 CI page (MSBuild arguments including `GenerateAppxPackageOnBuild`, MSIX must be signed, Package and Publish > Create App Packages, creating a .pfx test certificate) and the code signing options page (SignTool for signing MSIX). Fixed an error: the draft built the MSIX with `dotnet publish`, which the docs describe as producing a self-contained folder or EXE. Removed: makeappx and Add-AppxPackage commands, the signtool arguments, and the 0x800B0109 error code marked "confirm", none of which those pages cover.

Method: documentation only; no commands were run.
