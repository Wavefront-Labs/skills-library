---
id: computing-software.software-engineering.csharp-dotnet.packing-and-publishing-nuget-packages
name: packing-and-publishing-nuget-packages
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-cli, nuget-pack, nuget, sourcelink, symbols, package-validation]
level: practitioner
status: docs-checked
description: "Produce quality NuGet packages with dotnet pack: metadata, README and icon, symbol packages, multi-targeting, package validation and trusted publishing."
sources:
  - https://learn.microsoft.com/en-us/nuget/create-packages/package-authoring-best-practices
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-pack
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/apicompat/package-validation/overview
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/apicompat/package-validation/baseline-version-validator
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/apicompat/diagnostic-ids
  - https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets
  - https://learn.microsoft.com/en-us/nuget/create-packages/symbol-packages-snupkg
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-nuget-push
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-nuget-add-source
  - https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/versioning
  - https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packing and publishing NuGet packages

**Goal:** packages that are discoverable, debuggable, compatible across versions, and published from CI without long-lived keys.

## 1. Metadata in the csproj
```xml
<PropertyGroup>
  <TargetFrameworks>net8.0;netstandard2.0</TargetFrameworks>
  <PackageId>Acme.Money</PackageId>
  <Version>2.3.0</Version>
  <Description>Money and currency types with exact arithmetic.</Description>
  <PackageReadmeFile>README.md</PackageReadmeFile>
  <PackageIcon>icon.png</PackageIcon>
  <IncludeSymbols>true</IncludeSymbols>
  <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  <EnablePackageValidation>true</EnablePackageValidation>
  <PackageValidationBaselineVersion>2.2.0</PackageValidationBaselineVersion>
</PropertyGroup>
<ItemGroup>
  <None Include="README.md" Pack="true" PackagePath="/" />
  <None Include="icon.png" Pack="true" PackagePath="/" />
</ItemGroup>
```
`PackageReadmeFile` and `PackageIcon` name a path inside the package, and the file must also be packed explicitly, as the `None ... Pack="true"` items do. The icon is limited to PNG or JPEG. Set other metadata (authors, tags, licence expression, project URL) as the msbuild-targets page lists.

## 2. Pack
```bash
dotnet pack -c Release -o artifacts
```
Open the `.nupkg` (it is a zip) and check it holds a `lib/<tfm>` folder per target framework and the README.

## 3. Compatibility
Package validation compares the package against the baseline version (`PackageValidationBaselineVersion`) and reports breaking API changes, and inconsistent APIs across target frameworks. Suppress an intentional break with a `CompatibilitySuppressions.xml` file; generate it by packing once with `/p:GenerateCompatibilitySuppressionFile=true`. After releasing the new major version, delete the suppression file and move the baseline version forward.

## 4. Publish
```bash
dotnet nuget push "artifacts/*.nupkg" --source https://api.nuget.org/v3/index.json --api-key "$NUGET_API_KEY" --skip-duplicate
```
Prefer nuget.org trusted publishing (short-lived credentials from CI such as GitHub Actions) over long-lived API keys. For private feeds, register the source with `dotnet nuget add source`.

## Gotchas
- Keep `AssemblyVersion` to the major version only (for example `2.0.0.0`); Microsoft's library guidance says this reduces binding redirects. It also advises against a fixed assembly version.
- Test both targets of a multi-targeted package.

## Verify
- A scratch console app references the packed package from a local folder feed and package validation passes in CI.

## Checked
2026-11-01. Confirmed on Microsoft Learn: msbuild-targets (`PackageIcon`, `PackageReadmeFile` must be packed
explicitly; icon JPEG or PNG), symbol-packages (`snupkg`), package validation and baseline-version pages
(`PackageValidationBaselineVersion`, `CompatibilitySuppressions.xml`, `GenerateCompatibilitySuppressionFile`),
dotnet nuget push (`--skip-duplicate`), trusted publishing, and the library versioning guidance
(`AssemblyVersion` major only). Fixed the suppression property name. Removed unconfirmed claims: SourceLink
and deterministic-build properties and the SDK 8 SourceLink note, `dotnet validate package local`,
symbol auto-push, immutable-version and prerelease advice, the key-scoping advice, PrivateAssets and
polyfill gotchas.
Method: documentation only; no commands were run.
