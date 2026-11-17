---
id: computing-software.game-programming.unity.missing-prefab-and-missing-script-recovery
name: missing-prefab-and-missing-script-recovery
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-prefabs, missing-prefab, missing-script, guid-recovery, game-programming]
level: practitioner
status: docs-checked
description: "Why Unity assets lose references: .meta files and asset IDs, moving assets outside the Editor, and removing missing-script components with GameObjectUtility."
sources: ["https://docs.unity3d.com/Manual/AssetMetadata.html", "https://docs.unity3d.com/ScriptReference/GameObjectUtility.RemoveMonoBehavioursWithMissingScript.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missing prefabs and missing scripts

**Goal:** understand why references break and how to clear missing-script components. Unity 6000.x docs.

## Why references break: .meta files
- On import Unity assigns the asset a unique ID, creates a `.meta` file, and processes the asset. The ID lets Unity move
  or rename an asset without breaking anything; the Import Activity window shows an asset's ID.
- A `.meta` file exists for each file and folder under `Assets`, next to the asset. It holds the unique ID and the asset's
  import settings, and is hidden in the Project window (and often by the OS).
- Moving or renaming an asset in the Project window moves or renames its `.meta` too. If you move or rename outside Unity,
  you must move or rename the `.meta` file to match.
- If an asset loses its `.meta`, references to it break: Unity generates a new `.meta` as if it were a new asset and
  deletes the old one. Consequences from the page:
  - a texture that loses its `.meta`: materials lose the texture and you must reassign it;
  - a script that loses its `.meta`: GameObjects and Prefabs that used it have an unassigned script component and lose
    functionality; you must reassign the script.
- Version control and empty folders: some systems cannot store empty folders. If Unity finds an empty folder with no
  `.meta`, it assumes another user deleted it and deletes the folder locally; if it finds a new `.meta` for a folder that
  does not exist locally, it creates the folder (with an unversioned meta file for empty folders).

## Removing missing-script components
```csharp
// public static int RemoveMonoBehavioursWithMissingScript(GameObject go)  (UnityEditor.GameObjectUtility)
int removed = GameObjectUtility.RemoveMonoBehavioursWithMissingScript(gameObject);
```
It removes the MonoBehaviours with a missing script from the given GameObject and returns how many were removed. See also
`GameObjectUtility.GetMonoBehavioursWithMissingScriptCount`. It handles one GameObject, so loop over children yourself.

## Checked
Date: 2026-11-07.
Read in full: "Asset metadata" manual page and the `GameObjectUtility.RemoveMonoBehavioursWithMissingScript` script
reference (6000.6 docs). The linked importing and asset workflow pages were not opened.
Removed as unconfirmed: the `{fileID, guid, type}` reference format and `guid:` field details, compile-failure and class
name versus file name causes, recovering the old GUID from git history, `Selection`/menu-item stripping sample,
`PrefabUtility.LoadPrefabContents` handling, "Missing Prefab" red instances, Unpack and Replace options, Force Text `grep`
search, `[MovedFrom]`, and the invented Verify checklist. The page does not cover missing prefab instances, so that part
of the draft's scope was dropped.
Method: documentation only; no commands were run.
