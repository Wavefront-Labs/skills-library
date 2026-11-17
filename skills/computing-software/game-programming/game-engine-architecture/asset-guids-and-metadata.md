---
id: computing-software.game-programming.game-engine-architecture.asset-guids-and-metadata
name: asset-guids-and-metadata
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, asset-guid, asset-metadata, asset-pipeline, game-programming]
level: practitioner
status: draft
description: "Identify assets by stable GUIDs instead of paths: sidecar meta files, rename-safe references, GUID collision on copy, and redirectors for moved assets."
sources: ["https://docs.unity3d.com/Manual/AssetMetadata.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-redirectors-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset GUIDs and metadata

**Goal:** references between assets survive renames and moves.

## GUIDs over paths
Each source asset gets a 128-bit GUID at creation; references store GUIDs; a database maps
GUID -> current path. Renaming changes only the database entry.

## Unity model
A `.meta` sidecar per asset holds `guid:` plus importer settings. References in scenes and prefabs
are `{fileID, guid, type}`. Consequences:
- Always commit `.meta` files with their assets and move them together (move inside the editor
  or move both files).
- Duplicating a file outside the editor duplicates the GUID; Unity detects the conflict and
  regenerates one, breaking references to whichever got the new GUID.
- Missing meta on another machine regenerates a new GUID and breaks references (the classic
  "missing script/material" after a merge).

## Unreal model
Assets are referenced by package path (`/Game/Characters/Hero.Hero`); moving creates a
**redirector** that points old path -> new. Fix up redirectors (Content Browser "Fix Up
Redirectors") before deleting them, or references break.

## Designing your own
- Sidecar or embedded header with GUID, importer id, importer version, settings.
- Reference resolution at build: GUID -> artifact id; runtime uses compact ids or hashes, not strings.
- Tools: "find references" (reverse index GUID -> referrers) to make deletes safe.
- Validation in CI: every referenced GUID exists; no duplicate GUIDs.

## Verify
- Rename and move an asset in a test project; every referencing asset still resolves.
- CI check fails on an orphaned reference.
