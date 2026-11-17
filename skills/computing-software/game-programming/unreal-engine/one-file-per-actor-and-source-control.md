---
id: computing-software.game-programming.unreal-engine.one-file-per-actor-and-source-control
name: one-file-per-actor-and-source-control
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ofpa, one-file-per-actor, world-partition, source-control, game-programming]
level: practitioner
status: draft
description: "Work with Unreal One File Per Actor: external actor files, hashed paths, finding which actor a file holds, changelists, deleted actors and multi-user editing."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/source-control-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# One File Per Actor and source control

**Goal:** many people edit one level at once without lock contention or lost work.

## How OFPA works
With World Partition (or Use External Actors on a level), each actor is saved to its own `.uasset`
under `Content/__ExternalActors__/<MapPath>/<hash dirs>/<GUID>.uasset`; the map file holds level
settings only. Folders are external too (`__ExternalObjects__`). Locking one actor locks one small file.

## Workflow
- Use the editor's source control integration (Perforce recommended, Git with LFS locking possible):
  **View Changes** / Changelists window shows actors by their **label** rather than GUID filenames.
- Submit from the editor or use "Submit Content" so the right external files and the map are grouped.
- Find which actor a file is: in the Changelists window, or `Tools > Find Actor by file`; in Perforce
  the file's description is unreadable, so always submit through the editor or keep labels in commit
  messages.
- Deleted actors are file deletions; ensure deletions are submitted, or actors resurrect.
- Moving an actor between data layers or cells changes only its file.

## Converting
Existing level: World Settings > Use External Actors, or World Partition convert commandlet
(`-run=WorldPartitionConvertCommandlet`). Converts actors to files; review the large changelist.

## Gotchas
- Command-line tools that grep map files no longer see actors; use asset registry queries.
- Rename/move the map: external actor folders move with it; do it in the editor, not in Explorer.
- Git without locking leads to unmergeable binary conflicts on the same actor; enable LFS locks.
- Actors referenced by Level Blueprint keep the level file involved in edits; minimise Level Blueprint
  logic in shared maps.

## Verify
- [ ] Two developers edit different actors in the same map and submit without conflicts.
- [ ] Changelist view shows actor labels; no orphaned external actor files after deletions.
