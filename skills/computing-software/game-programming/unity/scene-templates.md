---
id: computing-software.game-programming.unity.scene-templates
name: scene-templates
category: computing-software
field: game-programming
product: unity
tags: [unity, scene-templates, scenes, editor-workflow, game-programming]
level: practitioner
status: docs-checked
description: "Create Unity scene templates so new scenes start pre-configured, and know the menu paths, clone-vs-reference dependencies and scripting entry points."
sources: ["https://docs.unity3d.com/Manual/scene-templates.html", "https://docs.unity3d.com/Manual/scene-templates-creating.html", "https://docs.unity3d.com/ScriptReference/SceneTemplate.SceneTemplateService.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scene templates

**Goal:** new scenes start from a standard set of assets and settings instead of an empty default scene.

## Create (Manual: Creating scene templates)
- **Empty template**: Assets > Create > Scene Template, or right-click a Project folder > Create > Scene Template.
  An empty template does not appear in the New Scene dialog until you edit its properties to associate a scene
  asset.
- **From an existing scene asset**: right-click the scene > Create > Scene Template From Scene, or select it and
  use Assets > Create > Scene Template From Scene.
- **From the current scene**: File > Save As Scene Template (Unity prompts to save unsaved changes first).
After creating from a scene, edit the template's properties to choose which dependencies Unity clones when a new
scene is created from it.
- Tip from the Manual: before creating a template from a scene, make a folder with the same name as the scene and
  put the assets you want cloned in it; Unity then enables Clone for those assets automatically.

## Clone or reference
The Manual's "Editing scene templates" page covers configuring which assets to clone or reference. When a template
is created from a scene via the API, all of the scene's dependencies are extracted and set to be referenced
(`CreateTemplateFromScene`). Use Clone for assets each new scene should own its own copy of; leave shared assets
referenced. (The editing page itself was not read, so UI field names are not listed here.)

## Scripting (`UnityEditor.SceneTemplate`)
`SceneTemplateService` is a static class that manages instantiation. Documented members:
- `CreateSceneTemplate`: new template at a path, not bound to a scene.
- `CreateTemplateFromScene`: new template bound to a scene; dependencies extracted and set to be referenced.
  The Manual shows `SceneTemplate.CreateTemplateFromScene(SceneAsset sourceSceneAsset, string sceneTemplatePath)`.
- `Instantiate`: instantiates a new scene from a template.
- Events `newSceneTemplateInstantiating` (before) and `newSceneTemplateInstantiated` (after).
The Manual also has a "Customizing new scene creation" page for scripts that hook into scene creation.

## Verify
- [ ] The New Scene dialog lists the template and a scene created from it needs no manual setup.
- [ ] Only the assets that must be per-scene copies are cloned.

## Checked
Date 2026-11-09. Read in full as fetched text: Scene templates, Creating scene templates, and the
SceneTemplateService script reference. Confirmed menu paths, empty-template behaviour, folder-naming tip,
API method purposes and events.
Removed as unconfirmed: the pipeline interface sample (`ISceneTemplatePipeline` and its callbacks), the Inspector
field names (title, description, thumbnail, Pin in New Scene dialog), the Project Settings clone/reference
defaults note and claims about how source-scene edits flow into templates. The editing and customizing pages were
not opened.
Method: documentation only; no commands were run.
