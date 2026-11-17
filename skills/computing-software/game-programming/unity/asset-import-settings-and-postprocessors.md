---
id: computing-software.game-programming.unity.asset-import-settings-and-postprocessors
name: asset-import-settings-and-postprocessors
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables, assetpostprocessor, import-settings, texture-import, model-import, presets, asset-pipeline, onpreprocesstexture, game-programming]
level: practitioner
status: docs-checked
description: "Hook the Unity import pipeline with AssetPostprocessor (pre and post hooks, model import order, GetVersion) and reuse import settings with Presets."
sources: ["https://docs.unity3d.com/ScriptReference/AssetPostprocessor.html", "https://docs.unity3d.com/Manual/Presets.html", "https://docs.unity3d.com/Manual/class-TextureImporter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asset import settings and AssetPostprocessor

**Goal:** make import settings automatic and consistent instead of relying on manual changes per asset.

## AssetPostprocessor
- `AssetPostprocessor` (namespace `UnityEditor`) lets you hook into the import pipeline and run
  scripts before or after importing assets. Properties: `assetImporter`, `assetPath`, `context`.
- Pre hooks run before import, for example `OnPreprocessTexture` (just before the texture importer
  runs), `OnPreprocessModel`, `OnPreprocessAudio`, `OnPreprocessAnimation`, `OnPreprocessAsset`
  (just before any asset is imported).
- Post hooks include `OnPostprocessTexture` (after import, just before Unity compresses),
  `OnPostprocessModel`, `OnPostprocessAudio`, `OnPostprocessSprites`, `OnPostprocessPrefab`,
  `OnPostprocessMaterial` and `OnPostprocessAllAssets` (after importing any number of assets is
  complete).
- Model import order: `OnPreprocessModel` first (you can override `ModelImporter` settings for the
  whole import); after meshes and materials are imported the hierarchy is created, and
  `OnPostprocessMeshHierarchy` can change it; `OnAssignMaterialModel` is invoked before a Material is
  assigned to a MeshRenderer; `OnPostprocessGameObjectWithUserProperties` follows; if animation
  generation is not disabled (`ModelImporter.generateAnimations`), skinned mesh and animations are
  generated, then `OnPostprocessModel` is called for the root GameObject.
- `GetPostprocessOrder` returns the execution order priority.
- Versioning: the page says that if you change the code of an AssetPostprocessor you should default
  to incrementing its version number with `AssetPostprocessor.GetVersion`, for example when the output
  or declared input dependencies change.

## Presets
Presets are assets that save and apply identical property settings across components, assets or
Project Settings windows, and can specify defaults for new components and default import settings. They
apply only in the Editor and have no effect at runtime. The manual's sub-topics include setting
default presets and applying default presets to assets by folder (Preset Manager).

## Texture importer
The Texture Import Settings window page is an index to the "Texture type and shape settings" and
"Platform-specific texture overrides" reference pages; its own text lists no settings.

## Checked
Date: 2026-11-07

Read in full: the `AssetPostprocessor` reference (remarks, property and method tables), the Presets
overview page and the Texture Import Settings overview page. The Presets and Texture pages are only
tables of links; the sub-pages were not opened.

Removed because no cited page confirms it: the whole `ImportRules` code sample (importer property
names, ASTC format, audio load types), "halves mesh memory", `importSettingsMissing` first-import
check, `glob:` filter syntax, the Presets-apply-on-first-import-only claim, reimport menu paths,
`FindAssets` audit script and CI use, the three Gotchas (worker processes, postprocess no-ops, Sprite
Atlas overrides) and the Verify list.

Method: documentation only; no commands were run.
