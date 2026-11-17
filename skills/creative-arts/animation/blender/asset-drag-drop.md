---
id: creative-arts.animation.blender.asset-drag-drop
name: asset-drag-drop
category: creative-arts
field: animation
product: blender
tags: [blender, asset-browser, asset-drag-drop, drop-asset, node-groups, materials, collection-instance]
level: practitioner
status: docs-checked
description: "Use Blender assets by dragging: objects and worlds into the scene, materials onto objects, node groups as modifiers, collections as instances, and import method effects."
sources:
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# asset-drag-drop

Goal: place assets where they belong with one gesture.

## The rule

An asset is used by dragging it from the Asset Browser to the desired location. What gets created depends on the asset type and on the Import Method (Follow Asset or Preferences, Link, Append, Pack) shown in the Asset Browser header.

## By asset type

- **Objects and worlds:** drag into the scene. Dropping a world asset into the viewport replaces the current world.
- **Materials:** drag onto the object that should use it; the drop replaces the material slot.
- **Geometry node groups:** drag onto an object to add a Geometry Nodes modifier. Node group assets can also be dragged into compatible node editors (Geometry Nodes, Shader Editor, Compositor), and appear in the Add menus following their catalog hierarchy.
- **Collections:** added as an instance (one empty representing the whole collection), so the content is not visible in the Outliner. Enable the *Instance* option in the redo panel after dropping into the 3D Viewport to choose instance or full hierarchy, or use the header option Instance Collections - When Linking/Appending. Collection assets from the Current File are always instanced.
- **Scenes:** dragging a scene asset into a window other than the Asset Browser imports or links the scene and makes it that window's active scene.
- **Pose assets and brushes** are preset assets: they are applied or activated rather than placed. Poses are described in the Pose Library page; brush assets are loaded into the file and activated but not saved in it.

## Turning an instance into real objects

- The operator `bpy.ops.object.duplicates_make_real` (Make Instances Real) replaces the instance by the collection contents.
- Or delete the instance object, find the collection in the Outliner Blender File mode and use *Link to Scene* in its context menu.

## Making a linked asset editable

After import you can link an object to the scene and then make just the object local (`Object > Relations > Make Local... > Selected Objects`), keeping its mesh and materials linked to the library.

## Gotchas

- Check the Import Method before dragging into production files. Append makes independent copies each time you drag; Link keeps the asset read-only.
- Online asset libraries cannot be linked directly; assets must be appended or packed.

## Verify

The Outliner shows the new data in the expected collection; for linked assets the library appears in the Blender File mode.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/asset_browser.rst, files/asset_libraries/introduction.rst).
Confirmed: drag behaviour per type, material slot replacement, node group modifier drop, collection instancing and the Instance option, scene asset drop, instance-to-real routes, Make Local route. Removed unconfirmed claims: surface snapping and bounding box preview, specific Shift A and asset-shelf gestures, version tags for node tools and brushes, and Modifier/Tool flag details.
Method: documentation only; no commands were run.
