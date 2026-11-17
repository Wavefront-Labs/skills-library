---
id: computing-software.game-programming.unity.editor-undo-api
name: editor-undo-api
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, undo-recordobject, undo-groups, editor-tools, game-programming]
level: practitioner
status: docs-checked
description: "Make Unity editor tools undoable with the Undo API: RecordObject, RegisterCreatedObjectUndo, DestroyObjectImmediate, AddComponent, SetTransformParent, and undo grouping."
sources: ["https://docs.unity3d.com/ScriptReference/Undo.html", "https://docs.unity3d.com/ScriptReference/Undo.RecordObject.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undo in editor tools

**Goal:** register editor changes with the Undo system so they can be undone.

## Calls by operation (from the Undo class page)
| Operation | Call |
|---|---|
| Modify object properties | `Undo.RecordObject(myGameObject.transform, "Zero Transform Position");` then change the value |
| Add a component | `Undo.AddComponent<Rigidbody>(myGameObject);` |
| Create a GameObject | `var go = new GameObject(); Undo.RegisterCreatedObjectUndo(go, "Created go");` |
| Destroy a GameObject or component | `Undo.DestroyObjectImmediate(myGameObject);` |
| Change parent | `Undo.SetTransformParent(myGameObject.transform, newTransformParent, "Set new parent");` |

Other listed methods: `RecordObjects` (same as calling `RecordObject` multiple times),
`RegisterCompleteObjectUndo`, `RegisterFullObjectHierarchyUndo` (copies the states of a hierarchy),
`RegisterChildrenOrderUndo`, `RegisterImporterUndo`, `SetSiblingIndex`, `MoveGameObjectToScene` (the
GameObject must be at the root of its Scene).

## RecordObject
- Records any changes done on the object after the call. Almost all property changes can be recorded;
  transform parent, `AddComponent` and object destruction cannot, use the dedicated functions.
- Internally makes a temporary copy of the object's state; at the end of the frame Unity diffs the state
  and records changed properties. If nothing changed (binary exact comparison), nothing is stored.
- Prefab instances: `PrefabUtility.RecordPrefabInstancePropertyModifications` must be called after
  `RecordObject` (page marks this Important).
- Page example: in `OnSceneGUI`, after `EditorGUI.EndChangeCheck()` returns true, call
  `Undo.RecordObject(target, "Changed Area Of Effect")` then assign the value. The page notes
  `BeginChangeCheck`/`EndChangeCheck` is not required for `RecordObject`, which only registers changes
  made after the call.
- `FlushUndoRecordObjects` registers recorded objects as an undoable action; usually unnecessary since it
  is done automatically after mouse-up and certain other events.

## Grouping and callbacks
- The Undo system stores delta changes; operations store per property or per object state and scale well
  with Scene size.
- Operations combine automatically based on events (for example mouse down events split groups); a group
  appears and works as a single undo. Use `Undo.IncrementCurrentGroup` for manual grouping,
  `Undo.SetCurrentGroupName` to set the UI name (default is chosen by a hardcoded action ordering),
  `GetCurrentGroup`, and `CollapseUndoOperations` (collapses all operations down to a group index into
  one step).
- Callbacks: `undoRedoPerformed` (after an undo or redo), `undoRedoEvent`, `postprocessModifications`,
  `willFlushUndoRecord`; `isProcessing` is true while undo or redo is processing.

## Checked
Date: 2026-11-07

Read in full: the `Undo` class page and the `Undo.RecordObject` page including its example. The pages for
`CollapseUndoOperations`, `RegisterCreatedObjectUndo` and the other methods were not opened, so only
their one-line descriptions are used.

Removed because the pages do not confirm it: the Scatter Rocks group sample (including the exact call
order of `IncrementCurrentGroup`/`GetCurrentGroup`/`CollapseUndoOperations`), `PrefabUtility.InstantiatePrefab`,
`EditorUtility.SetDirty` and `AssetDatabase.SaveAssets` advice, "RecordObject marks the object dirty",
the claims that recording a GameObject does not record its components and that the full hierarchy call
is slow, and the Verify list. The page example records the Transform for transform changes but never
states a rule about components.

Method: documentation only; no commands were run.
