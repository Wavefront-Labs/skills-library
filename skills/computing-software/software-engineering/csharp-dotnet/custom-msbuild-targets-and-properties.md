---
id: computing-software.software-engineering.csharp-dotnet.custom-msbuild-targets-and-properties
name: custom-msbuild-targets-and-properties
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, msbuild-targets, msbuild-properties, beforetargets, incremental-build, msbuild, directory-build-targets, msbuild-itemgroups]
level: advanced
status: docs-checked
description: "Extend .NET builds with MSBuild: properties vs items, targets hooked with BeforeTargets/AfterTargets, Inputs/Outputs for incremental builds, and evaluation order."
sources:
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-targets
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/incremental-builds
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom MSBuild targets and properties

**Goal:** add build steps (codegen, asset copying, version stamping) that run at the
right time, only when needed, and work in `dotnet build` and the IDE.

## Model
- **Properties** (`<PropertyGroup><Foo>bar</Foo>`): scalar, `$(Foo)`. Last definition wins.
- **Items** (`<ItemGroup><Schema Include="schemas/*.json" /></ItemGroup>`): lists with metadata,
  `@(Schema)`, `%(Schema.Filename)`.
- **Evaluation** (all properties, then items, from top to bottom, imports included) happens
  before **execution** of targets. Properties set inside targets apply only from then on.

## A custom target
```xml
<Target Name="GenerateApiClient"
        BeforeTargets="CoreCompile"
        Inputs="@(OpenApiSpec)"
        Outputs="$(IntermediateOutputPath)ApiClient.g.cs">
  <Exec Command="dotnet tool run my-codegen --input &quot;@(OpenApiSpec)&quot; --output &quot;$(IntermediateOutputPath)ApiClient.g.cs&quot;" />
  <ItemGroup>
    <Compile Include="$(IntermediateOutputPath)ApiClient.g.cs" />
  </ItemGroup>
</Target>
<ItemGroup><OpenApiSpec Include="api/billing.json" /></ItemGroup>
```
- `Inputs`/`Outputs` make it incremental: skipped when outputs are newer than inputs.
- Hook with `BeforeTargets`/`AfterTargets` on well-known targets (`CoreCompile`, `Build`,
  `Publish`, `Pack`) rather than overriding SDK targets.

## Where to put it
- Single project: in the `.csproj`.
- Shared: `Directory.Build.props` (imported early, for defaults) vs `Directory.Build.targets` (imported late, so it can see the project's final properties).

## Useful built-ins
`<Message Importance="high" Text="..." />`, `<Error Condition="..." Text="..." />`,
`<Copy SourceFiles="@(X)" DestinationFolder="$(OutDir)" SkipUnchangedFiles="true" />`,
`<WriteLinesToFile>`, `<MakeDir>`, conditions `Condition="'$(Configuration)' == 'Release'"`,
property functions `$([System.DateTime]::UtcNow.ToString(yyyyMMdd))`.

## Debugging
```bash
dotnet msbuild -preprocess:full.xml       # fully expanded project with all imports
dotnet msbuild -getProperty:TargetPath -getItem:Compile   # evaluate and print properties/items without building
```

## Gotchas
- Quote paths in `Exec`.
- Targets without Inputs/Outputs run on every build, slowing inner loops.

## Verify
- [ ] Second `dotnet build` with no changes skips the target because its outputs are up to date (see the detailed build log).

## Checked

Checked 2026-10-25 against MicrosoftDocs/visualstudio-docs (msbuild-targets, incremental-builds, customize-by-directory, msbuild-command-line-reference) on main.
Confirmed: `BeforeTargets`/`AfterTargets`; `Inputs`/`Outputs` incremental behaviour (targets with up-to-date outputs are not executed); Directory.Build.props/targets import roles; `-preprocess` (`-pp`), `-getProperty` and `-getItem` evaluate without building.
Removed as unconfirmed: the NSwag command line (replaced with a placeholder tool name), `FileWrites` clean behaviour, `build/<PackageId>.targets`, the design-time build condition, the .NET 8 label on `-getProperty`, binlog viewer advice.

Method: documentation only; no commands were run.
