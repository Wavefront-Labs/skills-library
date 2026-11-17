---
id: computing-software.game-programming.unity.enter-play-mode-options-and-domain-reload
name: enter-play-mode-options-and-domain-reload
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, domain-reload, enter-play-mode-options, scene-reload, static-fields, iteration-time, runtimeinitializeonloadmethod, game-programming]
level: practitioner
status: docs-checked
description: "Unity Enter Play Mode settings: domain and scene reload defaults, what persists when off, and resetting statics with OnEnteringPlayMode, OnExitingPlayMode, AutoStaticsCleanup."
sources: ["https://docs.unity3d.com/Manual/ConfigurableEnterPlayMode.html", "https://docs.unity3d.com/Manual/DomainReloading.html", "https://docs.unity3d.com/Manual/SceneReloading.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enter Play Mode options and domain reload

**Goal:** know what the Enter Play Mode settings change and reset static state correctly.

## The setting (current manual)
- Project Settings (Edit > Project Settings) > Editor tab > Enter Play Mode Settings > "When entering Play
  Mode": Reload Domain and Scene; Reload Scene only (**the default**); Reload Domain only; Do not reload
  Domain or Scene.
- By default Unity reloads the scene and does NOT reload the scripting domain on entering Play mode (the
  old draft said the opposite). The page notes it is recommended to leave domain reload off, partly to
  prepare for the CoreCLR runtime, which has no domain reload concept.
- Both reloads take longer as scripts and scenes get more complex; turning them off prioritizes iteration
  time over accuracy of the Play mode simulation.

## Domain reload off: effects
- Non-serialized fields keep values assigned in Play mode on returning to Edit mode (all script types,
  including MonoBehaviours on prefab assets, ScriptableObjects, custom C# types).
- Static variables and static event subscribers persist between Play mode sessions.
- No additional `OnDisable`/`OnEnable` calls for `[ExecuteInEditMode]`/`[ExecuteAlways]` scripts.
- You must reset state in your code.

## Scene reload
- On by default: Unity destroys scene GameObjects and reloads the scene from disk. Turned off, Unity only
  resets the scene's modified contents but still calls the same event functions (`OnEnable`,
  `OnDisable`, `OnDestroy`) as if freshly loaded.
- Startup time in the Editor is then not representative of a build; enable scene reload to debug or
  profile startup.
- Unity does not recreate objects or call constructors, so non-serialized fields keep Play mode values.
  `private` fields are serialized by the Editor's hot reloading (not by the regular build pipeline), so
  modified private fields may still reset on exit even with both reloads off. Null private/internal
  array and `List` fields become empty during domain reload and stay non-null for runtime scripts.
- `[ExecuteInEditMode]`/`[ExecuteAlways]` scripts do not receive `OnDestroy` or `Awake` calls; page
  suggests initialising affected fields in `OnEnable` inside a check of `EditorApplication.isPlaying`.

## Resetting statics from code
- Manual: lifecycle attributes `[OnEnteringPlayMode]` and `[OnExitingPlayMode]` on static methods (page
  example uses `public static partial class PlayModeManager`). Often most efficient to reset on exit; but
  if code also runs in Edit mode and may change statics there, reset on entering Play mode.
- With domain reload off, `MonoBehaviour.OnDisable` is skipped and with scene reload off `OnDestroy` is
  skipped for Edit-mode scripts, so they are inappropriate for resetting state in such scripts.
- Automatic: `[AutoStaticsCleanup]` / `[NoAutoStaticsCleanup]` on static fields (namespace
  `Unity.Scripting.LifecycleManagement`; the declaring type must be `partial`). Code generation is on by
  default. Non-readonly field: the inline initializer is re-evaluated on each Play mode transition;
  `readonly` collections are preserved and `Clear()` is called. The static constructor is not re-run.
  Parameterless accessible `Dispose` on the old value is called for non-readonly fields. An
  undeterminable member gives error `UAC0034`.
- Page guidance table: events/delegates, collections of user objects, references to Unity objects ->
  `[AutoStaticsCleanup]`; ID counters, cached `GUIStyle`/`GUIContent` -> `[NoAutoStaticsCleanup]`.
- Analyzer warnings `UAL0010` to `UAL0014` (analysis off by default). Configure per assembly with
  `<assemblyDefinitionName>.globalconfig` containing `build_property.UnityEnableAutoStaticsCleanupCodeGen`
  (default true) and `build_property.UnityEnableAutoStaticsCleanupAnalysis` (default false).

## Checked
Date: 2026-11-07

Read in full: the Configurable Enter Play Mode page, the "domain reload" page including its code
examples, the property tables and the analyzer table, and the "scene reload" page. The Domain and scene
reload execution order reference and the `[AutoStaticsCleanup]` API page were not opened.

Corrected: the draft claimed domain reload is on by default and the draft's menu wording ("Do not reload
Domain or Scene (fastest)", Unity 6 UI vs older checkbox) is not on the page; the default per the page is
"Reload Scene only". Removed because the pages do not confirm it: "domain reload often takes several
seconds", the `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]` reset sample (the manual uses
`[OnEnteringPlayMode]`, `[OnExitingPlayMode]` and `[AutoStaticsCleanup]` instead),
`EditorApplication.playModeStateChanged`, static constructors "do not run again" for the no-reload case
(page states it only for generated cleanup), third-party package support, the ScriptableObject
statement, and the Verify timing targets.

Method: documentation only; no commands were run.
