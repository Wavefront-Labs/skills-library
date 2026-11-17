---
id: computing-software.game-programming.game-engine-architecture.asset-pipeline-and-streaming
name: asset-pipeline-and-streaming
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, asset-pipeline, cooking, asset-import, dependency-graph, streaming, asset-bundle, guid, content-addressing, hot-reload, reference-counting, asset-manager, virtual-texturing, game-programming]
level: advanced
status: draft
description: "Design an engine's asset pipeline: importing/cooking to a runtime format, tracking dependencies by stable ID, and streaming content in and out under a memory budget."
sources: ["https://www.gamedeveloper.com/programming/game-engine-architecture", "https://docs.unrealengine.com/en-US/world-partition-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset pipeline and streaming architecture

**Goal:** the plumbing underneath every engine's "drag a texture into the
scene" — import/cook source assets into a fast-to-load runtime format, track
what depends on what with a stable identity, and load/unload content on demand
without stalling the frame or running out of memory.

## Import vs cook — two different transforms
- **Import**: source format (a `.png`, `.fbx`, `.wav`) → an engine-native
  in-memory/on-disk representation, done once and cached (re-run only when the
  source file's hash/timestamp changes). This is where you decide texture
  compression format, mesh LOD generation, audio compression — expensive, so
  cache aggressively and invalidate by content hash, not just timestamp (a
  file touched without content change shouldn't force a re-import).
- **Cook** (console/shipping terminology): the imported assets → a
  platform-specific packaged format (byte order, compression, platform texture
  format) ready to stream directly into memory with minimal runtime
  transformation. Cooking is what makes "works in editor, won't load on
  console" bugs show up — the cooked format and the editor's in-memory format
  are not the same thing, and a cook-time-only code path (stripped debug data,
  different serialization) is where those bugs hide.

## Dependency tracking needs a stable ID, not a path
A material references textures; a level references meshes referencing
materials. If assets are tracked by **file path**, renaming or moving a file
silently breaks everything referencing it with no error until runtime (a
missing/pink-texture bug far from the actual rename). The standard fix: assign
every asset a **stable GUID at creation time**, independent of its file path,
stored as metadata alongside the source file; all references serialize the
GUID, and a path is resolved by looking the GUID up in an asset registry/
database rebuilt by scanning for that metadata. This is why Unity's `.meta`
files and Unreal's embedded asset GUIDs exist — losing/regenerating that
metadata (checking `.meta` files out of version control, copy-pasting an asset
folder outside the engine) is the single most common cause of "every reference
in this project just broke."

## Streaming under a memory budget
Loading an entire open world's assets at once doesn't fit in memory; the
pipeline must load what's near the player and unload what isn't, continuously,
without a visible stall:
- **Reference counting**: an asset stays loaded exactly as long as something
  needs it (a streamed-in region, an active instance); drops to zero → eligible
  for unload, usually on a delay/LRU basis rather than instantly (avoids
  thrash when something unloads and immediately reloads, e.g. the player
  walking back and forth across a streaming boundary).
- **Priority and budget**: when more content wants to be resident than the
  memory budget allows, a priority score (distance, visibility, "will be
  needed in N seconds based on velocity") decides what loads first and what
  gets evicted — a flat "load everything within radius X" starves the
  budget the moment X is tuned for the wrong platform.
- **Streaming granularity**: too coarse (whole-level chunks) means visible
  pop-in/stalls at boundaries; too fine (per-asset) means tracking overhead
  dominates. Engines converge on mid-size cells/tiles (Unreal's World
  Partition grid, a custom chunk grid) as the sweet spot, with a **virtual
  texturing** layer for cases even a cell is too coarse (streaming texture
  mip levels independently of the whole texture).
- **Async, always**: any load triggered by gameplay (not a loading screen)
  must be async with a placeholder/LOD-0 fallback shown immediately — a
  synchronous load on the main thread during open-world traversal is a hitch,
  full stop, regardless of how "fast" the asset is.

## Verify
- [ ] Assets are referenced by stable ID (GUID/handle), never by raw file path,
      verified by renaming/moving a referenced asset and confirming nothing breaks.
- [ ] A cooked/packaged build is tested on-device, not assumed equivalent to the
      editor's in-memory representation.
- [ ] Reference counts return to the expected baseline after streaming out of an
      area — checked by walking away and confirming memory drops, not just that
      visuals disappeared.
- [ ] No gameplay-triggered load blocks the main thread; verified by profiling a
      frame during a traversal-triggered load spike.
