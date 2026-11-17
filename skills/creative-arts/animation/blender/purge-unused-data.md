---
id: creative-arts.animation.blender.purge-unused-data
name: purge-unused-data
category: creative-arts
field: animation
product: blender
tags: [blender, purge-unused-data, fake-user, orphan-purge, orphan-data, users-count, file-management, data-blocks]
level: practitioner
status: docs-checked
description: "Clean bloated .blend files: user counts, fake users, File > Clean Up > Purge Unused Data (local, linked, recursive), the Unused Data view, and orphans_purge."
sources:
  - https://docs.blender.org/manual/en/latest/files/data_blocks.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/api/current/bpy.types.BlendData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# purge-unused-data

Goal: smaller, cleaner files without deleting materials, actions or node groups you meant to keep.

## The model

- Every data-block has a user count (shown next to its name when more than one). Blender follows the rule that unused data is eventually removed, by skipping zero-user data-blocks when writing the file.
- **Fake user (Protected):** the shield-icon button next to a data-block's name. A protected data-block is never silently deleted by Blender (you can still remove it by hand). Typical uses: an animation library of Actions, or spare materials. Linked data cannot be protected this way.

## Purge

- `File > Clean Up > Purge Unused Data...` (`outliner.orphans_purge`) opens a dialog (it cannot be undone):
  - **Local Data-Blocks:** remove unused data-blocks from the current file.
  - **Linked Data-Blocks:** remove unused data-blocks from linked data.
  - **Recursive Delete:** also remove data-blocks only used by unused data-blocks, so no orphans remain afterwards.
- `File > Clean Up > Manage Unused Data...` (`outliner.orphans_manage`) opens the Unused Data view.
- Outliner display mode **Unused Data**: lists data-blocks that are unused or only have a fake user; the shield icon on the right adds or removes a fake user, and the header **Purge** button runs the same dialog. Unused data-blocks are also deleted automatically when you save and reload.

## Python

```python
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
users = bpy.data.user_map(subset={mat})   # who uses this data-block
```

`BlendData.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)` is the documented signature (note the default for `do_recursive`); `BlendData.user_map(subset=None, key_types=None, value_types=None)` shows what uses what.

## Find hidden users

Outliner Blender File mode lists every data-block with its user count and fake-user shield; `user_map` answers "why won't this material go away".

## Gotchas

- Anything unused and unprotected goes: an Action keyed once and then unassigned, or an image you painted but never assigned. Give it a fake user first.
- Purge cannot be undone; keep a saved copy in production.
- The purge dialog can also touch linked data, so leave Linked Data-Blocks off if you only want to clean your own data.

## Verify

Compare file size before and after; counts such as `len(bpy.data.materials)` drop; renders are unchanged.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/data_blocks.rst, editors/outliner/interface.rst), the current Python API (BlendData.orphans_purge, BlendData.user_map, bpy.ops.outliner.orphans_purge) and the 5.3 release source (space_topbar.py Clean Up menu).
Confirmed: user count and fake user behaviour, dialog options and the no-undo warning, menu entries, Unused Data view behaviour, Python signatures. Removed unconfirmed claims: a `Recursive Unused Data-Blocks` menu entry, the "4.2+" dialog history, `F` as a fake-user key, assets receiving a fake user automatically, NLA strips counting as users, brushes and palettes carrying fake users.
Method: documentation only; no commands were run.
