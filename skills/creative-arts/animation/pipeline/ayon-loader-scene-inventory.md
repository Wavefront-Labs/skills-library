---
id: creative-arts.animation.pipeline.ayon-loader-scene-inventory
name: ayon-loader-scene-inventory
category: creative-arts
field: animation
product: pipeline
tags: [ayon-loader, ayon, openpype, scene-inventory, containers, version-update, load-plugins, outdated-versions, asset-loading]
level: advanced
status: draft
description: "Load published products into DCC scenes with the Ayon Loader and manage them in Scene Inventory: containers, updating outdated versions, switching products."
sources:
  - https://ayon.ynput.io/docs/artist_tools_loader/
  - https://ayon.ynput.io/docs/artist_tools_inventory/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ayon Loader and Scene Inventory

**Goal:** scenes reference published versions (not random files), so the pipeline knows what each shot uses
and artists can update to newer versions safely.

## Loader

- Browse folders (assets/shots), products and versions; filter by product type.
- Right-click a version - load action provided by the DCC addon: Reference, Import, Load as GPU cache,
  Load Alembic, Load USD, etc. Actions depend on the product type and representation (e.g. `abc`, `usd`,
  `ma`, `exr`).
- Loading creates a **container**: a node/collection tagged with metadata (product, version, representation
  id) in the scene.

## Scene Inventory

Lists all containers in the open scene with their versions:
- Outdated versions are highlighted; **Update to latest** or **Set version** per container or in bulk.
- **Switch** to another product or representation (swap proxy for render geometry).
- Remove containers cleanly (removes references/imports it created).

## Practice

- Animation scenes load rigs by reference, never import, so rig fixes propagate by version update.
- Lighting loads animation caches and asset look products; a pre-render step checks for outdated containers.
- Locked shots: do not update containers without a supervisor's go-ahead; versions are part of what was
  approved.

## Gotchas

- Files brought in with File - Import bypass containers; the pipeline can't track or update them. Validators
  can flag untracked references.
- Updating a rig with changed controls can break animation curves; check rig change notes before bulk updates.
- Representation availability differs per version (an old version may lack USD); switch fails gracefully,
  check the result.

## Verify

Open Scene Inventory after loading: every loaded product shows the right version; bump a test asset version,
update, and confirm the scene content changed and the container records the new version.
