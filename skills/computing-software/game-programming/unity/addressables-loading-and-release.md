---
id: computing-software.game-programming.unity.addressables-loading-and-release
name: addressables-loading-and-release
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables, addressables-release, asyncoperationhandle, loadassetasync, instantiateasync, reference-counting, memory-leak, assetreference, game-programming]
level: practitioner
status: docs-checked
description: "Pair every Addressables load with a release: reference counts, bundle unloading, memory clearance, asset churn and the Profiler module for spotting leaks."
sources: ["https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/LoadingAddressableAssets.html", "https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/MemoryManagement.html", "https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/AssetReferences.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Addressables loading and release

**Goal:** every Addressables load is paired with a release, so bundles unload and memory returns.

## Reference counting
- The Addressables system keeps a reference count of every item it loads. Loading increments it,
  releasing decrements it, and at zero the item can be unloaded.
- When you explicitly load an Addressable asset, you must also release it when you finish with it.
- To avoid leaks (assets staying in memory after they are no longer needed), mirror every call to a
  load method with a call to a release method. You can release with the asset instance itself or with
  the result handle returned by the original load operation.

## Release does not unload immediately
- Unity does not unload released assets immediately: an asset's memory is not freed until the
  AssetBundle it belongs to is also unloaded.
- Bundles have their own reference count and are treated like Addressables whose contained assets are
  dependencies. Loading an asset from a bundle increases the bundle's count, releasing decreases it,
  and at zero Unity unloads the bundle and all assets in it.
- Worked example from the page: bundle `stuff` holds `tree`, `tank` and `cow`. Load `tree`, then
  `tank`; release `tree`. Its ref-count becomes zero but it is not unloaded: you can load part of a
  bundle but cannot unload part of one, so nothing in `stuff` unloads until the bundle does.

## Asset churn
Churn happens when you release the last item in a bundle and immediately reload that asset or another
one from the same bundle. Page example: materials `boat` and `plane` share texture `cammo` in its own
bundle; leaving level 1 releases `boat`, so `cammo` unloads, and loading `plane` reloads `cammo`.

## Finding leaks
Use the Addressables Profiler module to monitor loaded content: it shows when assets and their
dependencies load and unload. A released asset shows as released with disabled text, which does not
mean it was unloaded. The page says the module can also help detect asset churn.

## Loading overview (index pages)
- The `Addressables` class provides methods to load Addressable assets one at a time or in batches.
- An `AssetReference` can be a field on a MonoBehaviour or ScriptableObject that references an
  Addressable asset.
- The Loading overview links sub-pages on asynchronous loading and operation handles, loading assets
  by address, label or AssetReference, loading scenes, unloading, and preloading dependencies.

## Checked
Date: 2026-11-07

Read in full: Memory management overview (all sections: reference counts, memory leaks, memory
clearance, asset churn). The "Loading Addressable assets" and "Asset references overview" pages are
only tables of links to sub-pages, which were not opened; the AssetReferences fetch returned a very
short page and I read it all.

Removed because no cited page confirms it: the whole C# example, `handle.Task`, `InstantiateAsync` /
`ReleaseInstance` / `trackHandle` details, `LoadAssetsAsync` with labels and `MergeMode.Intersection`,
the AssetReference behaviours (throws on second load, `ReleaseAsset`, `RuntimeKeyIsValid`,
`AssetReferenceT` and label restriction), version claims about the Profiler module versus Event
Viewer, the "invalid operation handle" message, the Resources.UnloadUnusedAssets and pink-material
gotchas, the Play Mode Script gotcha and the invented Verify steps.

Method: documentation only; no commands were run.
