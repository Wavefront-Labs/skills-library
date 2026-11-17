---
id: computing-software.game-programming.unity.prefab-instance-overrides
name: prefab-instance-overrides
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-prefabs, prefab, prefab-overrides, apply-overrides, revert-overrides, added-components, removed-components, property-modifications, game-programming]
status: docs-checked
level: intro
description: "Manage prefab instance overrides in Unity: what counts as an override, precedence, array override traps, and applying or reverting them."
sources: ["https://docs.unity3d.com/Manual/PrefabInstanceOverrides.html", "https://docs.unity3d.com/ScriptReference/PrefabUtility.GetObjectOverrides.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Prefab instance overrides

**Goal:** scene instances differ from their prefab only where intended, and changes go back to the prefab when they should.

## What counts as an override
Changing any of these on a prefab instance is an override: a property value, adding or removing a component, adding or removing a child GameObject.
- Inspector: a blue line on the left; added or removed components get a plus or minus badge on the icon; overridden property labels are bold.
- Hierarchy: added objects get a plus badge.
- Not overrides: a prefab instance's Position and Rotation (always differ from the asset). For a Rect Transform, Width, Height, Margins, Anchors and Pivot are not considered overrides.

## Precedence
An overridden value on an instance always wins over the prefab asset value, so editing the asset has no effect on instances that override that property. If instances do not update as expected, check for overrides. Many overrides are hard to track; the Manual suggests prefab variants for manageable variations.
If you modify or delete scripts that declare an override's value, the override becomes unused; the Overrides dropdown offers an option to remove unused overrides.

## Arrays, lists and dictionaries
An override on one entry is recorded at that entry's position. If the asset's collection later gains or loses entries, the override stays at the same position and may apply to a different entry (example from the Manual: int[] 10, 20, 30 with the second set to 99; after deleting 10 on the asset, 99 replaces 30 instead of 20). The Inspector shows dictionaries in sorted order, not storage order, so you cannot predict which entry is affected. After structural changes, especially deletions, review instances.

## Apply and revert
Select the instance, then Inspector > Override:
- Apply All / Revert All.
- Click an override (Ctrl or Command, or Shift, to multi-select) then Apply Selected / Revert Selected; a single override has Revert / Apply.
- Context menus: components via the More menu (Added, Removed or Modified Component > Revert or Apply); a property via right-click > Apply or Revert; an added GameObject via right-click in the Hierarchy > Added GameObject > Apply or Revert.
Targets vary by prefab type: with a nested prefab you can apply to the nested prefab asset or to the root prefab asset; with a variant, to the variant or the original prefab.

## Scripting
`PrefabUtility.GetObjectOverrides(GameObject prefabInstance, bool includeDefaultOverrides = false)` (UnityEditor, UnityEditor.CoreModule) returns a `List<ObjectOverride>` describing overrides on the instance. With includeDefaultOverrides true, components that contain only default overrides are also included.

## Verify
- [ ] Scene instances show only intended overrides.
- [ ] After editing a prefab default, non-overridden instances update.

## Checked
Date 2026-11-09. Read in full as fetched text: Override prefab instances (Manual) and PrefabUtility.GetObjectOverrides (script reference). Confirmed override kinds, indicators, precedence, transform exceptions, array behaviour, apply and revert routes, and the method signature and parameter.
Removed as unconfirmed: the colour claims (green plus, red minus), removed GameObject version note, the audit script (`IsOutermostPrefabInstanceRoot`, `GetAddedComponents`, `RevertPrefabInstance`), override-drift causes, and the Undo and `RecordPrefabInstancePropertyModifications` advice.
Method: documentation only; no commands were run.
