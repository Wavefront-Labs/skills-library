---
id: computing-software.game-programming.unity.dontdestroyonload-and-bootstrap-scene
name: dontdestroyonload-and-bootstrap-scene
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, dontdestroyonload, bootstrap-scene, singleton, persistent-managers, runtimeinitializeonloadmethod, game-programming]
level: practitioner
status: docs-checked
description: "Keep Unity objects across scene loads with DontDestroyOnLoad (root objects only, duplicate guard) and run startup code with RuntimeInitializeOnLoadMethod load-type order."
sources: ["https://docs.unity3d.com/ScriptReference/Object.DontDestroyOnLoad.html", "https://docs.unity3d.com/ScriptReference/RuntimeInitializeOnLoadMethodAttribute.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DontDestroyOnLoad and startup methods

**Goal:** keep an object (for example background music) across scene loads without duplicating it, and
run initialisation code at startup.

## DontDestroyOnLoad
- Loading a new Scene destroys all current Scene objects; `Object.DontDestroyOnLoad(target)` preserves one.
  It returns nothing.
- It only works for root GameObjects or components on root GameObjects. For a component or GameObject,
  Unity also preserves all of the Transform's children.

## Duplicate guard (the page's example)
The page's `DontDestroy` script, on a GameObject tagged `music` in scene1, runs in `Awake`:
```csharp
GameObject[] objs = GameObject.FindGameObjectsWithTag("music");
if (objs.Length > 1) Destroy(this.gameObject);
DontDestroyOnLoad(this.gameObject);
```
When returning to scene1, the scene's own copy finds more than one tagged object and destroys itself.
(The page calls `DontDestroyOnLoad` after `Destroy` without a `return`.)

## RuntimeInitializeOnLoadMethod
- Attribute on a method (`AllowMultiple = false`) that gives a callback when the runtime starts up and
  loads the first scene. The page examples use `static` methods.
- Order: low-level systems initialise; `SubsystemRegistration` and `AfterAssembliesLoaded` callbacks;
  more setup (input systems etc.); `BeforeSplashScreen`; first scene starts loading; `BeforeSceneLoad`
  (scene objects loaded, `Awake` not yet called, all objects considered inactive); `Awake` and `OnEnable`
  on MonoBehaviours; `AfterSceneLoad` (objects fully loaded; active objects can be found with
  `FindObjectsByType`).
- Same invocations are ensured when entering Play mode in the Editor.
- Default load type is `AfterSceneLoad`. Order within each load type is not guaranteed.
- Use `AlwaysLinkAssemblyAttribute` on package or precompiled assemblies that contain such methods but
  may not contain types used in any built scene (see Managed code stripping).

## Checked
Date: 2026-11-07

Read in full: the `Object.DontDestroyOnLoad` page including both example scripts, and the
`RuntimeInitializeOnLoadMethodAttribute` page including its example. The `RuntimeInitializeLoadType`
enum page, Enter Play Mode Options and `SceneManager` pages were not opened.

Removed because neither page confirms it: that DDOL objects survive only `LoadSceneMode.Single`, the
warning logged for child objects and the `SetParent(null)` fix, assets referenced from DDOL objects
staying loaded, the Instance singleton with `OnDestroy`, the Boot scene at build index 0, the
`Resources.Load` Systems prefab bootstrap, the claim that it runs every Play from any scene, the domain
reload and `SubsystemRegistration` static reset recipe, the service locator / VContainer / Zenject
alternatives, and the Verify list. The cited pages do not describe a bootstrap-scene pattern, so the
name of this skill is broader than its content.

Method: documentation only; no commands were run.
