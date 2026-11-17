---
id: computing-software.game-programming.unreal-engine.asset-registry-queries
name: asset-registry-queries
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-asset-manager, asset-registry, fassetdata, asset-tags, game-programming]
level: practitioner
status: docs-checked
description: "Query Unreal's Asset Registry without loading assets: FARFilter component rules, FAssetData, AssetRegistrySearchable tags, asynchronous gathering and the IAssetRegistry API."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-registry-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/AssetRegistry/IAssetRegistry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asset Registry queries

**Goal:** list assets and read their metadata without loading them.

## What it is
The Asset Registry is an editor subsystem that gathers information about unloaded assets asynchronously while the
editor loads and keeps it in memory; the Content Browser is its main consumer but it may be used anywhere in editor
code.

## Getting assets
The Asset Registry page loads the module with
`FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry")` and calls `Get()` on it. The `IAssetRegistry`
API page also lists `static IAssetRegistry& GetChecked()`.
Query functions on the guide page: `GetAssetsByPackageName()`, `GetAssetsByPath()`, `GetAssetByObjectPath()`,
`GetAssetsByTagValues()`, `GetAllAssets()` (can be slow), and `GetAssets()` with an `FARFilter` for several criteria.
The API page lists `GetAssets(const FARFilter&, TArray<FAssetData>&, bool bSkipARFilteredAssets)` and
`GetAssetsByClass(FTopLevelAssetPath ClassPathName, TArray<FAssetData>&, bool bSearchSubClasses)`; the guide page's
older example passes `Class->GetFName()`, so check the signature in your engine version.

## FARFilter rules
Components: PackageName, PackagePath, Collection, Class, Tags/Value pairs. An asset passes only if it satisfies ALL
components used; within one component it needs to match ANY element. Example from the page: with PackagePath
`/Game/Meshes` and Classes UParticleSystem and UStaticMesh, `/Game/Meshes/BeachBall` (a StaticMesh) passes; with only
class UParticleSystem it fails; with PackagePath `/Game/NotMeshes` it fails.

## FAssetData
Holds what is known before load: ObjectPath, PackageName, PackagePath, GroupNames, AssetName, AssetClass and
`TagsAndValues` (a `TMap<FName, FString>`). `GetAsset()` loads the asset if needed and returns the `UObject*`;
`IsAssetLoaded()` checks without loading.

## Tags
Only properties marked `AssetRegistrySearchable` in `UPROPERTY()` are gathered; values are written when the asset is
saved (header of the UAsset file), so existing assets must be resaved. The page's example is `UTexture::Filter` giving
the string value such as "TF_Linear". For data that is not a property, override `GetAssetRegistryTags()` (inherited
from `UObject`) to add key/value pairs.

## Asynchronous gathering
The registry may not yet know every asset. Delegates on `IAssetRegistry`: `OnAssetAdded()`, `OnAssetRemoved()`,
`OnAssetRenamed()`, `OnFilesLoaded()` (initial search complete), `OnFileLoadProgressUpdated()`; `IsLoadingAssets()`
returns true while it is still loading. Keep `OnAssetAdded` handlers fast: the page's code comment says slow code
slows the gathering process. In commandlets the registry gathers synchronously and the `LoadModule()` call blocks until
done. The API page also lists `SearchAllAssets(bool bSynchronousSearch)` ("Look for all assets on disk (can be async
or synchronous)") and `IsSearchAllAssets()`. Slate frontends waiting on discovery should include an
`SAssetDiscoveryIndicator`.

## Checked
Date: 2026-11-07. Read in full: the Asset Registry guide page (all sections, code blocks included) and the
`IAssetRegistry` API page member tables (read via search for GetAssets, GetAssetsByClass, GetChecked, IsLoadingAssets,
OnFilesLoaded, SearchAllAssets, not every row opened). The `FARFilter` and `FAssetData` API pages return empty text and
could not be read, so `ClassPaths`, `bRecursiveClasses`, `bRecursivePaths`, `GetTagValue` and `GetSoftObjectPath` were
removed. Both pages are unversioned and state no engine version.
Also removed as unconfirmed: cooked-build `AssetRegistry.bin` behaviour and `CookedTagsWhitelist/AllowList` ini
settings, the `FAssetRegistryTagsContext` "UE 5.4+" signature, Blueprint-class `NativeParentClass` filtering, redirector
filtering advice, and the Verify checklist.
Method: documentation only; no commands were run.
