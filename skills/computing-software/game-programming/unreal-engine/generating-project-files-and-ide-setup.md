---
id: computing-software.game-programming.unreal-engine.generating-project-files-and-ide-setup
name: generating-project-files-and-ide-setup
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, generate-project-files, unrealbuildtool, visual-studio, ide-setup, game-programming]
level: practitioner
status: docs-checked
description: "Generate Unreal project files with GenerateProjectFiles.bat and UBT, know when to regenerate, and set up Visual Studio workloads and components for Unreal C++ projects."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-generate-unreal-engine-project-files-for-your-ide", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-build-tool-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating project files and IDE setup

**Goal:** a working Visual Studio solution for Unreal C++ with IntelliSense and builds.

## Generate (source-built engine)
The Project Files for IDEs page is for engine source downloaded from GitHub: run `GenerateProjectFiles.bat` in the
engine root. It analyses module and target build files and, for Visual Studio, writes `UE5.sln` in the root; project
files go to `Engine/Intermediate/ProjectFiles/`. The page recommends the Development configuration on Win64 for the
first compile. The script is a wrapper that launches UnrealBuildTool with `-ProjectFiles`.
Optional arguments from the page:
| Option | Effect |
|---|---|
| `-CurrentPlatform` | only the current desktop platform (lighter files); default is every platform with an SDK detected |
| `-2022` | generate VS 2022 format and use the VS 2022 compiler |
| `-ThirdParty` | add third-party headers/files (slower project load) |
| `<Project>.uproject -Game` | only that project's code and content, e.g. `GenerateProjectFiles.bat ShooterGame.uproject -Game` |
| `-NoIntelliSense` | skip IntelliSense data |
| `-AllLanguages` / `-OnlyPublic` / `-NoShippingConfigs` | all-language docs / only public engine headers / drop Shipping and Test configs |
| `-Platforms=PLATFORM_1+PLATFORM_2` | explicit platforms (solution name gets a platform suffix) |
Typically these options are not required.

## When to regenerate
Re-run after syncing new code from source control and after adding or removing source files; do not hand-edit
project files. UBT itself does not need project files: it finds sources through module and target build files, so a
new source file may compile before the project files are refreshed. Project files are not checked in to source
control. The `Intermediate/ProjectFiles` files are safe to delete and regenerate, but you may lose project-specific
preferences such as command-line argument strings.
The UnrealVS extension has a toolbar button for regenerating (shortcut command `UnrealVS.RefreshProjects`); it only
works once a solution is loaded, so run `GenerateProjectFiles.bat` first if there is no `UE5.sln`.

## Visual Studio setup (Setting Up Visual Studio page)
- Workloads: under Desktop & Mobile enable .NET desktop development, Desktop development with C++, and .NET
  Multi-platform App UI development; under Gaming enable Game development with C++.
- Components under Game development with C++: C++ profiling tools, C++ AddressSanitizer, Windows 10 or 11 SDK
  (10.0.18362 or newer), Unreal Engine installer.
- A first Unreal C++ project may show a missing-components warning in Solution Explorer: click Install.
- If Unreal was synced from Perforce, run the Prerequisite Installer from `[UNREAL_ENGINE_ROOT]\Engine\Extras\Redist\en-us\`.
- The page has a version table of supported Visual Studio versions per engine release (5.1 to 5.8) and MSVC, Windows
  SDK, LLVM and .NET minimums; consult it for your engine version rather than relying on this skill.
- Optional: turn off Tools > Options > Projects and Solutions > Always show Error List if build finished with errors,
  because it can show downstream errors; use the Output Log for the root cause.

## Verify
- [ ] After regenerating, the solution opens, builds in the configuration you chose and lists the expected modules.

## Checked
Date: 2026-11-07.
Read in full: Setting Up Visual Studio (Version Compatibility, installer options, Recommended Settings), Project Files
for IDEs (all sections) and UnrealBuildTool (overview and topic list). dev.epicgames.com; the VS table on the first
page reflects the latest engine versions listed there, so check it for older releases.
Removed as unconfirmed: right-click uproject and Editor menu refresh paths, the `Build.bat -projectfiles` and `-rocket`
/ `-vscode` / `-rider` command lines, Rider and VS Code claims, "IDE support for Unreal Engine" and natvis claims,
build-configuration descriptions, branch-switch and Live Coding gotchas, and the F5 Verify step.
Method: documentation only; no commands were run.
