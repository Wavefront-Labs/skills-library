---
id: creative-arts.animation.pipeline.asset-management
name: asset-management
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, asset-management, blend, versioning, naming, locked-asset, manifest, registry, dependency, re-render, consistency, library-link, dependency-tracking]
level: advanced
status: draft
description: "Manage locked .blend assets at scale: naming, versioning, the lock-and-reuse law, a manifest/registry, dependency tracking, safe updates and re-render impact."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Asset management (locked .blend assets at scale)

**Goal:** keep every character, set and prop across 10 episodes identical,
findable, versioned and safe to update — so the data-driven renderer
(`shot-renderer`) can resolve any asset by name and a character looks the same in
EP01 and EP10. This is the operational backbone of `character-consistency`: that
skill states the *law* (reuse the locked modeled asset, never re-generate);
this skill is the *system* that enforces it at the scale of hundreds of assets.

## The lock-and-reuse law (why this exists)

The show's consistency doesn't come from a style guide — it comes from
**rendering the same modeled assets every time.** A character is not re-modeled,
re-sculpted or AI-regenerated per episode; the one locked `.blend` is linked into
every shot. Therefore the entire job of asset management is:
1. there is exactly **one canonical, locked version** of each asset at any time,
2. everyone/every tool can **find it unambiguously**, and
3. changing it is **deliberate, tracked, and impact-assessed** — because a change
   silently restyles every shot that uses it.

## WIP vs published, and who may touch what

Two zones, one gate. Artists iterate freely in a **WIP** area; nothing there is
canonical and nothing links to it. **Publishing** is the single act that makes a
version real: it copies the WIP to an immutable `v<NNN>` in the published tree and
writes a registry row. Only the registry's `current` pointer — never the file
system, never "the newest export" — decides what a shot gets. That one rule
prevents the classic disaster: a work-in-progress save silently restyling the
whole show because a tool grabbed the latest file. Publish is deliberate,
reviewed, and recorded; everything else is sandbox.

## Naming (the primary key)

Names are the API between assets and the renderer. Lock a scheme and never
deviate:

```
<type>_<name>_v<NNN>.blend
char_dill_v004.blend
set_alley_v002.blend
prop_mug_v001.blend
```

- `type`: `char` | `set` | `prop` | `fx` | `comp` (node-group libs).
- `name`: lowercase-kebab, matches the renderer's `CHAR_MAP`/`SET_MAP` key exactly.
- `v<NNN>`: zero-padded integer, monotonic, never reused.
- **Inside the file**, the datablock (Collection/Object) has a *stable* name with
  **no version** (`char_dill`), because shots **link** that datablock by name —
  the version lives in the filename, not the linked name, so bumping a version
  doesn't break every link. (This is the crucial trick: filename carries the
  version for humans/registry; the internal collection name is version-free so
  `library.filepath` is the only thing that changes on an update.)

## Versioning: WIP vs published

- **WIP** lives in an artist working area and iterates freely.
- **Publish** = promote a WIP to a new immutable `v<NNN>` in the published asset
  tree. **Published versions are never edited in place** — a change is always a
  new version. Immutability is what lets you re-render EP01 next year and get the
  same frame.
- The published version a shot used is recorded (see manifest) so a shot is
  reproducible even after the asset moves forward.

## The manifest / registry (single source of truth)

A machine-readable registry — one JSON (or JSONL) the renderer and tracker both
read. One row per asset version:

```json
{
  "id": "char_dill",
  "type": "char",
  "current": "v004",
  "versions": {
    "v004": {
      "path": "<REPO>/assets/char/char_dill_v004.blend",
      "collection": "char_dill",
      "sha256": "…",
      "published": "2026-09-30",
      "author": "cam",
      "status": "locked",
      "depends_on": ["prop_mug", "comp_cel_core"],
      "notes": "added screen-face emissive AOV outputs"
    }
  }
}
```

- `current` is what the renderer resolves by default; a shot may pin an older
  version for reproducibility.
- `sha256` detects silent corruption / accidental edits to a "locked" file.
- `status`: `wip` | `review` | `locked` | `retired`.
- `depends_on` makes the dependency graph queryable (next section).
- The registry is the **only** place `current` is decided — not "the newest file
  in the folder." A stray `_v005` in the directory must not auto-promote.

Keep this registry versioned in git with the repo. It is small, text, diffable —
the audit trail of the whole show's look.

## Dependency tracking

Assets reference each other via Blender's **library linking** (`File ▸ Link`),
not appending — link keeps one shared source, append copies (and fragments the
truth). Track the graph so you know blast radius before touching anything:

