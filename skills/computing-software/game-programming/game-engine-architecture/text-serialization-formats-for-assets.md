---
id: computing-software.game-programming.game-engine-architecture.text-serialization-formats-for-assets
name: text-serialization-formats-for-assets
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, text-serialization, json, yaml, game-programming]
level: practitioner
status: draft
description: "Choose and implement text formats for assets: JSON, YAML and custom formats for mergeability, stable key ordering, schema versioning and fast parsing."
sources: ["https://docs.unity3d.com/Manual/FormatDescription.html", "https://github.com/simdjson/simdjson"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text formats for assets

**Goal:** source assets that diff and merge in version control, then compile to binary for runtime.

## Why text for source data
Merge conflicts in binary scenes are unresolvable. Unity's "Force Text" serialisation writes
scenes/prefabs as a YAML subset; Godot `.tscn`/`.tres` are text; Unreal assets are binary (hence
their exclusive checkout workflow).

## Design rules for mergeable text
- **Stable ordering:** write keys and lists in a deterministic order (sorted, or creation-ordered
  by stable id); never hash-map iteration order.
- **One item per line** where possible and stable ids per object, so merges are line-local.
- **Omit defaults** to shrink diffs (but version the defaults).
- **Avoid volatile data** (timestamps, editor camera position) in shared files, or put it in a
  per-user file.
- **Floats:** round-trip exactly (shortest repr, `std::to_chars`), otherwise re-saving changes values.

## Format choice
- **JSON:** universal tooling, strict; no comments (JSON5/JSONC add them). Fast parsers: simdjson,
  RapidJSON, yyjson.
- **YAML:** comments and anchors; slow, complex spec, ambiguous scalars ("no" as bool in YAML 1.1).
  Restrict to a subset.
- **TOML:** good for configs, poor for deep hierarchies.
- **Custom (Godot tscn-like):** section headers with properties; easy to merge and parse.

## Versioning
Include `version` per file; loaders upgrade old versions step by step (v1->v2->v3 migrations), and
editors re-save in the latest version.

## Runtime
Compile text to binary at build time; loading JSON at runtime for large data costs startup time
and memory.

## Verify
- Load and save with no changes: byte-identical file (idempotent save).
- Two people edit different objects in the same scene; git merges automatically.
