---
id: creative-arts.animation.blender.dope-sheet-channels-filters
name: dope-sheet-channels-filters
category: creative-arts
field: animation
product: blender
tags: [blender, dope-sheet, dope-sheet-channels, channel-groups, only-show-selected, dope-sheet-filters, dope-sheet-modes, shape-key-editor]
level: practitioner
status: docs-checked
description: "Organise the Blender Dope Sheet: modes, channel groups, Only Show Selected and Only Show Errors filters, channel search, and mute/lock toggles."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/dope_sheet/introduction.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/introduction.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dope-sheet-channels-filters

Goal: see only the keys you are working on, in the right editor mode.

## Modes (header dropdown)

- **Dope Sheet**: overview of most types of animatable data in the scene.
- **Action Editor**: one object's action; assign, stash and push down actions here (see `action-editor-assign`).
- **Shape Key Editor**: shape key animation of the active mesh.
- **Grease Pencil**: grease pencil frames.
- **Mask**: mask animation (other types such as masks need their specific mode).
- **Cache File**: listed in the dropdown but never implemented; do not rely on it for Alembic data.

## Channels

- The channel list is a tree of items (objects, bones...) and their animated properties; each channel has an F-curve. Row colours: dark blue scenes/objects, light blue actions and shape keys, green channel groups, gray channels.
- Ctrl-G groups selected channels, Ctrl-Alt-G ungroups (Channel > Un/Group Channels); double-click a group to rename it. By default Blender creates one group per bone.
- Per-channel toggles: Pin, Hide (Ctrl-LMB solos the channel), Modifiers, **Mute** (a muted channel, empty checkbox, does not affect the animation), **Lock** (Tab; a protected channel cannot be edited).
- Expand/collapse selected headers with Numpad + and Numpad - (Channel > Expand/Collapse Channels).
- Select all channels: A; deselect: Alt-A; double-click a channel header to select all its keyframes.
- Reorder channels: PageUp / PageDown, Shift-PageUp / Shift-PageDown (Channel > Move).

## Filters

- **Search** (Ctrl-F) filters channels by part of their name; the Invert button shows channels that do not match.
- Header filters in the time-based editors: **Show Only Selected** (only items belonging to selected objects/bones; turn off to see everything, often why keys seem to disappear), **Show Hidden** (items of hidden objects/bones), **Show Only Errors** (channels that animate a property that does not exist, for example after a rename).

## Gotchas

- Renamed bones or objects leave F-curves with broken data paths; Show Only Errors finds them. Fix by renaming back or editing the data path.
- Muted channels do not affect the animation, so anything that reads the evaluated result will not see their motion.

## Verify

With Show Only Selected on, selecting a bone shows only its group; with Show Only Errors on, the list is empty when nothing is broken.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Dope Sheet mode list (Cache File never implemented), channel list colours, group/ungroup, mute/lock/hide behaviour and shortcuts, expand/collapse and move shortcuts, Search with Invert, filter names. Removed as unconfirmed: Filter by Type, Summary row, Ctrl-click expand-all, Only Show Errors red underline, FBX bake claim.
Method: documentation only; no commands were run.
