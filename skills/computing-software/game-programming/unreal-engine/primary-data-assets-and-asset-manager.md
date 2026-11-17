---
id: computing-software.game-programming.unreal-engine.primary-data-assets-and-asset-manager
name: primary-data-assets-and-asset-manager
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-asset-manager, primary-data-asset, primary-asset-id, asset-bundles, uassetmanager, soft-references, async-loading, game-programming]
level: advanced
status: draft
description: "Use Unreal's Asset Manager with Primary Data Assets: PrimaryAssetId, Primary Asset Types config, asset bundles, async loading by id and cook rules."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UPrimaryDataAsset"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Primary Data Assets and the Asset Manager

**Goal:** game content (items, characters, levels) discoverable and loadable by id, with only what
is needed in memory, and cooked deliberately.

## Primary vs secondary assets
- **Primary assets** have a `FPrimaryAssetId` (Type:Name), are managed by the Asset Manager, and can
  be queried/loaded without hard references. Maps are primary by default.
- **Secondary assets** (textures, meshes) load because a primary asset references them.

## Define a type
```cpp
UCLASS(BlueprintType)
class UItemDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly) FText DisplayName;
    UPROPERTY(EditDefaultsOnly) int32 MaxStack = 1;
    UPROPERTY(EditDefaultsOnly, meta=(AssetBundles="UI"))   TSoftObjectPtr<UTexture2D> Icon;
    UPROPERTY(EditDefaultsOnly, meta=(AssetBundles="Game")) TSoftObjectPtr<UStaticMesh> WorldMesh;

    virtual FPrimaryAssetId GetPrimaryAssetId() const override
    { return FPrimaryAssetId(TEXT("Item"), GetFName()); }
};
```
`UPrimaryDataAsset` provides a default `GetPrimaryAssetId` using the native class; overriding gives a
stable type name.

## Register in Project Settings > Asset Manager (DefaultGame.ini)
```ini
[/Script/Engine.AssetManagerSettings]
+PrimaryAssetTypesToScan=(PrimaryAssetType="Item",AssetBaseClass=/Script/MyGame.ItemDefinition,bHasBlueprintClasses=False,bIsEditorOnly=False,Directories=((Path="/Game/Items")),Rules=(Priority=-1,CookRule=AlwaysCook))
```
CookRule: `AlwaysCook`, `NeverCook`, `DevelopmentAlwaysProductionNeverCook`, `Unknown` (cook if
referenced). This is how data-only items get into packaged builds without being referenced by a map.

## Query and load
```cpp
UAssetManager& AM = UAssetManager::Get();
TArray<FPrimaryAssetId> Ids;
AM.GetPrimaryAssetIdList(FPrimaryAssetType("Item"), Ids);

TArray<FName> Bundles = { "UI" };      // load the definition + its UI bundle only
AM.LoadPrimaryAssets(Ids, Bundles, FStreamableDelegate::CreateUObject(this, &UInventoryMenu::OnItemsLoaded));
...
UItemDefinition* Def = AM.GetPrimaryAssetObject<UItemDefinition>(Id);
// unload when done:
AM.UnloadPrimaryAssets(Ids);
```
`ChangeBundleStateForPrimaryAssets` switches bundles (e.g. from UI to Game when an item is equipped).
The Asset Manager keeps loaded primary assets alive until unloaded.

## Custom Asset Manager
Subclass `UAssetManager` (set `AssetManagerClassName` in DefaultEngine.ini) to add startup loading
of core data (`StartInitialLoading`) and typed helpers.

## Auditing
Tools > Audit > Asset Audit window shows primary assets, sizes and chunk assignment; Reference
Viewer shows soft vs hard references; Size Map shows what a primary asset pulls in.

## Verify
- [ ] Packaged build lists all items (cook rules include them) without any map referencing them.
- [ ] Opening the inventory loads only the UI bundle (meshes not resident, check `obj list class=StaticMesh`).
- [ ] Unloading primary assets frees their bundle memory after GC.
