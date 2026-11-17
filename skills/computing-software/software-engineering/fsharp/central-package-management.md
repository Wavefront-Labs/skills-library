---
id: computing-software.software-engineering.fsharp.central-package-management
name: central-package-management
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, central-package-management, fsharp-project, directory-build-props, directory-packages-props]
level: advanced
status: draft
description: "Share properties and package versions across projects with Directory.Build.props and Directory.Packages.props."
sources:
  - https://learn.microsoft.com/en-us/nuget/
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared build configuration
**Goal:** configure many projects once.

`Directory.Build.props` at the repo root:
```xml
<Project>
  <PropertyGroup>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <Deterministic>true</Deterministic>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
</Project>
```
`Directory.Packages.props`:
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Expecto" Version="10.2.1" />
  </ItemGroup>
</Project>
```
Then projects use `<PackageReference Include="Expecto" />` with no version.
- MSBuild automatically imports the nearest `Directory.Build.props` upward from each project.
- Version numbers are illustrative.
- `Directory.Build.targets` runs after the project body.

## Gotchas
- With central management, a `Version` on a `PackageReference` is an error unless `VersionOverride` is used.
- Props defined in the project file override props from `Directory.Build.props` unless set conditionally.

## Self-check
Remove a version from a project's PackageReference and confirm restore still succeeds.
