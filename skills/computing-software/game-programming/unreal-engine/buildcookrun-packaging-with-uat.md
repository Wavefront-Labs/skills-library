---
id: computing-software.game-programming.unreal-engine.buildcookrun-packaging-with-uat
name: buildcookrun-packaging-with-uat
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-packaging, buildcookrun, runuat, automation-tool, cook, stage, archive, ci-build, game-programming]
level: practitioner
status: docs-checked
description: "Package Unreal projects with BuildCookRun via RunUAT: build, cook, stage and package steps, build configurations, cook methods and Project Launcher command lines, per Epic."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuildCookRun packaging with RunUAT

**Goal:** understand what BuildCookRun does and get a command line for it that matches a tested editor setup.

## What it is
- The Automation Tool (UAT) runs utility scripts for Unreal projects; packaging uses its `BuildCookRun` command, which can
  cook content, package it into a platform's native format, deploy to a device and run it where applicable.
- Stages: Build (compile executables for the platform), Cook (run the engine in a special mode to cook content), Stage
  (copy executables and content to a standalone staging directory outside the development directory), Package (platform
  distribution format), Deploy, Run.
- RunUAT files are in `Engine/Build/BatchFiles`: `RunUAT.bat` on Windows, `RunUAT.sh` on Mac/Linux. They run directly on
  the command line with valid arguments.

## Getting a command line
Page advice: hand-authoring arguments is involved and error-prone; create a Custom Launch Profile in the Project Launcher
(Platforms > Project Launcher > Add) and read the command it generates in the Output Log. Anything from `BuildCookRun`
onward can be passed straight to RunUAT. The page's example (log vs manual):
```
Automation.ParseCommandLine: Parsing Command Line: -ScriptsForProject=MyProject.uproject BuildCookRun -project=MyProject.uproject -clientconfig=Development
[UnrealEngineRoot]/Engine/Build/BatchFiles/RunUAT.bat BuildCookRun -project=MyProject.uproject -clientconfig=Development
```
`-clientconfig` is the only configuration flag shown on the pages. Flags for cook, stage, pak, archive and so on are not
listed there; take them from the generated profile output or the UAT reference.

## Build configurations (Packaging page)
| Configuration | Page description |
|---|---|
| Debug | Builds engine and project code, no optimization, all debug symbols; unsuitable for distribution |
| DebugGame | Builds project code only, no optimization, some debug info; not available for Blueprint-only projects |
| Development (default) | All but the most time-consuming optimizations, minimal debug info |
| Test | Debug tools (console commands, stats, profiling) with all optimizations; internal QA |
| Shipping | Disables console commands, stats and profiling tools; all optimizations; for distribution |

## Cooking
- Cooking converts assets to the platform format; some platforms need all content cooked before use. By the book (default)
  cooks everything ahead of time and suits performance tests and playtests. On the fly delays cooking until deployed and
  uses a Cook Server; start one with `UnrealEditor-cmd.exe <FullPathToProject.uproject> -run=cook -targetplatform=Windows
  -cookonthefly`, and give the client `-filehostip=<server IP>` (without it the build loads existing local files).
- Basic commandlet cook: `UnrealEditor.exe [GameName or .uproject] -run=cook -targetplatform=[Platform] -cookonthefly
  -map=[Map Name]`, output to `[Project]/Saved/Sandboxes/Cooked-[Platform]`.
- Cooking strips content not referenced by game levels or code. Cooked content goes in Pak files by default; Project
  Settings > Packaging also lists archive types Pak, Chunk, Utoc and Ucas.
- Deploy options in a launch profile: File Server, Copy to Device, Do Not Deploy, Copy Repository.

## Editor packaging notes (Packaging page)
- Set a Game Default Map (Project Settings > Maps & Modes) or the packaged game shows a black screen; templates set one
  automatically. Platforms menu > platform > Package Project asks for a staging directory.
- Known issue named on the Build Operations page: in UE 5.4.0 "Use Project Setting" used the configuration from editor
  startup; resolved in UE 5.4.1.
- Errors appear in the Output Log and in the Message Log under Packaging Results.
- Consoles need a source build of the engine, not the Launcher version.

## Checked
Date: 2026-11-07. Read in full: Build Operations page and Packaging Your Project page (all sections), unversioned en-us
pages whose only version statement is the UE 5.4.0/5.4.1 issue. The third source (Unreal Automation Tool Overview)
returns empty text and was dropped.
Removed as not on the pages: the whole flag table (`-build -cook -stage -pak -iostore -archive -archivedirectory -prereqs
-nodebuginfo -utf8output -unattended -nop4 -server -serverplatform -noclient -map= -compressed -distribution
-CrashReporter`), the `-skipbuild`/`-skipcook`/`-iterativecooking` options, UE5 iostore default claim, Project Settings
checkbox names, `-ini:` overrides, all CI tips (exit codes, DDC, log paths, Horde), the common-failures table, and the
Verify checklist.
Method: documentation only; no commands were run.
