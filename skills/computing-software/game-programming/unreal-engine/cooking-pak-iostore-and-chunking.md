---
id: computing-software.game-programming.unreal-engine.cooking-pak-iostore-and-chunking
name: cooking-pak-iostore-and-chunking
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-packaging, pak-files, iostore, chunking, primary-asset-labels, zen-loader, game-programming, chunk-id]
level: advanced
status: docs-checked
description: "Assign Unreal assets to chunks with Primary Asset Rules or Labels, audit with Asset Audit, and understand Zen Loader .utoc/.ucas containers and UnrealPak inspection."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-and-creating-chunks-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/zen-loader-in-unreal-engine"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cooking, pak/IoStore containers and chunking

**Goal:** split cooked content into independently distributable chunks and know what ended up where.

## Chunks (Cooking and Chunking page)
- A chunk is a numbered collection of assets known to the asset management system. Assign via the Asset Manager (primary
  asset rules) or Primary Asset Labels; both feed the cook. On cook each chunk generates a `.pak`.
- Primary assets are manipulated directly by the Asset Manager; secondary assets referenced by a primary asset are chunked
  alongside it when it has authority over them. Rules are `FPrimaryAssetRules` (see its API page, not read).
- Chunk 0 is the default, distributed with base data; assets with no chunk ID or a negative one go to chunk 0. IDs above 0
  become separate `.pak` files. Example: ShooterGame has chunk 1 ("Sanctuary" map), chunk 2 ("Highrise"), chunk 0 for the rest.
- Define via Project Settings > Game > Asset Manager (Primary Asset Types to Scan; rules list with Priority and Chunk ID),
  via `DefaultGame.ini` `[/Script/Engine.AssetManagerSettings]` `+PrimaryAssetRules=(PrimaryAssetId="Map:/Game/Maps/X",
  Rules=(Priority=-1,ChunkId=1,CookRule=Unknown))` (page: Priority -1 sets the default, which is 1; the startup map entry
  uses `ChunkId=0,CookRule=AlwaysCook`), or via a Primary Asset Label.
- Primary Asset Label: Content Browser right-click > Miscellaneous > Data Asset > `PrimaryAssetLabel`. It has Chunk ID and
  Priority; Explicit Assets (or an Asset Collection), or tick Label Assets in My Directory to cover the folder.
- Output: `Saved/StagedBuilds/[Platform]/[Project]/Content/Paks`. Paks are per platform, not interchangeable.
- Audit: Windows menu > Developer Tools > Asset Audit, Add Chunks, then right-click a chunk for Size Map or Reference
  Viewer. Size Map shows asset sizes (nested box = referenced child; Memory Size mode is editor memory, which can differ a
  lot from shipped disk size). Reference Viewer shows why an asset is tied to a chunk.

## Zen Loader and containers (Zen Loader page)
- Zen Loader is UE5's runtime loader. It packages package data, bulk data and shaders into `.utoc` and `.ucas` containers
  instead of `.pak`; `.pak` files hold loose, less-used files, and mounting a pak mounts its container. `.utoc` describes
  the container (chunk size/offset, compression, encryption); `.ucas` holds the data. An I/O dispatcher loads by chunk ID.
- Containers are produced by default during UAT staging and their presence activates Zen Loader. The Event Driven Loader is
  deprecated; stage with `-SkipIoStore` or set `bUseIoStore=False` under `[/Script/UnrealEd.ProjectPackagingSettings]`.
- Limits: data cannot be looked up by directory through normal file APIs; Bulkdata cannot load inline data after initial
  serialization (store frequently needed data non-inline at cook time); core redirects and delegate resolvers are ignored.
- UnrealPak container commands: `-list`, `-diff`, `-extract`, and `IoStore -describe` (takes the `global.ucas` path,
  `-DumpToFile=`, `-CryptoKeys=`).
- Debugging: `-LogCmds="LogStreaming veryverbose"`, filter with `-s.VerbosePackageNames`, `-s.DebugPackageNames` with a
  debugger. Zen Store is described as experimental.

## Checked
Date: 2026-11-07. Read in full: Cooking and Chunking page and Zen Loader page (all sections), unversioned en-us pages. Image
captions are text only; screenshots were not viewed. The third source (Creating a Patch) returns empty text and was dropped.
The ini sample on the page spells one `Priority` as `Prority` (typo); not copied.
Removed as not on those pages: "UE5 default" and Project Settings > Packaging > Use Io Store, Oodle default, Crypto settings,
the "Generate Chunks" checkbox, the `pakchunk0-Windows.pak` naming, highest-priority-wins rule for multiply-referenced assets,
Tools > Audit menu path (page says Windows > Developer Tools), all patching steps (`-createreleaseversion`,
`-basedonreleaseversion`, `_P` suffix), `UnrealPak -List/-Extract` syntax forms, `-ListContainer`, cook flags and the Verify
checklist.
Method: documentation only; no commands were run.
