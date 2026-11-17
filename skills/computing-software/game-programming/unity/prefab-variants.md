---
id: computing-software.game-programming.unity.prefab-variants
name: prefab-variants
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-prefabs, prefab, prefab-variants, base-prefab, inheritance, enemy-variants, prefab-workflow, game-programming]
status: docs-checked
level: practitioner
description: "Use Unity prefab variants to build families of objects (enemy types): create them, inspect inheritance, and read or revert variant overrides."
sources: ["https://docs.unity3d.com/Manual/PrefabVariants.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Prefab variants

**Goal:** many related prefabs (for example enemy types) that share a base, with per-variant differences kept as overrides.

## What a variant is
A prefab variant inherits properties from a base prefab. Overrides in the variant take precedence over the base values. A variant can use any prefab as its base, including other variants. In the Editor a variant has a blue cube icon with one hashed side.

## Create
- Project window: right-click the prefab > Create > Prefab Variant. The variant is created in the same folder as the original.
- Hierarchy: drag a prefab instance into a Project folder. Unity asks whether to create a new prefab or a prefab variant; choosing Prefab Variant applies the instance's overrides to the new variant.

## Inspect the hierarchy
Selecting a variant shows its parent prefab in the Inspector. The menu button shows the root prefab asset, any child variants and the number of overrides the variant has.

## Edit
Opening a variant in prefab editing mode shows its root as a prefab instance representing the base. Every edit is applied as an override (property values, added or removed components, added or removed child GameObjects).
To list them: open the variant in prefab editing mode, select the root prefab instance, then in the Inspector under Prefabs open the Overrides dropdown. Revert All resets the variant's changes; Apply all to Prefab Variant parent pushes them to the parent prefab asset (take care: that changes the base).

## Verify
- [ ] Each variant's Overrides list holds only intended differences.
- [ ] Nothing was applied to the parent prefab by accident.

## Checked
Date 2026-11-09. Read in full as fetched text: Create variations of prefabs (docs.unity3d.com/Manual/PrefabVariants.html). Confirmed creation routes, inheritance display, override listing and Revert All / Apply all behaviour.
Removed as unconfirmed: the base-versus-variant table, chain depth advice, claims that a variant cannot remove inherited children or removed-component version notes, FormerlySerializedAs advice, the `m_IsActive` trick, propagation of base changes and the `GetPropertyModifications` script.
Method: documentation only; no commands were run.
