---
id: computing-software.software-engineering.csharp-dotnet.dotnet-watch-templates-and-slnx
name: dotnet-watch-templates-and-slnx
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-sdk-cli, dotnet-watch, dotnet-new-templates, slnx-solution, hot-reload, solution-files]
level: practitioner
status: docs-checked
description: "Daily dotnet CLI tooling: dotnet watch hot reload, authoring and installing dotnet new templates, and the XML .slnx solution format (SDK 9.0.200+) with migration from .sln."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-watch", "https://learn.microsoft.com/en-us/dotnet/core/tools/custom-templates", "https://devblogs.microsoft.com/dotnet/introducing-slnx-support-dotnet-cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dotnet watch, templates and .slnx

## dotnet watch
```bash
dotnet watch run --project src/Api          # rebuild+restart on change; hot reload applies supported edits in place
dotnet watch test                           # rerun tests on save
dotnet watch --no-hot-reload run            # force restart semantics
dotnet watch --non-interactive              # no console prompts; restarts on rude edits
```
A change hot reload cannot apply is a "rude edit": `dotnet watch` asks whether to restart (Yes/No/Always/Never), and `DOTNET_WATCH_RESTART_ON_RUDE_EDIT=true` always restarts. `Ctrl+R` forces a rebuild and restart while the app is running. By default `dotnet watch` watches the `Watch` item group (the `Compile` and `EmbeddedResource` items, including referenced projects), and `.config` and `.json` files do not trigger a restart. Add files with `<Watch Include="**\*.js" />`; ignore files with `Watch="false"` on an item or project reference. Env: `DOTNET_WATCH_SUPPRESS_EMOJIS` for garbled consoles, `DOTNET_USE_POLLING_FILE_WATCHER=true` for network shares and Docker mounted volumes.

## Templates
```bash
dotnet new list                       # installed templates
dotnet new <shortName> -?               # parameters a template exposes
dotnet new install ./my-template/     # local folder that contains .template.config
dotnet new install Microsoft.TemplateEngine.Authoring.Templates   # NuGet package id
dotnet new uninstall                  # lists installed packages and the uninstall command for each
```
Authoring: a folder with `.template.config/template.json` (`shortName`, `symbols`, `sourceName`). Distribute as a NuGet package from a packaging project with `PackageType` = `Template`, `IncludeContentInPack` = `true`, `IncludeBuildOutput` = `false` and `ContentTargetFolders` = `content`; `dotnet new templatepack -n <PackageName>` (from `Microsoft.TemplateEngine.Authoring.Templates`) generates one. Test locally by installing the template folder directly.

## .slnx (dotnet CLI support from SDK 9.0.200; GA in Visual Studio 17.14)
```xml
<Solution>
  <Configurations>
    <Platform Name="Any CPU" />
    <Platform Name="x64" />
    <Platform Name="x86" />
  </Configurations>
  <Project Path="my-app/my-app.csproj" />
</Solution>
```
```bash
dotnet sln MySolution.sln migrate      # creates MySolution.slnx
dotnet sln MySolution.slnx add src/New/New.csproj   # add, list and remove work on slnx
dotnet build MySolution.slnx
```
XML-based and more concise than `.sln`; data absent from the file is part of the format's defaults. Tool support varies: the Visual Studio post says Visual Studio only loads `.slnx` when the solution file persistence setting is enabled (before 17.14 it was a preview feature), C# Dev Kit needs `dotnet.defaultSolution` set to the file, and `slngen` and Rider had no or preliminary support at the time of the post. Check your team's tools before migrating.

## Gotchas
- Running `dotnet build` and similar commands in a folder with both a `.sln` and a `.slnx` is an error: name the file explicitly.
- The post notes `dotnet nuget why` and `dotnet list package` did not work in 9.0.200 (fixed in 9.0.201); use a current SDK.

## Verify
`dotnet sln list` after migration matches the old project set and `dotnet build` of the .slnx matches the old output; edit a method body during `dotnet watch` and see it applied without restart.

## Checked
2026-11-09. Confirmed against Microsoft Learn dotnet watch and custom templates pages and the .NET Blog post Introducing support for SLNX (Chet Husk): watch options, rude edit prompt, watched files, environment variables, template package settings, `dotnet new install`/`uninstall`, SDK 9.0.200 and `dotnet sln migrate`, VS 17.14 GA, tool support notes. Removed (not stated on the pages): `--use-controllers` and `-f net9.0` example, NuGet version pin syntax, `postActions`/`constraints`/`--dry-run`, `<Watch Remove>`, .NET 10 slnx-default claim, per-project configuration and Native AOT hot reload remarks, the `<Folder>` slnx sample.
Method: documentation only; no commands were run.
