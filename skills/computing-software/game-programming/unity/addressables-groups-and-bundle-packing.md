---
id: computing-software.game-programming.unity.addressables-groups-and-bundle-packing
name: addressables-groups-and-bundle-packing
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables, addressables-groups, bundle-mode, content-packing, game-programming]
level: practitioner
status: docs-checked
description: "Design Unity Addressables groups with the Content Packing & Loading schema: build and load paths, Bundle Mode, compression, naming, Asset Load Mode and catalog options."
sources: ["https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/Groups.html", "https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/ContentPackingAndLoadingSchema.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Addressables groups and bundle packing

**Goal:** set group schema options deliberately, so bundles load, cache and update the way the
project needs.

## Where the settings are
A group is the main organizational unit of Addressables. To open the Content Packing & Loading
schema, open the Addressables Groups window (Window > Asset Management > Addressables > Groups) and
select a group; its settings show in the Inspector. This is the main schema used by the default
build script.

## Build and Load Paths
- **Build & Load Paths** is a Profile path pair: where the build creates this group's artifacts and
  where they load from at runtime. Choose a pair or pick `<custom>` to set Build Path and Load Path
  separately.
- Path options come from Profile variables. `LocalBuildPath` is for assets distributed as part of
  the application installation; `RemoteBuildPath` is for assets distributed through a remote hosting
  service such as Unity Cloud Content Delivery or another CDN.
- Use only variables intended for the setting (a load path variable in a build path setting gives no
  useful result). The Path Preview shows the resolved path; parts in braces such as
  `{UnityEngine.AddressableAssets.Addressable.RuntimePath}` are static variables resolved when
  Addressables initializes at runtime.
- The page warns you usually should not change local build or load paths from their defaults. If you
  do, copy the local build artifacts to the project's StreamingAssets folder before a Player build;
  altering the paths also precludes building Addressables as part of the Player build.

## Bundle Mode
- **Pack Together**: a single bundle containing all assets.
- **Pack Separately**: a bundle for each primary asset. Subassets (for example sprites in a sprite
  sheet) are packed together, as are assets within a folder added to the group.
- **Pack Together by Label**: a bundle for assets sharing the same combination of labels.

## Compression (Asset Bundle Compression, per group)
- Uncompressed: largest on disk and fastest to load; the page suggests it for local content if space
  allows, and says it gives the most accurate (smallest) platform patching.
- LZ4: chunk-based, so parts of the file can load without loading all of it. The page says to use
  it for all other local content if Uncompressed is not viable.
- LZMA: smallest bundles but slow to load. The page says to use it for all remote content and no
  local content. Downloaded LZMA bundles are recompressed when stored in the AssetBundle cache, which
  uses LZ4 by default.
- Compression does not affect the in-memory size of loaded content. LZMA AssetBundle compression is
  not available on WebGL (use LZ4).
- Uncompressed is not always fastest: loading uncompressed is limited by IO speed, LZ4 by IO or CPU
  depending on hardware. The page recommends profiling.

## Other Advanced Options
- **Include In Build**: include the group's assets in a content build. **Use Asset Bundle Cache**:
  cache remotely distributed bundles.
- **Bundle Naming Mode**: Filename (derived from the group name, no hash), Append Hash to Filename,
  Use Hash of AssetBundle, Use Hash of Filename.
- **Asset Bundle CRC**: Disabled, Enabled Including Cached, or Enabled Excluding Cached. The page
  calls Enabled Excluding Cached a good default for remote bundles; checking requires decompressing
  the whole bundle, which can hurt performance.
- **Include Addresses / GUIDs / Labels in Catalog**: disable any you do not load by, to shrink the
  catalog. GUID strings are required to access an asset with an AssetReference.
- **Internal Asset Naming Mode** (Full Path, Filename, GUID, Dynamic) and **Internal Bundle Id
  Mode** (Group Guid, Group Guid Project Id Hash, Group Guid Project Id Entries Hash): changing
  either changes CRC and Hash values, and the page warns not to modify them for content update
  builds because data in the content state file becomes invalid. Dynamic is recommended for release;
  Full Path during development.
- **Asset Load Mode**: Requested Asset and Dependencies (the default; the page recommends it for most
  cases) loads only what the requested assets need. All Packed Assets and Dependencies loads
  everything in the group on first load; the page says it can perform better for serialized data such
  as prefabs or ScriptableObjects, and on Nintendo Switch, while textures often load better
  individually. Profile for your content and platform.

## Checked
Date: 2026-11-07

Read in full: the Content Packing & Loading schema reference (Build and Load Paths, Advanced Options
table, AssetBundle compression, AssetBundle CRC and Asset Load Mode sections) and the Groups overview
page, which is only a table of links to sub-pages that were not opened. This rewrite is from those two
pages only.

Removed because neither page confirms it: Content Update Restriction, the claim that LZ4 is the
default for local bundles, the "1-10 MB" bundle-size heuristic, the shared-dependency/Analyze advice,
the scripting snippet (`CreateGroup`, `BundledAssetGroupSchema`), the scenes-in-separate-bundles
gotcha, the Bundle Mode rename/re-download gotcha, the built-in-scenes duplication gotcha and the
Build Layout / Event Viewer Verify steps.

Method: documentation only; no commands were run.
