---
id: computing-software.game-programming.unity.resources-folder-tradeoffs-and-migration
name: resources-folder-tradeoffs-and-migration
category: computing-software
field: game-programming
product: unity
tags: [unity, resources-load, resources-folder, addressables, memory, game-programming]
level: practitioner
status: draft
description: "Understand Unity Resources folder costs (startup index, everything in build, no unloading granularity) and migrate Resources.Load calls to Addressables or direct references."
sources: ["https://docs.unity3d.com/Manual/LoadingResourcesatRuntime.html", "https://docs.unity3d.com/ScriptReference/Resources.Load.html", "https://learn.unity.com/tutorial/assets-resources-and-assetbundles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resources folder trade-offs and migration

**Goal:** know why `Resources/` hurts at scale and move off it safely.

## How Resources works
Every asset under any folder named `Resources` (and its dependencies) goes into the build, used or
not, packed into one data file. At startup the player builds a lookup index of all of them;
large Resources folders measurably increase startup time and memory, and patching changes the whole
blob. `Resources.Load<T>("Path/Name")` takes paths relative to a Resources folder, no extension.

## Acceptable uses
Small, always-needed bootstrap data (a settings ScriptableObject, a debug font), prototypes, and
test fixtures. Keep it under a few MB.

## Migration
1. Audit: `grep -rn "Resources.Load" Assets/` and list Resources folders and their size (Build Report).
2. Prefer **direct serialized references** where the loader is always present anyway.
3. Otherwise mark assets Addressable: Groups window > Tools > **Convert Legacy AssetBundles** is for
   bundles; for Resources, selecting a Resources asset and ticking Addressable offers to move it out
   of Resources (keeps address = old path).
4. Replace calls:
```csharp
// before
var cfg = Resources.Load<GameConfig>("Config/Game");
// after
var h = Addressables.LoadAssetAsync<GameConfig>("Config/Game");
var cfg = await h.Task;   // keep h, Release when done
```
5. Async ripple: callers become async; for startup data, load in a bootstrap scene before gameplay.

## Unloading
`Resources.UnloadAsset` only for non-GameObject assets; otherwise `Resources.UnloadUnusedAssets`
(slow, scans everything). Addressables releases by handle refcount instead.

## Gotchas
- Assets referenced from Resources and from Addressables get duplicated in the build.
- Editor-only folders named `Resources` inside `Editor/` are still treated as Resources for editor
  loading (`EditorGUIUtility.Load` uses Editor Default Resources).

## Verify
- [ ] Build Report shows Resources content reduced to the intended bootstrap set.
- [ ] Startup time measured before/after on the slowest target device.
