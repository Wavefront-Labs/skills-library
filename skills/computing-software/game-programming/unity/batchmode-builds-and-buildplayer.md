---
id: computing-software.game-programming.unity.batchmode-builds-and-buildplayer
name: batchmode-builds-and-buildplayer
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, batchmode, buildplayer, ci-builds, build-profiles, command-line, game-programming]
level: practitioner
status: docs-checked
description: "Script headless Unity builds: -batchmode and -executeMethod, -quit and exit codes, -buildTarget, -logFile, build profiles, BuildPipeline.BuildPlayer overloads and caveats."
sources: ["https://docs.unity3d.com/Manual/EditorCommandLineArguments.html", "https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildPlayer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batchmode builds and BuildPipeline.BuildPlayer

**Goal:** run a Unity build from the command line and fail the process on error.

## Command line behaviour (Editor command line arguments page)
- `-batchmode`: runs command line arguments without human interaction and suppresses dialogs. On a script
  exception, failed Asset server update or other failed operation Unity exits immediately with return
  code 1. Console output is minimal (log files still hold the full log). Only one Unity instance can
  open a project at a time. If the project has not yet been imported, the target platform is the default;
  force another with `-buildTarget`. `Application.isBatchMode` detects it.
- `-executeMethod <ClassName.MethodName>` (or with a namespace): runs a static method once the project
  opens. To return an error, throw an exception (exit code 1) or call `EditorApplication.Exit` with a
  non-zero code. Pass parameters on the command line and read them with
  `System.Environment.GetCommandLineArgs`. The script must be in an Editor folder; the method must be
  static. If `-activeBuildProfile` is also given, Unity compiles with the profile's scripting defines
  first (added to existing defines).
- `-quit`: quits after other commands finish; can hide some error messages (they remain in the Editor
  log). It quits `-runTests` immediately and can hang when asynchronous code is running.
  `-quitTimeout` sets the wait for pending async tasks (default 300 seconds).
- `-projectPath <pathname>`: absolute or relative; quote if it has spaces.
- `-logFile <pathname>`: Editor log location; `-` writes to the console. On Windows, `-logFile` can
  direct output to stdout.
- `-nographics` (batch mode): no graphics device, for machines without a GPU; cannot bake GI; output logs
  are off unless `-logFile` is given.
- `-buildTarget <name>`: options include android, ios, linux64, osxuniversal, tvos, visionos,
  windowsstoreapps, webgl, win, win64, cloudrendering.
- Build arguments: `-activeBuildProfile <path relative to project root>`, `-build <path>` (builds a
  Player from the active build profile; some platforms need an extension), and
  `-buildWindows64Player`, `-buildLinux64Player`, `-buildOSXUniversalPlayer` and others.
- Licence arguments: `-serial` (requires `-batchmode`; `-quit` is good practice), `-returnlicense` (not
  for floating licences), `-createManualActivationFile`, `-manualLicenseFile`.

Example shape:
`Unity -batchmode -quit -projectPath <path> -buildTarget win64 -executeMethod MyBuilder.Build -logFile -`

## BuildPipeline.BuildPlayer
- Overloads: `BuildPlayer(BuildPlayerOptions)`, `BuildPlayer(BuildPlayerWithProfileOptions)` (applies the
  settings of the given build profile; use it when working with a `BuildProfile`), and older
  `levels, locationPathName, target, options` overloads that are still supported but will be replaced.
  All return a `BuildReport`.
- Page example fields: `scenes`, `locationPathName`, `target`, `options` (`BuildOptions.None`);
  profile version uses `buildProfile`, `locationPathName`, `options`. Check
  `report.summary.result` against `BuildResult.Succeeded` / `Failed`; `summary.totalSize` is available.
- If `levels` is empty, the build includes only the current open scene.
- Calling it invalidates editor-script variables referencing GameObjects; reacquire them.
- Scripting symbol changes (for example `SetDefineSymbolsForGroup`) only take effect at the next domain
  reload, and the active platform's built-in symbols (such as `UNITY_STANDALONE_WIN`) stay in place when
  building for another target, which can compile the wrong code.
- Build callbacks the page names: `BuildPlayerProcessor`, `IPreprocessBuildWithContext`,
  `IProcessSceneWithReport`, `IPostprocessBuildWithContext`.

## Checked
Date: 2026-11-07

Read: the full `BuildPipeline.BuildPlayer` page and, from the Editor command line page (about 40K
characters), the general arguments, Batch mode, Build and License sections in chunks plus a search of
all argument names. I did not read the Package Manager, Test, Graphics API, Android/iOS and other
sections, nor the linked "Create a build from the command line" or licence pages.

Removed because the pages do not confirm it: `BuildOptions.StrictMode`, the DEV_BUILD environment
variable, `r.summary.totalTime` and the `/1e6` size print, "non-zero exit on compile errors" (the page
says exceptions and failed operations exit 1), `Library/` caching per target, the `-buildVersion`
`PlayerSettings.bundleVersion` pattern, GameCI, Unity Build Server, the "Scripts have compiler errors"
log string, the Addressables `BuildPlayerContent` gotcha, Hub CLI `install-modules` and the Verify list.

Method: documentation only; no commands were run.
