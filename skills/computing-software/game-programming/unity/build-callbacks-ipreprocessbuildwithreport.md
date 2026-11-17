---
id: computing-software.game-programming.unity.build-callbacks-ipreprocessbuildwithreport
name: build-callbacks-ipreprocessbuildwithreport
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, ipreprocessbuildwithreport, ipostprocessbuildwithreport, iprocessscenewithreport, build-callbacks, game-programming]
level: practitioner
status: docs-checked
description: "Unity build callback interfaces IPreprocessBuildWithReport, IPostprocessBuildWithReport and IProcessSceneWithReport: Player-only scope, Context alternatives, scene caching."
sources: ["https://docs.unity3d.com/ScriptReference/Build.IPreprocessBuildWithReport.html", "https://docs.unity3d.com/ScriptReference/Build.IPostprocessBuildWithReport.html", "https://docs.unity3d.com/ScriptReference/Build.IProcessSceneWithReport.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build callbacks with IPreprocessBuildWithReport

**Goal:** choose the right Unity build callback interface and know what each is documented to do.

All three are in namespace `UnityEditor.Build` (assembly `UnityEditor.CoreModule`) and derive from
`IOrderedCallback`, so they inherit `callbackOrder`.

| Interface | Method | Documented behaviour |
|---|---|---|
| `IPreprocessBuildWithReport` | `OnPreprocessBuild` | callback before the build starts; start of the Player build |
| `IPostprocessBuildWithReport` | `OnPostprocessBuild` | callback after the build is complete; immediately after the Player build |
| `IProcessSceneWithReport` | `OnProcessScene` | callback for each scene during the build |

## Rules from the pages
- `IPreprocessBuildWithReport` behaves like `IPreprocessBuildWithContext` but is invoked only for Player
  builds. The page says to use `IPreprocessBuildWithContext` instead, because it is also invoked for
  AssetBundle and content directory builds. The same applies to `IPostprocessBuildWithReport` and
  `IPostprocessBuildWithContext`.
- `IProcessSceneWithReport`: if the scene or related content is unchanged since the previous Player
  build, Unity does not build the scene and uses cached Player build data; the callback is then not
  called.
- `BuildPipeline.BuildPlayer` lists `BuildPlayerProcessor`, `IPreprocessBuildWithContext`,
  `IProcessSceneWithReport` and `IPostprocessBuildWithContext` as callbacks that run at strategic points.
- The pages refer to a "Use build callbacks" manual page for more detail (not opened).

## Checked
Date: 2026-11-07

Read in full: the three interface reference pages (each is a short definition, remarks and one-row
method table) and the Remarks of `BuildPipeline.BuildPlayer`. The "Use build callbacks" manual page was
not fetched, and no method parameter pages were opened.

Removed because the pages do not confirm it: the StampVersion and StripDebugObjects samples, "lower runs
first", `BuildFailedException` semantics, the claim that `OnProcessScene` also runs when entering Play
Mode with a null report, the Editor-folder placement advice, the restore-after-build and postprocess
skipped-on-failure notes, the `EditorOnly` tag, the related hook list and the Verify list.

Method: documentation only; no commands were run.
