---
id: computing-software.game-programming.unity.assetdatabase-batch-asset-editing
name: assetdatabase-batch-asset-editing
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, assetdatabase, batch-asset-edit, startassetediting, findassets, editor-tools, game-programming]
level: practitioner
status: docs-checked
description: "Script Unity's AssetDatabase for batch edits: FindAssets filter syntax, StartAssetEditing and StopAssetEditing batching, AssetEditingScope, and which calls suit batching."
sources: ["https://docs.unity3d.com/ScriptReference/AssetDatabase.html", "https://docs.unity3d.com/ScriptReference/AssetDatabase.FindAssets.html", "https://docs.unity3d.com/ScriptReference/AssetDatabase.StartAssetEditing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AssetDatabase scripting and batch asset edits

**Goal:** change many assets from Editor code without the Asset Database importing after every step.

## Batching with StartAssetEditing
- `AssetDatabase.StartAssetEditing` places the Asset Database in a state that prevents imports until
  `AssetDatabase.StopAssetEditing` is called. If an exception occurs between the two calls the Asset
  Database is unresponsive, so always put the pair inside try-catch or try-finally.
- While automatic importing is paused some `AssetDatabase` APIs will not work as expected, because assets
  created during the pause are not fully created before `StopAssetEditing`. Limit batches to operations
  that do not need the assets fully imported. The supported and recommended batch methods are
  `ImportAsset`, `MoveAsset`, `CopyAsset` and `AddObjectToAsset`.
- Calls nest and are counted: `StartAssetEditing` increments, `StopAssetEditing` decrements. The totals
  must be equal for automatic import to resume. More Starts than Stops: import does not resume. More
  Stops than Starts: an error.
- Alternative: `AssetDatabase.AssetEditingScope` in a `using` statement (that class page was not opened).

```csharp
string[] guids = AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/Art" });
try {
    AssetDatabase.StartAssetEditing();
    foreach (string guid in guids) {
        string path = AssetDatabase.GUIDToAssetPath(guid);
        AssetDatabase.ImportAsset(path);   // a recommended batch method
    }
} finally {
    AssetDatabase.StopAssetEditing();
}
```

## FindAssets filter syntax
`FindAssets(string filter, string[] searchInFolders)` returns an array of GUID strings (empty array if
none match). Folders are searched with their child folders; if unspecified it searches `Assets` and
`Packages`. Restricting folders is faster than searching everything.
- Name: filename without extension; words separated by a space are separate name searches
  (`"test asset"`); partial matches work (`awesome` matches `MyAwesomeTexture`).
- `l:label` for labels (use `l:` before each label); `t:type` for built-in types (`Texture2D`) or
  ScriptableObject classes, and `t:Object` matches all assets; `b:` for assets in an AssetBundle.
- `a:` area: `all`, `assets` or `packages`.
- `glob:` e.g. `glob:Editor` (Editor folders), `glob:(Editor|Resources)`, `glob:Editor/*` (assets in
  Editor folders), `glob:Editor/**` (recursively).
- Searching is case insensitive. Use `GUIDToAssetPath` for paths and `LoadAssetAtPath` to load.
- Page example: `FindAssets("co l:architecture t:texture2D", new[] {"Assets/MyAwesomeProps"})`.

## Other AssetDatabase members (one-line descriptions on the class page)
`CreateAsset` (new asset in a native Unity format), `AddObjectToAsset`, `MoveAsset` (file or folder),
`CopyAsset`, `DeleteAsset`, `MoveAssetToTrash`, `GetDependencies`, `ImportAsset`, `Refresh` (import any
changed assets), `SaveAssets` (writes all unsaved asset changes), `SaveAssetIfDirty`,
`ForceReserializeAssets`.

## Checked
Date: 2026-11-07

Read in full: the `StartAssetEditing` page, the `FindAssets` page (remarks, both code examples) and the
`AssetDatabase` class page (a member table with one-line descriptions only; no member detail pages were
opened, nor `AssetEditingScope`).

Removed because no cited page confirms it: the `FixWeapons` menu sample (SetDirty, `Undo.RecordObject`,
progress bar), "path must end in a valid extension", `MoveAsset` returning an error string, `CopyAsset`
creating a new GUID, `AssetImporter.SaveAndReimport`, the System.IO and `.meta` gotcha, the PrefabUtility
advice, the batchmode `-executeMethod` advice and the Verify list.

Method: documentation only; no commands were run.
