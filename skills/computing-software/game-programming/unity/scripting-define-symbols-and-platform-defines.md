---
id: computing-software.game-programming.unity.scripting-define-symbols-and-platform-defines
name: scripting-define-symbols-and-platform-defines
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, scripting-define-symbols, platform-defines, conditional-compilation, conditional-attribute, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity's platform #defines and custom scripting define symbols for conditional compilation, set per build target or profile, and avoid defines that break other platforms."
sources: ["https://docs.unity3d.com/Manual/platform-dependent-compilation.html", "https://docs.unity3d.com/Manual/custom-scripting-symbols.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripting define symbols and platform defines

**Goal:** platform- and build-specific code that compiles everywhere it should and nowhere it shouldn't.

## Built-in defines
- Editor: `UNITY_EDITOR`, `UNITY_EDITOR_WIN/OSX/LINUX`.
- Platform: `UNITY_STANDALONE`, `UNITY_STANDALONE_WIN`, `UNITY_IOS`, `UNITY_ANDROID`, `UNITY_WEBGL`,
  `UNITY_SERVER` (dedicated server build). Console symbols are in the platform's own documentation.
- Version: for editor 6000.0.33 Unity defines `UNITY_6000`, `UNITY_6000_0` and `UNITY_6000_0_33`; use
  `UNITY_X_Y_OR_NEWER` (for example `UNITY_6000_0_OR_NEWER`) for minimum-version checks.
- Build: `DEVELOPMENT_BUILD`, `ENABLE_IL2CPP`, `ENABLE_MONO`, `ENABLE_INPUT_SYSTEM`,
  `ENABLE_LEGACY_INPUT_MANAGER`. `#if DEBUG` is equivalent to `#if UNITY_EDITOR || DEVELOPMENT_BUILD`.
  `DEVELOPMENT_BUILD` only reflects the build option at build time; at runtime use `Debug.isDebugBuild`.
Platform defines describe the **target**, not the machine: in the editor with Android selected,
`UNITY_ANDROID` is true.

## Custom symbols
- Player Settings > Other Settings > Script Compilation > **Scripting Define Symbols** (per platform; select
  Apply to recompile), or a Build Profile (Add Settings > Scripting Defines).
- From code / CI:
```csharp
PlayerSettings.SetScriptingDefineSymbols(NamedBuildTarget.Android, new[] { "ENABLE_CHEATS", "USE_FMOD" });
```
- `csc.rsp` in the root of Assets, with a line `-define:FOO;BAR`, applies project-wide; changes need a script
  recompile. It is the only option that works in an Editor running in batch mode.
- Symbols from all applicable scopes are added together (csc.rsp + platform + active build profile).
- Symbols set from code with `SetScriptingDefineSymbols` take effect only after the Editor recompiles, so a
  `BuildPipeline.BuildPlayer` call on the next line does not see them.

## Using them
```csharp
#if UNITY_EDITOR || DEVELOPMENT_BUILD
    DevConsole.Register("god", ToggleGodMode);
#endif

#if UNITY_IOS && !UNITY_EDITOR
    [DllImport("__Internal")] static extern void _ShowReview();
#endif

[System.Diagnostics.Conditional("ENABLE_LOGS")]
public static void Log(string msg) => Debug.Log(msg);    // calls and argument evaluation vanish when undefined
```
`[Conditional]` beats wrapping every call site in `#if`, and the method still compiles so refactors
don't rot it.

## Gotchas
- Code inside a false `#if` isn't compiled, so it silently rots; build every platform in CI regularly.
- `UNITY_EDITOR` blocks inside runtime scripts are fine; `using UnityEditor;` must also be inside the guard.

## Checked
2026-11-01. Confirmed against the Unity manual (Unity scripting symbol reference, Custom scripting symbols) and
the PlayerSettings.SetScriptingDefineSymbols Scripting API: predefined symbol names, version symbol format,
DEBUG equivalence, set locations and their menu paths, csc.rsp rules, inheritance, array overload. Removed:
UNITY_PS5, UNITY_SWITCH, UNITY_2022_3_OR_NEWER example, asmdef Define Constraints note, serialized-field gotcha.
Method: documentation only; no commands were run.

## Verify
- [ ] Every target builds in CI with its define set.
- [ ] Release build contains no cheat/console symbols (search the build or decompile).
