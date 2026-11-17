---
id: computing-software.software-engineering.fsharp.nuget-packaging
name: nuget-packaging
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, nuget-packaging, fsharp-nuget, dotnet-pack, sourcelink]
level: practitioner
status: draft
description: "Build and publish an F# library as a NuGet package with metadata, symbols and SourceLink."
sources:
  - https://learn.microsoft.com/en-us/nuget/
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NuGet packaging
**Goal:** ship a library.

```xml
<PropertyGroup>
  <PackageId>My.Lib</PackageId>
  <Version>1.0.0</Version>
  <Authors>me</Authors>
  <Description>Short description</Description>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <PackageReadmeFile>README.md</PackageReadmeFile>
  <RepositoryUrl>https://github.com/org/repo</RepositoryUrl>
  <PublishRepositoryUrl>true</PublishRepositoryUrl>
  <EmbedUntrackedSources>true</EmbedUntrackedSources>
  <IncludeSymbols>true</IncludeSymbols>
  <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  <ContinuousIntegrationBuild Condition="'$(CI)' == 'true'">true</ContinuousIntegrationBuild>
</PropertyGroup>
```
```bash
dotnet pack -c Release -o nupkg
dotnet nuget push "nupkg/*.nupkg" --api-key $NUGET_API_KEY --source https://api.nuget.org/v3/index.json
```
- SourceLink is built into the .NET SDK for GitHub-hosted repos (SDK 8+); earlier SDKs add `Microsoft.SourceLink.GitHub` package (unconfirmed exact cutoff).
- Never put the API key in the repo; pass from CI secrets.
- Follow SemVer; prerelease via `-beta.1`.

## Gotchas
- Packages push permanently; unlisting does not delete.
- Missing README or licence yields NuGet warnings.

## Self-check
`dotnet pack` then unzip the .nupkg and check the nuspec metadata.
