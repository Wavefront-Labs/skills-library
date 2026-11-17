---
id: computing-software.game-programming.unity.addressables-labels-and-loading-by-label
name: addressables-labels-and-loading-by-label
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables-labels, addressables, asset-loading, game-programming]
level: practitioner
status: docs-checked
description: "Use Addressables labels to load sets of assets (LoadAssetsAsync, MergeMode) and to drive bundle packing by label."
sources: ["https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/Labels.html", "https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/load-assets.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Addressables labels

**Goal:** load "all weapons of level 3" by tag, not by individual keys.

## Assign and manage labels
Tag Addressable assets with one or more labels in the Addressables Groups window. Create and delete labels in the Labels window (Window > Asset Management > Addressables > Groups > Tools > Windows > Labels): the + button adds one, the - button deletes the selected one, and deleting a label removes it from all assets. Until you run an Addressables build, re-adding a deleted label with the exact same string restores it on its original assets; after a build it no longer reapplies.

Labels are used to: identify which assets to load at runtime (as keys), pack assets in a group into bundles, and filter in the Groups window.

## Load by label
`LoadAssetAsync` accepts a label as a key, but if the key resolves to several assets only the first one found is loaded. To load several, use `LoadAssetsAsync` with a single key (such as a label) or a list of keys:

```csharp
loadHandle = Addressables.LoadAssetsAsync<GameObject>(
    keys,                          // for example a List<string> of labels
    addressable => { /* called for every loaded asset */ },
    Addressables.MergeMode.Intersection,
    false);                        // releaseDependenciesOnFailure
yield return loadHandle;
// later
loadHandle.Release();
```
- Merge mode with several keys: `Union` includes assets matching any key, `Intersection` assets matching every key, `UseFirst` assets only from the first key that resolves to a valid location.
- `releaseDependenciesOnFailure` true: the operation fails on any single load error and the operation and loaded assets are released. False: it loads what it can, does not release, still completes as Failed if it fails, and the returned list has null where an asset failed. Use true when assets must load as a set (such as a level).
- Release the operation handle with `Release` (the example does so in `OnDestroy`).

## Packing by label
Setting a group's Bundle Mode to pack by label makes the build script create one bundle per unique combination of labels in the group. Example from the docs: assets labelled cat or dog and small or large produce four bundles. Many labels per asset multiply the bundle count.

## Checked
Method: 2026-11-09 docs-only read of the Addressables 2.3 Labels overview and Load assets pages in full. Removed claims not on those pages: the LoadResourceLocationsAsync, GetDownloadSizeAsync and DownloadDependenciesAsync sections, the InvalidKeyException on zero matches, the AssetLabelReference advice, the three-argument overload form and `await h.Task`, and the Verify list.