- A **set** links props; a **shot** links sets + characters; **characters** link a
  shared `comp_cel_core` node group and shared rigs/materials.
- `depends_on` in the registry mirrors the link graph. A simple script walks
  `bpy.data.libraries` of each `.blend` to *verify* the declared deps match the
  actual links (drift here is a real bug source).
- **Who uses this asset?** Reverse the graph: before changing `comp_cel_core`,
  query every asset whose `depends_on` includes it — that's the re-render set.

## Safe updates (impact before edit)

Updating a locked asset restyles every shot using it. The procedure:

1. **Branch the version:** new `v<NNN>`, never edit the locked file.
2. **Compute blast radius:** registry reverse-lookup → list of assets → list of
   **shots** (from the shot tracker, `production-tracking`) that use it. A mug
   tweak might touch 12 shots; a `comp_cel_core` tweak touches the whole series.
3. **Review on a representative shot** before promoting — render one WIDE and one
   CLOSE that use the asset and compare to the locked version. Catch regressions
   (a changed pivot, a broken AOV name, a shifted material) here.
4. **Promote** to `locked`, bump `current`, log the re-render set.
5. **Re-render** only the impacted shots and re-run comp (passes/cryptomatte may
   depend on the asset name — see `multipass-compositing`). Mark those shots
   `needs-rerender` in the tracker until done.
6. **Never bump `current` without scheduling the re-render** — a half-updated
   series (new asset, old renders) is the worst state: inconsistent and invisible
   until someone spots it on the cut.

## Directory layout

A flat, predictable tree the registry paths point into — browsable by a human,
resolvable by a tool:

```
<REPO>/assets/
  char/   char_dill_v004.blend   char_vera_v002.blend   …
  set/    set_alley_v002.blend   set_catwalk_v001.blend …
  prop/   prop_mug_v001.blend    …
  fx/     fx_seam_v003.blend     …
  comp/   comp_cel_core_v002.blend   (shared node groups)
  tex/    (linked texture library, relative paths)
  registry.json
```

- One type per folder; version in the filename; the registry is the index over
  it. No per-episode asset copies — an asset belongs to the *show*, linked into
  episodes, never duplicated into them.
- Shared material/node libraries (`comp_cel_core`, rigs) live in `comp/` and are
  the highest-fan-out assets — treat a change there as a series-wide event.
- Textures live once in `tex/` and are **linked with relative paths** so the whole
  `assets/` tree relocates without re-pointing every material.

## Retirement (not deletion)

An asset version is never deleted — it's **retired**: `status: retired`, kept on
disk and in the registry. Shots that pinned it stay reproducible; new shots
resolve `current`. Deleting a version breaks the reproducibility guarantee that
is the entire point of the system. Prune only truly unused WIP, never a published
`v<NNN>` any shot ever rendered against. If disk is the constraint, archive
retired versions (compress/cold-store) but keep the registry row and `sha256`.

## Gotchas

- **Append instead of link** forks the asset — now two "canonical" copies drift.
  Always link.
- **Renaming the internal collection** breaks every shot's link (and every
  cryptomatte pick that stored that name). Rename the *file*, never the linked
  datablock; if you must, keep the old name as the stable one.
- **"Newest file wins"** auto-promotion — a stray WIP export silently restyles the
  show. Only the registry's `current` is canonical.
- **Packed vs linked textures** — decide one policy (linked texture library with
  relative paths, or packed) and hold it, or a moved file renders untextured.
- **Editing a locked file in place** destroys reproducibility; the sha256 check
  exists to catch exactly this.
- **Bumping a version without the re-render set** leaves orphan old frames —
  always pair a version bump with a tracker `needs-rerender` sweep.

## Verify

1. Resolve a character by its `CHAR_MAP` name through the registry: you get one
   unambiguous locked `v<NNN>` path, and its `sha256` matches the file on disk.
2. Pick a shared asset (`comp_cel_core`) and run the reverse dependency query:
   it returns the full list of dependent assets/shots — cross-check against the
   actual links reported by `bpy.data.libraries` and they match.
3. Open a published-locked `.blend`, confirm its internal collection name has no
   version suffix (so links survive a version bump).
4. Simulate an update: branch to a new version, change it, render one shot, and
   confirm the tracker marks exactly the blast-radius shots `needs-rerender` — no
   more, no fewer.
5. Attempt to open a shot whose asset version was retired: the registry still
   records the pinned version path so the shot is reproducible (or flags the pin
   as retired), rather than silently grabbing `current`.
