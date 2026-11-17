---
id: computing-software.game-programming.unity.addressables-and-build-pipeline
name: addressables-and-build-pipeline
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables, asset-bundles, build-pipeline, build-size, catalog, remote-content, content-update, groups, labels, platform-variants, memory-management, async-loading, resources-folder, player-settings, game-programming]
level: practitioner
status: draft
description: "Manage Unity asset loading and shipping with Addressables: groups, labels, remote vs local content, and keeping build size and memory under control."
sources: ["https://docs.unity3d.com/Packages/com.unity.addressables@latest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Addressables and the Unity build pipeline

**Goal:** load and ship assets deliberately — know what's in the build, what's
downloaded on demand, when it's released from memory, and why a `Resources`
folder is the thing that quietly ruins all of it.

## Why not `Resources/`
Everything in a `Resources` folder is forced into the build and loaded by string
path with no dependency tracking — Unity can't strip unused assets inside it, and
every subfolder's contents ship even if 90% is unused. It doesn't scale past a
small project. Addressables replace it: assets get an address (a GUID-backed key,
editable to a friendly string) and are organized into **Groups**, each of which
builds to one or more asset bundles.

## Groups, labels, and load paths
- A **Group**'s packing mode (Packed Together / Packed Separately / Packed Together
  by Label) decides bundle granularity. Packed Together = fewer, bigger bundles
  (less overhead, but a player downloads the whole bundle for one asset inside it).
  Packed Separately = one bundle per asset (fine-grained download, more overhead
  per bundle header).
- **Labels** let you load/release logically ("level-3", "boss-vo") without caring
  which bundle backs them: `Addressables.LoadAssetsAsync<GameObject>("level-3", ...)`.
- Each Group's **Build & Load Paths** can be Local (ships in the build) or Remote
  (hosted — a CDN URL, `{UnityEngine.AddressableAssets.Addressables.RuntimePath}`
  substitutions). Remote groups need a **content catalog** published separately
  from the player build, and the catalog's version must be bumped on every content
  update or clients keep hitting a stale CDN entry.

## Loading and the handle you must release
```csharp
AsyncOperationHandle<GameObject> handle = Addressables.LoadAssetAsync<GameObject>("enemy_goblin");
await handle.Task;
var instance = Instantiate(handle.Result);
...
Addressables.Release(handle);   // decrements the internal refcount
```
Addressables refcounts loaded assets. Forgetting `Release` (or
`ReleaseInstance` for `InstantiateAsync`) leaks memory silently — nothing crashes,
the asset just never unloads, and it only shows up as a slow memory climb over a
play session, caught in the Addressables Profiler window (not the normal Memory
Profiler at a glance) or Window → Asset Management → Addressables → Event Viewer.
Pair every Load/Instantiate with exactly one Release/ReleaseInstance, ideally in
the same class that requested it.

## Build size triage
When a build is bloated: Build Report (`Build Settings → the hamburger menu after
a build → "Open Addressables Report"` or the Editor log's size breakdown) shows
per-asset contribution. Common offenders: uncompressed textures (check **Texture
Import** compression format per-platform, not just the default), unused shader
variants (`Project Settings → Graphics → Shader Stripping`, strip unused variants
per quality level), duplicate assets pulled into multiple Addressables groups
because of a shared dependency not marked Addressable itself (mark the shared
asset Addressable so it's deduplicated into its own bundle instead of copied into
every group that references it).

## Platform variants
Different texture compression per platform (ASTC on mobile, DXT/BC on desktop,
PVRTC legacy iOS) is set per-platform in the texture's import settings, not a
separate asset — Addressables builds separate bundles per active build target
automatically. Don't hand-roll a "mobile assets" folder duplicate; it's the import
settings override that should carry the platform split.

## Verify
- [ ] `Resources/` is empty or near-empty; new content goes through Addressables.
- [ ] Every `LoadAssetAsync`/`InstantiateAsync` call has a matching
      `Release`/`ReleaseInstance`, verified by watching the Addressables Event
      Viewer refcount return to 0 after a scene unload.
- [ ] Remote groups have a published catalog, and content-update builds bump the
      catalog version (test by force-pointing a dev client at the new catalog URL).
- [ ] Build Report checked after any large content addition, not just at ship time.
