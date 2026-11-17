---
id: creative-arts.animation.pipeline.asset-variants-and-lods
name: asset-variants-and-lods
category: creative-arts
field: animation
product: pipeline
tags: [asset-variants, lod, levels-of-detail, variants, proxies, usd-purpose, asset-management]
level: practitioner
status: draft
description: "Manage asset variants and levels of detail: when a variation is a variant, LOD or proxy, naming, shared rig and topology rules, USD variant sets and purposes, tracking."
sources:
  - https://openusd.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Asset variants and LODs

One asset often needs several forms. Keep the decision clear: what changes, and what must stay shared.

## Definitions
- **Variant**: an alternate version of the same asset for story reasons: clean and damaged, summer and winter, costume A and B, colour variations. Variants share identity and usually the rig.
- **LOD (level of detail)**: the same asset at lower geometric or texture detail for distance, speed or real-time use. LOD0 is the highest.
- **Proxy**: a lightweight stand-in for viewport or layout; the heavy **render** version loads at render time.

## Rules
1. **Shared base**: variants share skeleton, UV layout where possible and naming, so animation transfers and textures are swappable. If topology changes, treat it as a new asset or a new rig version.
2. **Naming**: encode variant and LOD in the name consistently, for example `hero_clean`, `hero_damaged`, `hero_LOD0`, `hero_LOD1`. Never ad hoc suffixes.
3. **One asset record** in the tracker (`production-tracking.md`) with variant children, so approvals and versions are traceable per variant.
4. **LOD thresholds** (real-time or crowd): choose screen-size or distance switch points by testing; reduction to roughly half the triangles per level is a common start. Keep silhouettes stable across LODs.
5. **Textures**: lower LODs can share an atlas or use lower resolution; keep the same UV layout so materials do not change.

## In USD
- **Variant sets** carry alternatives inside one asset file (`usd-variant-sets.md`).
- **Purpose** (`default`, `render`, `proxy`, `guide`) tags geometry for viewports vs final render, which is the USD way to hold a proxy and hero version together (`usd-composition-arcs.md`).

## Alembic / FBX pipelines
- Publish each variant as its own file with a variant tag, and record which variant a shot uses in the shot's asset list (`alembic-caches.md`).

## Verify
- [ ] Names follow the convention; variants load in the same rig.
- [ ] Shot records state the variant used.
- [ ] LOD switch points tested in context.
