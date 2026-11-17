---
id: computing-software.game-programming.unity.additive-scene-loading
name: additive-scene-loading
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, scenemanager, additive-scene-loading, multi-scene-editing, setactivescene, unloadsceneasync, level-streaming, game-programming, active-scene-lighting]
level: practitioner
status: docs-checked
description: "Structure Unity games with additive scenes: persistent core scene plus content scenes, SetActiveScene, UnloadSceneAsync, and multi-scene editing."
sources: ["https://docs.unity3d.com/Manual/MultiSceneEditing.html", "https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.SetActiveScene.html", "https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.UnloadSceneAsync.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Additive scene loading

**Goal:** keep a persistent core scene and load or unload content scenes additively, for streaming
worlds and collaborative editing.

## Why multiple scenes
Unity's multi-scene page says that for large streaming worlds, or to manage multiple scenes at
runtime, you can open and edit several scenes in the Editor simultaneously, which also helps when
editing scenes collaboratively. Its sub-pages cover setting up multiple scenes, baking lightmaps and
occlusion culling data across multiple scenes, and scripting multi-scene edits in the Editor or at
runtime.

## Loading and the active scene
```csharp
// Pattern from the SetActiveScene reference example
SceneManager.LoadScene("Scene2", LoadSceneMode.Additive);
// Later, once the scene is loaded:
bool ok = SceneManager.SetActiveScene(SceneManager.GetSceneByName("Scene2"));
```
- When you add a scene additively, the first scene stays the active scene until you switch it.
- The active scene is the target for new GameObjects instantiated by scripts and the scene whose
  lighting settings are used.
- `SetActiveScene` returns `false` if the scene is not loaded yet, so check the result.
- There must always be one active scene, and the active scene has no impact on what scenes are
  rendered.

## Unloading
- `SceneManager.UnloadSceneAsync` destroys all GameObjects associated with the scene and removes it
  from the SceneManager. It accepts a build index, a scene name or path, or a `Scene`, with an
  optional `UnloadSceneOptions`, and returns an `AsyncOperation`.
- The scene argument can be a full scene path, the path shown in the Build Settings window, or just
  the scene name. A bare name unloads the first match in the list, so use the full path when several
  scenes share a name. Matching is case-insensitive.
- Because it is async there are no guarantees about completion time; use the returned
  `AsyncOperation` to see when it has completed.
- Assets are not unloaded with the scene. Call `Resources.UnloadUnusedAssets` to free asset memory.
- It is not possible to use `UnloadSceneAsync` when there are no scenes to load; for example a project
  with a single scene cannot use it.

## Checked
Date: 2026-11-07

Read in full: the Multi-scene page (a short overview of three sub-topics; the sub-pages themselves
were not opened), the `SceneManager.SetActiveScene` reference including its example (all text), and
the `SceneManager.UnloadSceneAsync` reference (all five overloads and their remarks). Pages were read
via their current Unity 6 redirects.

Trimmed because no cited page confirms it: the `async Awaitable SwitchLevel` snippet, the
`Instantiate`-without-parent detail, skybox/ambient wording, the "Cross scene references are not
supported" message and its workaround patterns, Scene Setup via `EditorSceneManager`,
`RuntimeInitializeOnLoadMethod` bootstrap, camera/AudioListener/EventSystem and NavMesh gotchas,
the Addressables release remark, and the invented Verify checklist.

Method: documentation only; no commands were run.
