---
id: computing-software.game-programming.unity.unity6-build-profiles
name: unity6-build-profiles
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, unity-build-profiles, build-profiles, per-platform-overrides, game-programming]
level: practitioner
status: draft
description: "Use Unity 6 Build Profiles: per-profile scene lists, scripting defines, player settings overrides, and building a profile from the command line in CI."
sources: ["https://docs.unity3d.com/6000.0/Documentation/Manual/build-profiles.html", "https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Build.Profile.BuildProfile.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unity 6 Build Profiles

**Goal:** demo/dev/release or store-specific builds of the same platform without hand-editing
settings before each build.

## What a profile holds
File > Build Profiles: each platform has a default "platform profile"; you can add **custom build
profiles** (assets, `.asset` in the project) that override:
- Scene list (or use the shared list),
- Scripting Define Symbols (added to the platform's),
- Player Settings overrides (a copy of player settings stored in the profile),
- Graphics settings / quality overrides (6000.1+ adds more),
- Platform build settings (development build, compression, Android export...).

## Typical setup
| Profile | Defines | Scenes |
|---|---|---|
| Win-Dev | `DEV_CONSOLE;CHEATS` | all incl. test scenes |
| Win-Demo | `DEMO` | first two levels |
| Win-Release | (none) | shipping list |

## Building from code / CI
```csharp
public static void BuildDemo() {
    var profile = AssetDatabase.LoadAssetAtPath<BuildProfile>("Assets/Settings/Build/Win-Demo.asset");
    var opts = new BuildPlayerWithProfileOptions {
        buildProfile = profile, locationPathName = "Builds/Demo/Game.exe", options = BuildOptions.None };
    var report = BuildPipeline.BuildPlayer(opts);
    if (report.summary.result != BuildResult.Succeeded) EditorApplication.Exit(1);
}
```
Command line: `Unity -batchmode -quit -projectPath . -executeMethod Builds.BuildDemo -logFile -`, or
`-activeBuildProfile <path>` with `-build <path>` (Unity 6 command-line arguments).
`BuildProfile.SetActiveBuildProfile(profile)` switches the active profile (may trigger reimport).

## Gotchas
- Defines in a profile only apply when that profile is active or built; IDE intellisense follows the
  active profile.
- Player settings override in a profile is a full copy at creation time — later edits to the global
  player settings do not flow into it. Review when bumping version numbers (or set version in the
  build script).
- Commit the profile assets; they are the source of truth for CI.

## Verify
- [ ] CI builds each profile and logs `PlayerSettings` defines in the build output.
- [ ] Demo build excludes non-demo scenes (check build report scene list).
