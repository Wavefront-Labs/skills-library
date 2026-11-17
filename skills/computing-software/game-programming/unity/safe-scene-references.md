---
id: computing-software.game-programming.unity.safe-scene-references
name: safe-scene-references
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, scene-reference, build-index, scene-asset, game-programming]
level: practitioner
status: draft
description: "Reference Unity scenes safely: build index vs name vs path vs Addressables keys, editor SceneAsset fields that survive renames, and Build Profile scene lists."
sources: ["https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.LoadScene.html", "https://docs.unity3d.com/ScriptReference/SceneAsset.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Referencing scenes safely

**Goal:** level-select buttons and portals that keep working when scenes are renamed, moved or
reordered.

## Options
| Reference | Breaks when | Notes |
|---|---|---|
| Build index (`LoadScene(3)`) | list reordered | fastest to type, worst to maintain |
| Name (`"Forest"`) | renamed; duplicate names in different folders | ambiguous with duplicates |
| Path (`"Assets/Levels/Forest.unity"`) | moved | unique; works with `LoadScene` |
| Addressables key / `AssetReference` | almost never (GUID) | needs Addressables |
| Serialized `SceneAsset` -> path at build | never (GUID) | editor-only type, needs a wrapper |

## GUID-safe wrapper without Addressables
```csharp
[System.Serializable]
public class SceneRef : ISerializationCallbackReceiver {
#if UNITY_EDITOR
    [SerializeField] UnityEditor.SceneAsset asset;
#endif
    [SerializeField, HideInInspector] string path;
    public string Path => path;
    public void OnBeforeSerialize() {
#if UNITY_EDITOR
        path = asset ? UnityEditor.AssetDatabase.GetAssetPath(asset) : "";
#endif
    }
    public void OnAfterDeserialize() {}
}
// SceneManager.LoadSceneAsync(levelRef.Path);
```
`OnBeforeSerialize` runs on save/build, so renames are picked up the next time the asset is saved —
add a build preprocessor that touches assets holding SceneRefs, or validate at build time.

## Build list
Scenes loaded by path/name must be in the build list (Unity 6: Build Profiles > Scene List).
Validate in CI:
```csharp
bool inBuild = SceneUtility.GetBuildIndexByScenePath(path) >= 0;
```

## Gotchas
- `SceneManager.GetSceneByName` only finds *loaded* scenes.
- Addressable scenes must not also be in the build list (duplicated content).

## Verify
- [ ] Rename and move a referenced scene; loading still works after saving.
- [ ] Build fails with a clear error if a referenced scene is missing from the list.
