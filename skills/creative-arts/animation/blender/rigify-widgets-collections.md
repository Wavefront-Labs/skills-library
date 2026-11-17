---
id: creative-arts.animation.blender.rigify-widgets-collections
name: rigify-widgets-collections
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-widgets, rigify-bone-collections, rigify-layers, rig-ui]
level: practitioner
status: docs-checked
description: "Organise Rigify controls: bone collection UI rows and titles, color sets, widget shapes per control, and widget regeneration."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/metarigs.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/basics.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_features.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-widgets-collections

Goal: a generated rig whose collection visibility panel and colours are clear for animators.

## Bone Collections UI (metarig)
Rigify generates a **Rig Layers** panel (3D Viewport sidebar, Item tab, shown when a rig bone is active) with buttons that toggle bone collections. The metarig's **Bone Collections UI** panel configures it. It lists the collections with extra properties:
- **Color Set**: the colour set for bones in this collection (if a bone is in several collections, the earlier one in the list has priority).
- **Add Selection Set**: generate a selection set for the collection.
- **UI Row**: the row of the Rig Layers panel holding the button. Zero means no button and the collection is hidden.
- **UI Title**: overrides the button label; titles need not be unique.
- **Validate Collection References**: scans and normalises collection references in rig type options. Run it before and after joining two metarig armatures, and between renaming collections and joining.
A **UI Layout** sub-panel edits the rows: arrow moves the active button to that row, plus inserts a row, minus removes one; blank rows act as separators. The `Root` collection gets a button automatically at generation; `ORG`, `DEF` and `MCH` can be given buttons manually.

## Color Sets
The **Color Sets** panel defines the bone colour scheme. *Add Standard* adds the default Rigify scheme; *Add From Theme* adds a theme's colours. Selected and Active colours default to your Preferences theme, and *Unified Selected/Active Colors* keeps them consistent across sets.

## Widgets
Generated control shapes are widget objects in the **Widgets Collection** (see rigify-generate-options). By default regeneration reuses existing widget objects so edits survive; **Overwrite Widget Meshes** regenerates them. A metarig bone with a custom widget keeps it (the custom widget is copied to a control, usually the FK one, and suppresses automatic widget generation). Single-bone types like `basic.super_copy` offer a Widget Type option.

## Gotchas
- A collection with UI Row 0 has no button and is hidden in the rig panel.
- Joining armatures without validating collection references can break references.

## Verify
The Rig Layers panel shows rows in the designed order and each toggle shows or hides the intended controls.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Rigify Creating Meta-rigs, Basic Usage, Generated Rig Features), branch blender-v5.2-release. Confirmed: Bone Collections UI properties and UI Layout sub-panel, Color Sets panel buttons, Rig Layers panel and its Item tab location, widget reuse and Overwrite Widget Meshes, custom widget copying. Removed the six named colour sets, pre-4.0 layer note, hidden-collection and library-linking claims, and finalize-script advice for custom shapes.
Method: documentation only; no commands were run.
