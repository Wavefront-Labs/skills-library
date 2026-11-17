---
id: computing-software.game-programming.unity.initializeonload-and-editor-lifecycle
name: initializeonload-and-editor-lifecycle
category: computing-software
field: game-programming
product: unity
tags: [unity, initializeonload, editor-scripting, domain-reload, editorapplication, game-programming]
level: practitioner
status: draft
description: "Run editor code at the right time with InitializeOnLoad, InitializeOnLoadMethod, EditorApplication callbacks, playModeStateChanged and reload events without slow reloads."
sources: ["https://docs.unity3d.com/ScriptReference/InitializeOnLoadAttribute.html", "https://docs.unity3d.com/ScriptReference/EditorApplication-playModeStateChanged.html", "https://docs.unity3d.com/ScriptReference/AssemblyReloadEvents.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InitializeOnLoad and editor lifecycle

**Goal:** editor tooling that hooks in on load and play mode transitions, without slowing every
script reload.

## Entry points
```csharp
[InitializeOnLoad]
static class ToolBootstrap {
    static ToolBootstrap() {                      // static ctor after every domain reload
        EditorApplication.playModeStateChanged += OnPlayMode;
        AssemblyReloadEvents.beforeAssemblyReload += SaveState;
        EditorApplication.delayCall += () => Debug.Log("editor ready");   // runs after load completes
    }
    static void OnPlayMode(PlayModeStateChange s) {
        if (s == PlayModeStateChange.ExitingEditMode) EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo();
    }
    static void SaveState() => SessionState.SetInt("tool.tab", 2);
}
```
- `[InitializeOnLoadMethod]` on a static method is the same without a class attribute.
- `[InitializeOnEnterPlayMode]` runs on entering play mode even with domain reload disabled; use it to
  reset statics.
- Runtime equivalent: `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]`.

## Callbacks worth knowing
| Callback | When |
|---|---|
| `EditorApplication.delayCall` | once, after inspectors update; safe for AssetDatabase work |
| `EditorApplication.update` | every editor tick; keep it tiny |
| `playModeStateChanged` | ExitingEditMode, EnteredPlayMode, ExitingPlayMode, EnteredEditMode |
| `EditorApplication.quitting` | editor closing |
| `AssemblyReloadEvents.before/afterAssemblyReload` | around domain reloads |
| `CompilationPipeline.compilationFinished` | after scripts compile |

## Rules
- Static ctor runs on **every** reload: do no heavy work, no AssetDatabase.Refresh, no
  `FindAssets` scans; defer with delayCall and cache.
- Asset operations during import (inside static ctor at startup) can fail because the AssetDatabase is
  not ready; delayCall avoids it.
- Persist editor state across reloads with `SessionState` (session) or `EditorPrefs` (machine).

## Verify
- [ ] Editor > Preferences diagnostic or Profiler (Edit mode) shows no measurable reload cost added.
- [ ] Hooks work with Enter Play Mode Options domain reload disabled.
