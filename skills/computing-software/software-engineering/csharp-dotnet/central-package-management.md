---
id: computing-software.software-engineering.csharp-dotnet.central-package-management
name: central-package-management
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, msbuild, dotnet-cli, central-package-management, nuget, directory-packages-props, transitive-pinning]
level: practitioner
status: docs-checked
description: "Manage NuGet versions centrally with Directory.Packages.props: enabling CPM, overrides, transitive pinning, package source mapping, lock files and vulnerability audit."
sources:
  - https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
  - https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping
  - https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Central package management (CPM)

**Goal:** every project in a repo uses the same version of each NuGet package, updated in one place, with transitive vulnerabilities under control.

## 1. Enable
```xml
<!-- Directory.Packages.props at repo root -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Serilog.AspNetCore" Version="9.0.0" />
    <PackageVersion Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="9.0.2" />
    <PackageVersion Include="System.Text.Json" Version="9.0.1" />   <!-- pins a transitive dependency -->
  </ItemGroup>
  <ItemGroup>
    <GlobalPackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" />  <!-- referenced by every project -->
  </ItemGroup>
</Project>
```
Projects reference without versions:
```xml
<PackageReference Include="Serilog.AspNetCore" />
```
Use `VersionOverride="8.0.0"` on a `PackageReference` for a justified exception (it can be disabled with `CentralPackageVersionOverrideEnabled=false`, after which an override errors at restore).

`dotnet new packagesprops` scaffolds the file.

## 2. Transitive pinning
With `CentralPackageTransitivePinningEnabled`, any `PackageVersion` also pins that package when it arrives transitively, the standard way to patch a vulnerable transitive dependency without waiting for the direct dependency to update.

## 3. Restore safety
```xml
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>   <!-- packages.lock.json per project -->
  <NuGetAudit>true</NuGetAudit>
  <NuGetAuditMode>all</NuGetAuditMode>          <!-- direct and transitive; defaults to all for net10.0+, otherwise direct -->
  <NuGetAuditLevel>moderate</NuGetAuditLevel>   <!-- minimum severity reported; default low -->
</PropertyGroup>
```
With the lock file enabled, NuGet writes `packages.lock.json` at the project root; CI can run `dotnet restore --locked-mode` (or set `RestoreLockedMode`) to fail when the lock file would change.
```bash
dotnet list package --vulnerable --include-transitive   # --include-transitive is not the default
```

## 4. Package source mapping (supply chain)
```xml
<!-- NuGet.config -->
<packageSourceMapping>
  <packageSource key="nuget.org"><package pattern="*" /></packageSource>
  <packageSource key="internal"><package pattern="Acme.*" /></packageSource>
</packageSourceMapping>
```
Package source mapping improves supply chain security when you mix public and private package sources.

## Gotchas
- With several `Directory.Packages.props` files, the file closest to a project is evaluated; to include a parent's settings you must import it manually.
- Dependency update bots need to be configured to edit `Directory.Packages.props`.
- `PackageVersion` entries unused by any project rot; prune periodically.

## Verify
- No `PackageReference` in any project file carries a `Version`, restore passes in CI, and `dotnet list package --vulnerable --include-transitive` is clean.

## Checked

Checked 2026-10-25 against NuGet/docs.microsoft.com-nuget (Central-Package-Management, Auditing-Packages, Package-Source-Mapping, Package-References-in-Project-Files) on main.
Confirmed: `dotnet new packagesprops`; `CentralPackageTransitivePinningEnabled`; `VersionOverride` and `CentralPackageVersionOverrideEnabled`; `GlobalPackageReference` in `Directory.Packages.props`; closest `Directory.Packages.props` wins and a parent must be imported manually; `NuGetAuditMode` default is `all` for net10.0+ otherwise `direct` (the earlier ".NET 9" default was wrong); `NuGetAuditLevel` default `low`; `RestorePackagesWithLockFile` and `packages.lock.json`; `packageSourceMapping` element.
Also confirmed: `dotnet restore --locked-mode`, `RestoreLockedMode` and `dotnet list package --vulnerable --include-transitive` (NuGet docs).
Removed as unconfirmed: NU1008, floating-version behaviour, the third-party converter tool, pinned example package versions.

Method: documentation only; no commands were run.
