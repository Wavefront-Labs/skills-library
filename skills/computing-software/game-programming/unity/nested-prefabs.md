---
id: computing-software.game-programming.unity.nested-prefabs
name: nested-prefabs
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-prefabs, prefab, nested-prefabs, prefab-mode, composition, modular-prefabs, game-programming]
level: practitioner
status: docs-checked
description: "Add nested prefab instances to other prefabs in Unity, and edit prefab assets in Prefab Mode in isolation or in context, including editing environments and Auto Save."
sources: ["https://docs.unity3d.com/Manual/NestedPrefabs.html", "https://docs.unity3d.com/Manual/EditingInPrefabMode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested prefabs and Prefab Mode

**Goal:** compose larger prefabs from smaller prefab instances and edit them safely. Unity 6000.x docs.

## Nesting
Prefab instances included in other prefabs are nested prefabs. They keep their links to their own prefab assets while also
forming part of another prefab asset. Two ways to add one:
- **In prefab editing mode:** open the prefab, then drag another prefab into the Hierarchy or Scene view. You can add
  overrides to these instances.
- **From the Hierarchy:** select the dropdown arrow next to the prefab to edit, then drag a prefab from the Project window
  into its hierarchy.

The nested prefab is applied as an override on the parent prefab asset, shown with a green plus icon. You can optionally
apply the override permanently to the parent prefab asset (see "Apply overrides to the prefab asset").

## Opening Prefab Mode
Changes made in prefab editing mode affect all instances of that prefab.
- **In isolation:** hides the rest of the working scene and shows only the prefab's GameObjects in the Hierarchy. Open by
  double-clicking the asset in the Project window, or selecting it and choosing **Open** in the Inspector.
- **In context:** the rest of the scene stays visible but locked. Open by selecting an instance in the Hierarchy and
  choosing Open in the Inspector, pressing P (default binding), or selecting the arrow next to the instance.
- Default: Open from the Inspector opens in context; hold Alt (macOS: Option) to open in isolation. To change the default,
  Edit > Preferences (macOS: Unity > Settings) > General > Hierarchy window > Default Prefab Mode.
- A breadcrumb bar at the top of the Scene view (and a header bar in the Hierarchy with a back arrow) shows the open
  prefab and navigates back.

## In isolation vs in context
- Isolation shows the default skybox unless you set an editing environment: Edit > Project Settings > Editor > Prefab Mode >
  Editing Environments, one scene for regular prefabs and one for UI prefabs (root has a Rect Transform).
- In context, the Context option is Normal, Gray (default) or Hidden. Other scene objects cannot be selected. Unless the
  context is Hidden you can still snap prefab GameObjects to the scene.
- In context the contents show at the position of the instance you opened, so the root transform preview can differ from
  the asset's values. You cannot edit Transform values in context; open in isolation to do that. **Show Overrides** in the
  Scene view top bar visualizes overrides on the main prefab asset.

## Auto Save
Toggle **Auto Save** at the top right of the Scene view; disable it if editing a complex prefab is slow, and Unity asks
whether to save when you exit. To remove the option, disable Allow Auto Save under Project Settings > Editor > Prefab Mode.

## Checked
Date: 2026-11-07.
Read in full: "Nest prefab instances in other prefabs" and "Edit prefab assets" manual pages (6000.6 docs). The linked
"Apply overrides to the prefab asset", "Create variations of prefabs" and "Override prefab instances" pages were not opened.
Removed as unconfirmed: the Wheel/Car/Truck override-ownership walkthrough, the "Apply as Override in Prefab" versus
"Apply to Prefab" menu wording, claims that nested inner prefabs edit when opened from a parent, design guidance (small
blocks, avoiding overrides), `Unpack` and `Unpack Completely` behavior, scene merge-conflict and UnityYAMLMerge advice,
Missing Prefab placeholders and `PrefabUtility.IsPrefabAssetMissing`, and the invented Verify checklist.
Method: documentation only; no commands were run.
