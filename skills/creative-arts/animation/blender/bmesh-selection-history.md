---
id: creative-arts.animation.blender.bmesh-selection-history
name: bmesh-selection-history
category: creative-arts
field: animation
product: blender
tags: [blender, bmesh-selection, select-history, bmesh, edit-mode, select-flush, bpy]
level: advanced
status: verified
description: "Read and set edit-mode selection with bmesh: select_set and flushing, select_history order and active element, faces.active and syncing back with update_edit_mesh."
sources:
  - https://docs.blender.org/api/current/bmesh.types.html#bmesh.types.BMEditSelSeq
  - https://docs.blender.org/api/current/bmesh.types.html#bmesh.types.BMesh.select_flush_mode
  - https://docs.blender.org/api/current/bmesh.html#bmesh.update_edit_mesh
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bmesh-selection-history

Goal: tools that depend on what the user picked and in which order (first/last vertex, active face).

## Read the selection

```python
import bpy, bmesh
ob = bpy.context.edit_object
bm = bmesh.from_edit_mesh(ob.data)
sel_verts = [v for v in bm.verts if v.select]
order = list(bm.select_history)          # elements in click order (BMVert/BMEdge/BMFace)
active = bm.select_history.active        # last clicked element, or None
face_active = bm.faces.active            # active face (separate from history)
```
`select_history` is a `BMEditSelSeq`: it holds the elements in the order they were added and `active` is its last element.

## Set the selection

```python
for f in bm.faces:
    f.select_set(False)
target = bm.faces[10]
target.select_set(True)          # also selects its verts/edges
bm.select_history.clear()
bm.select_history.add(target)    # make it the active element
bm.faces.active = target
bm.select_flush_mode()           # resolve per current select mode
bmesh.update_edit_mesh(ob.data)  # push to the viewport
```

- `select_set(True)` differs from assigning `elem.select`: it also updates the selection state of associated geometry.
- `bm.select_flush(select)` flushes selection from vertices regardless of mode; `select_flush_mode(flush_down=False)` flushes according to `bm.select_mode`.
- `bm.select_history.validate()` ensures all entries are selected; `discard(elem)` removes one without raising if absent (`remove(elem)` raises); `add(elem)` does nothing if already present; `clear()` empties it.

## Index access

After adding or deleting geometry call `bm.verts.ensure_lookup_table()` (and edges/faces) before `bm.verts[i]`, needed again after adding or removing elements before integer indexing.

## Gotchas

- In Object mode use `bmesh.new(); bm.from_mesh(me)`, then `bm.to_mesh(me); bm.free()`; In 4.5.14 the history is stored in the mesh: after leaving Edit Mode, `from_mesh` on that mesh gave a `select_history` holding the element last added.
- `bmesh.update_edit_mesh(mesh, loop_triangles=True, destructive=True)`: refetch element references after mode switches or destructive updates (practice).

## Verify

Click three vertices in order, run the read snippet and see them in that order with the last one as `active`; run the set snippet and see the face highlighted as the active face in the viewport.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `BMEditSelSeq` methods add, clear, discard, remove, validate and `active`; `BMesh.select_flush(select)`, `select_flush_mode(*, flush_down=False)`, `select_mode`; `BMVert/BMEdge/BMFace.select_set`; `BMFaceSeq.active`; `ensure_lookup_table()`; `bmesh.from_edit_mesh`, `bmesh.update_edit_mesh(mesh, *, loop_triangles=True, destructive=True)`: API 5.2.
- Removed as unconfirmed: which interactive tools add history entries, tool names that read it, the exact IndexError text, the ReferenceError claim.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: history order for three added vertices was [3, 1, 5] with `active` the last; `type` is BMEditSelSeq; `add` of an existing element did nothing; `remove` of an absent element raised ValueError while `discard` did not; `validate()` dropped a deselected vertex; `clear()` emptied it and `active` became None; `faces.active` is None at first and settable; indexing without `ensure_lookup_table()` raised IndexError after `from_mesh` and after `verts.new`. Unrun: interactive click order.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
