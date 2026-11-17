---
id: computing-software.game-programming.unity.scene-unload-and-unload-unused-assets
name: scene-unload-and-unload-unused-assets
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, unload-unused-assets, scene-unloading, memory-leak, game-programming]
level: practitioner
status: docs-checked
description: "Unload Unity scenes cleanly with UnloadSceneAsync and Resources.UnloadUnusedAssets, find what keeps assets alive, and avoid hitches during unloads."
sources: ["https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.UnloadSceneAsync.html", "https://docs.unity3d.com/ScriptReference/Resources.UnloadUnusedAssets.html", "https://docs.unity3d.com/ScriptReference/Application-backgroundLoadingPriority.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scene unload and UnloadUnusedAssets

**Goal:** memory actually drops after leaving a level, without a long hitch.

## What unloading does
- `SceneManager.UnloadSceneAsync(scene)` destroys all GameObjects associated with the Scene and removes it from the SceneManager. It takes a build index, a scene name or path, or a `Scene`, and returns an `AsyncOperation`. Assets are currently not unloaded: call `Resources.UnloadUnusedAssets` to free asset memory.
- A scene name may be the full path, the path shown in Build Settings, or just the name (the first match is unloaded; use the full path when names clash). Matching is case-insensitive, and as it is async there is no guarantee about completion time.
- It is not possible to use `UnloadSceneAsync` if there are no other scenes to load: a project with a single scene cannot use it. Keep a persistent bootstrap scene.
- `Resources.UnloadUnusedAssets()` returns an `AsyncOperation` you can yield on. An asset is unused if it is not reached after walking the whole GameObject hierarchy, including script components; static variables are also examined. The script execution stack is not examined, so an asset referenced only from the stack will be unloaded.
- Assets other than ScriptableObjects are loaded back the next time one of their properties or methods is used. Take care with assets modified in memory: call `EditorUtility.SetDirty` before an asset garbage collection is triggered.

```csharp
IEnumerator SwapLevel(string oldScene, string newScene) {
    yield return SceneManager.UnloadSceneAsync(oldScene);
    yield return Resources.UnloadUnusedAssets();      // do it behind the loading screen
    yield return SceneManager.LoadSceneAsync(newScene, LoadSceneMode.Additive);
}
```

## What keeps assets alive
Anything still reachable from the hierarchy, script components or static variables. Static fields holding prefabs, sprites or ScriptableObjects therefore keep them loaded.

## Hitch control
- Run unloads behind a loading screen or fade.
- `Application.backgroundLoadingPriority` limits main-thread integration time per frame for asynchronous loads: Low 2 ms, BelowNormal 4 ms, Normal 10 ms, High 50 ms. It has no effect in the Editor, only in a built Player.

## Checked
Method: 2026-11-09 docs-only read of the SceneManager.UnloadSceneAsync (int, string and the start of the Scene overload), Resources.UnloadUnusedAssets and Application.backgroundLoadingPriority script reference pages. Removed claims not on those pages: LoadSceneMode.Single auto-unloading unused assets, Addressables/AssetBundle/event/material leak sources, the Memory Profiler workflow, GC.Collect advice, the null-return case, and the Verify list.
