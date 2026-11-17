---
id: computing-software.game-programming.unity.prefab-mode-in-context-editing
name: prefab-mode-in-context-editing
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-prefabs, prefab-mode-in-context, prefab-isolation, prefab-stage, game-programming]
status: docs-checked
level: practitioner
description: "Edit Unity prefabs in Prefab Mode in context vs isolation: how to open each, context display, editing environments, Auto Save and PrefabStageUtility."
sources: ["https://docs.unity3d.com/Manual/EditingInPrefabMode.html", "https://docs.unity3d.com/ScriptReference/SceneManagement.PrefabStageUtility.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prefab Mode in context and isolation

**Goal:** change the prefab asset (affecting all instances) while choosing whether to see the surrounding scene.

## Open
- In isolation (rest of scene hidden): double-click the prefab asset in the Project window, or select it and choose Open in the Inspector.
- In context (rest of scene visible but locked): select an instance in the Hierarchy and choose Open in the Inspector, press P (default binding), or use the arrow next to the instance.
- Opening from an instance's Inspector Open button is in context by default; hold Alt (macOS: Option) when selecting Open to use isolation. Change the default under Edit > Preferences (macOS: Unity > Settings) > General > Hierarchy window > Default Prefab Mode.
- A breadcrumb bar at the top of the Scene view names the open prefab and navigates back; the Hierarchy header has a back arrow.

## Isolation environment
In isolation the default is the default skybox. Assign scenes under Edit > Project Settings > Editor > Prefab Mode > Editing Environments (one for regular prefabs, one for UI prefabs, i.e. root has a Rect Transform). Used only in isolation.

## In context
Context options in the Scene view bar: Normal, Gray (default) or Hidden. You cannot select other scene objects. Unless Context is Hidden, snapping to the scene still works. Contents appear at the position of the instance used to open it, so the root transform preview can differ from the asset. You cannot edit Transform values in context; open in isolation for that. The Show Overrides setting in the Scene view bar visualises overrides on the main prefab asset.

## Auto Save
Auto Save (top right of the Scene view) saves edits automatically; disable it if a complex prefab is slow, and Unity then asks whether to save on exit. To remove the option entirely: Project Settings > Editor > Prefab Mode, disable Allow Auto Save.

## Scripting
`UnityEditor.SceneManagement.PrefabStageUtility` has static methods `GetCurrentPrefabStage` (null if none), `GetPrefabStage` (stage containing a given GameObject) and `OpenPrefab` (opens a prefab asset in Prefab Mode).

## Verify
- [ ] The edit appears on every non-overriding instance.

## Checked
Date 2026-11-09. Read in full as fetched text: Edit prefab assets (Manual) and PrefabStageUtility (script reference). Confirmed all open routes, settings paths, context options, Auto Save and the three methods.
Removed as unconfirmed: the stage script sample (`prefabContentsRoot`, `prefabStageOpened`, `SetDirty`), the `FindObjectsByType` stage-scene note, the OnValidate and ExecuteAlways gotcha, environment lighting claim and the git diff check.
Method: documentation only; no commands were run.
