---
id: creative-arts.animation.blender.compositor-node-groups
name: compositor-node-groups
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, compositor-node-groups, node-groups, asset-library]
level: practitioner
status: docs-checked
description: "Build reusable compositor node groups: Ctrl G grouping, interface sockets and panels, sharing through asset libraries and Link or Append, and versioning a show comp template."
sources:
  - https://docs.blender.org/manual/en/latest/interface/controls/nodes/groups.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
  - https://docs.blender.org/manual/en/latest/compositing/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# compositor-node-groups

Goal: one comp tool (grade, lens look, recombine) used across all shots and kept in sync.

## Make a group

1. Select nodes, **Node > Make Group** (**Ctrl G**). **Tab** (or Ctrl Tab) enters and leaves a group; **Node > Ungroup** (**Ctrl Alt G**) dissolves it.
2. Sidebar (N) > Group tab: the *Group* panel holds the node name and look; the *Group Sockets* panel adds, removes, reorders and edits sockets and **panels** (panels sit at the bottom of the node, can be nested, and can have a toggle checkbox). Each socket has default, min and max values.
3. Expose only meaningful controls (Lens Distortion Amount, Grain Strength) and keep the rest inside.

## Share

- **Asset library**: use **Mark as Asset** on the node group (data-block selector or Outliner), save the .blend inside a folder registered as an asset library in Preferences. Blender does not copy the asset into the library for you; the file must be saved there. Artists then drag the group from the Asset Browser.
- **File > Link** keeps a reference to the source file (changes made there propagate, data is not editable locally); **File > Append** makes a local copy. For a show look, link it so updates reach every shot.
- Online asset libraries cannot be linked directly: assets from them must be appended or packed.

## Versioning

Name groups with a version (`LensLook_v003`) when changes must not affect approved shots. Old shots keep the old version, and new ones get the latest.

## Compositor note (5.x)

In the current manual the compositor output is a *Group Output* node: the compositor looks for the active Group Output first, then the active Viewer, and does not run if neither exists. Group Output takes priority over a Viewer node.

## Gotchas

- Zero-user data-blocks are skipped when saving; protect a library group with the shield (Fake User) button next to its name.
- Changing an input socket type can break links in files that use the group.
- Compositor node groups can also drive Sequencer compositor strips and modifiers; the first group output socket must be a Color socket.

## Verify

Link the group into a second file, change a node inside the library file, then reopen the shot file. The change should appear.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): interface/controls/nodes/groups.rst (Ctrl G, Ctrl Alt G, Tab, Group and Group Sockets panels, panels and toggles), files/asset_libraries/introduction.rst (Mark as Asset, library must be saved in the registered folder, online libraries limits), files/linked_libraries/link_append.rst, files/data_blocks.rst (zero-user data-blocks not saved, shield button), compositing/usage.rst and compositor_system.rst (Group Output priority, Color first output socket). Removed: the claim that a scene's compositor can be assigned a linked group, the Reload menu path, and the 4.x/5.0 version framing. Method: documentation only; no commands were run.
