---
id: computing-software.software-engineering.csharp-dotnet.directory-build-props-and-shared-build-settings
name: directory-build-props-and-shared-build-settings
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, msbuild, dotnet-cli, directory-build-props, directory-build-targets, build-settings]
level: practitioner
status: docs-checked
description: "Share build settings across .NET projects with Directory.Build.props/.targets: target frameworks, warnings, analyzers, versioning, deterministic CI builds and debugging MSBuild."
sources:
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory
  - https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props
  - https://learn.microsoft.com/en-us/dotnet/core/sdk/artifacts-output
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory.Build.props and shared build settings

**Goal:** one place for settings every project in a repo shares, so csproj files only contain what is unique.

## 1. How discovery works
MSBuild walks up from each project's directory and stops at the **first** `Directory.Build.props` it finds, which is imported early (`Microsoft.Common.props`); `Directory.Build.targets` is imported late. To merge a nested file with its parent, import the parent explicitly:
```xml
<Import Project="$([MSBuild]::GetPathOfFileAbove('Directory.Build.props', '$(MSBuildThisFileDirectory)../'))" />
```

## 2. A typical root Directory.Build.props
```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <Company>Acme</Company>
    <ContinuousIntegrationBuild Condition="'$(CI)' == 'true'">true</ContinuousIntegrationBuild>
    <ArtifactsPath>$(MSBuildThisFileDirectory)artifacts</ArtifactsPath>   <!-- .NET 8+ unified output location -->
  </PropertyGroup>
</Project>
```
Set `ContinuousIntegrationBuild` from your CI system's variable, as the SDK docs describe.

## 3. props vs targets
- `.props`: defaults and items that projects may override (they are imported before the project body).
- `.targets`: logic that must see final property values (after the project), custom targets like `<Target Name="StampVersion" BeforeTargets="Build">`.
A property set in `.props` can be overridden by the project file; to override everything set earlier, set it in the project after the final import (or in `Directory.Build.targets`).

## 4. Other repo-level files
- `Directory.Packages.props`: central package versions (CPM).
- `global.json`: SDK version.
- `.editorconfig`: analyzer severities and code style.
- `NuGet.config`: package sources and source mapping.
- `Directory.Solution.props` / `Directory.Solution.targets`: properties and targets for solution builds.

## 5. Debugging MSBuild
```bash
dotnet msbuild -getProperty:TargetFramework -getProperty:Version src/Api
dotnet msbuild -pp:out.xml src/Api/Api.csproj   # fully preprocessed project with all imports
```

## Gotchas
- A stray `Directory.Build.props` in a parent folder is imported unexpectedly because the walk stops at the first file found; put one at the repo root to control the walk.
- `TreatWarningsAsErrors` at the root plus a new SDK with new warnings can break builds on upgrade; pin the SDK with global.json.

## Verify
- `dotnet msbuild -getProperty:Nullable` returns `enable` for every project, and csproj files contain no duplicated settings.

## Checked

Checked 2026-10-25 against MicrosoftDocs/visualstudio-docs (customize-by-directory, msbuild-command-line-reference) and dotnet/docs (core/project-sdk/msbuild-props, core/sdk/artifacts-output, fundamentals/code-analysis/overview) on main.
Confirmed: the upward walk stops at the first `Directory.Build.props`; the `GetPathOfFileAbove` import pattern; `Directory.Solution.props`/`.targets`; `ContinuousIntegrationBuild`; `ArtifactsPath` and the unified output layout in .NET 8 and later; `AnalysisLevel` as a compound value; `-getProperty` and `-preprocess`.
Removed as unconfirmed: `EnforceCodeStyleInBuild`, documentation-file and `NoWarn` defaults, the SourceLink package reference, test-project name condition, the claim that `.props` values for `Output*` paths have no effect, binlog viewer advice, incremental-build invalidation claim.

Method: documentation only; no commands were run.
