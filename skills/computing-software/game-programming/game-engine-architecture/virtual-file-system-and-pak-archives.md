---
id: computing-software.game-programming.game-engine-architecture.virtual-file-system-and-pak-archives
name: virtual-file-system-and-pak-archives
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, resource-manager, virtual-file-system, pak-archives, mount-points, patching, compression, async-io, file-ordering, game-programming]
level: advanced
status: draft
description: "Design a game virtual file system: mount points layered over pak archives, compressed block layout, patch overlay priority, async reads and file ordering for load times."
sources: ["https://www.gameenginebook.com/", "https://www.physfs.org/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-and-creating-chunks-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual file system and pak archives

**Goal:** game code opens `"textures/hero.tex"` the same way whether it is a loose file in
development, inside a compressed archive in shipping, or overridden by a patch or mod.

## Layers
```
Game code -> VFS path ("/game/textures/hero.tex")
   -> mount table (ordered by priority)
        patch_002.pak   (priority 30)
        patch_001.pak   (priority 20)
        base.pak        (priority 10)
        loose files dir (dev only, priority 100)
   -> archive reader (index lookup -> block reads -> decompress)
   -> platform async IO
```
Lookup: highest-priority mount containing the path wins. Patching = ship a small pak with changed
files at higher priority; mods use the same mechanism.

## Archive format essentials
- **Header + index**: path hash (e.g. 64-bit FNV/xxHash of normalised lowercase path) -> offset,
  compressed size, uncompressed size, flags. Store the index sorted for binary search or as a hash
  table; keep full paths only in debug builds or a separate table.
- **Block compression**: compress files in fixed blocks (64-256 KiB) so random access reads only the
  needed blocks; per-block offsets in the index. Codecs: Oodle Kraken/LZ4/Zstd; choose by
  decompression speed vs ratio for the platform.
- **Alignment** to the storage device's sector/page size for direct reads.
- Optional encryption of the index/data (AES) and signing to detect tampering.

## Load-time performance
- **File ordering**: write files into the archive in the order the game loads them (record an
  access log during a playthrough, feed it to the packer). Turns many seeks into sequential reads;
  vital on HDDs and optical media, still helps on SSD via larger reads.
- Bundle files always loaded together; avoid thousands of tiny reads.
- All reads asynchronous with priorities (streaming audio/textures > background prefetch).
- Decompress on worker threads or hardware decompressors (console IO APIs, DirectStorage GPU
  decompression).

## Dev workflow
Loose files mounted at highest priority in dev builds enable hot iteration; shipping builds refuse
loose-file overrides (or allow only a mods directory). Case sensitivity: normalise paths
(lowercase, forward slashes) at the VFS boundary so Windows-developed content works on case-sensitive
platforms.

## Engine examples
Unreal: `.pak` (and IoStore `.utoc/.ucas` containers), chunking via Primary Asset Labels, mount order
by `_P` suffix patch paks. Godot: `.pck` files loaded with `ProjectSettings.load_resource_pack()`
overlaying `res://`. PhysicsFS: C library providing exactly this mount/overlay model.

## Verify
- [ ] A patch pak overriding one file changes only that file at runtime.
- [ ] Load-time trace shows mostly sequential reads after file ordering.
- [ ] Path lookup of a missing file fails fast with a clear error including the normalised path.
