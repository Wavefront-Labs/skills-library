---
id: computing-software.devops-ci-cd.build-systems.dotnet-versioning-with-gitversion-and-minver
name: dotnet-versioning-with-gitversion-and-minver
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, gitversion, minver, dotnet-versioning, semver, assembly-version, nuget-versioning]
level: practitioner
status: docs-checked
description: "Derive .NET assembly and NuGet versions from git with GitVersion or MinVer: config, tag-based SemVer, AssemblyVersion vs InformationalVersion, shallow clone pitfalls."
sources: ["https://github.com/adamralph/minver", "https://gitversion.net/docs/", "https://github.com/GitTools/GitVersion/tree/main/docs/input/docs", "https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/versioning", "https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GitVersion and MinVer

Both compute a SemVer version from git history at build time, so nobody edits version numbers by hand.

## MinVer (minimal, tag-driven)
```xml
<ItemGroup>
  <PackageReference Include="MinVer" Version="x.y.z" PrivateAssets="All" />   <!-- pin the current release -->
</ItemGroup>
<PropertyGroup>
  <MinVerTagPrefix>v</MinVerTagPrefix>
  <MinVerDefaultPreReleaseIdentifiers>alpha.0</MinVerDefaultPreReleaseIdentifiers>
  <MinVerMinimumMajorMinor>2.0</MinVerMinimumMajorMinor>
</PropertyGroup>
```
- On a tag `v1.4.0`: version `1.4.0`.
- 3 commits after it: `1.4.1-alpha.0.3` (default pre-release identifiers `alpha.0` after a patch bump, with the height of 3 commits appended).
- With no version tag in history, the default version is `0.0.0-alpha.0` (plus height); `MinVerMinimumMajorMinor` raises the floor.
- Releasing = pushing a tag.
- Defaults MinVer sets: `AssemblyVersion` = `{MinVerMajor}.0.0.0`, `FileVersion` = `{MinVerMajor}.{MinVerMinor}.{MinVerPatch}.0`, `InformationalVersion` = `{MinVerVersion}`, `PackageVersion` = the version without build metadata. Build metadata is added with `MinVerBuildMetadata`.

## GitVersion (branch-aware)
```bash
dotnet tool install --global GitVersion.Tool
dotnet-gitversion          # prints the version variables as JSON (SemVer, FullSemVer, InformationalVersion, ...)
```
```yaml
# GitVersion.yml (6.x flat layout)
workflow: GitHubFlow/v1          # or GitFlow/v1, TrunkBased/preview1
branches:
  main:
    increment: Patch
```
- The current GitVersion documentation describes a v7 layout that nests settings under `calculation:` and `output:`; the `workflow` key stays at the root, and `gitversion --show-config` prints the effective settings. Check the documentation for your installed version.
- Version increments come from tags plus branch configuration and commit messages containing `+semver: major|breaking`, `+semver: minor|feature` or `+semver: patch|fix`.
- MSBuild integration via the `GitVersion.MsBuild` package (needs `dotnet msbuild`; Visual Studio's .NET Framework MSBuild is not supported), or run the tool in CI and pass the values to the build.
- More powerful, more configuration to understand; suits GitFlow-style release branches.

## CI integration
```yaml
- uses: actions/checkout@v4
  with: { fetch-depth: 0 }          # full history and tags
- run: dotnet pack -c Release -o out
```
GitHub Actions, Azure Pipelines and Travis CI use shallow clones by default, so MinVer falls back to its default version; set `fetch-depth: 0` (GitHub Actions) or `fetchDepth: 0` (Azure Pipelines checkout step). GitVersion's requirements page asks for an unshallow clone (`fetch-depth: 0`).

## Which number goes where
| Property | Use |
|---|---|
| `AssemblyVersion` | the version the CLR uses to select an assembly (strong-named assemblies on .NET Framework require exact matches), so Microsoft's guidance is to consider only the major version in it |
| `FileVersion` | Windows file properties; can include build height |
| `InformationalVersion` | human/full version, for example `1.4.1-alpha.0.3+abc123` - show in logs/about |
| `PackageVersion` | NuGet; must be unique per publish |
The .NET SDK appends the source revision to `InformationalVersion` by default (`IncludeSourceRevisionInInformationalVersion` defaults to true).

## Verify
- [ ] Building a tagged commit yields exactly the tag's version; untagged commits yield pre-release versions.
- [ ] CI checkouts fetch full history (the version is not the 0.0.0 default).

## Checked
Date: 2026-10-25. Documentation: MinVer README (adamralph/minver), GitVersion docs on the default branch (GitTools/GitVersion `docs/input/docs`: configuration, version-increments, variables, requirements, usage/msbuild, usage/cli/output), Microsoft Learn sources in dotnet/docs (`msbuild-props.md`, library versioning guidance).
Confirmed: MinVer options, `alpha.0` default identifiers, default `0.0.0-alpha.0`, height, MSBuild property defaults, shallow-clone FAQ for GitHub Actions and Azure Pipelines; GitVersion `GitVersion.Tool` and `GitVersion.MsBuild` packages, `workflow: GitHubFlow/v1`, `branches.main.increment`, `+semver:` keywords, JSON default output, unshallow requirement; `IncludeSourceRevisionInInformationalVersion` default true; AssemblyVersion guidance.
Removed: the pinned MinVer package version, the `NuGetVersionV2` variable (not in the current variable list), the `release: { label: rc }` and `ignore` example entries, `/p:Version=$(GitVersion.SemVer)` and `/output json` flag spellings (command-line syntax differs between GitVersion versions), the Azure `fetchTags` setting and the exact MinVer failure version for shallow clones.
Note: the GitVersion documentation on the default branch documents the v7 configuration layout while the flat 6.x layout is shown above; verify against the installed version.
Method: documentation only; no commands were run.
