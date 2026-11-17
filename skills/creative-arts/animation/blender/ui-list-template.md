---
id: creative-arts.animation.blender.ui-list-template
name: ui-list-template
category: creative-arts
field: animation
product: blender
tags: [blender, ui-list-template, uilist, template-list, collection-property, addon-development, bpy]
level: practitioner
status: docs-checked
description: "Build a scrollable list in an add-on panel with UIList and template_list: CollectionProperty plus index, draw_item, add/remove/move operators and custom filtering."
sources:
  - https://docs.blender.org/api/current/bpy.types.UIList.html
  - https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.template_list
  - https://docs.blender.org/api/current/bpy.props.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ui-list-template

Goal: a list widget like the material slots or vertex groups list, backed by your own data.

## Data

```python
import bpy
from bpy.props import CollectionProperty, IntProperty, StringProperty, FloatProperty

class SHOT_PG_item(bpy.types.PropertyGroup):
    name: StringProperty()           # 'name' is used for search/filter and double-click rename
    frames: IntProperty(default=48)

# in register(), after registering the PropertyGroup:
bpy.types.Scene.shot_items = CollectionProperty(type=SHOT_PG_item)
bpy.types.Scene.shot_index = IntProperty()
```

## The list class and the panel

```python
class SHOT_UL_items(bpy.types.UIList):          # PREFIX_UL_name convention
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='SEQUENCE')
            layout.prop(item, "frames", text="")
        else:                                    # any other layout type
            layout.label(text=item.name)

class SHOT_PT_panel(bpy.types.Panel):
    bl_label, bl_space_type, bl_region_type, bl_category = "Shots", 'VIEW_3D', 'UI', "Shots"
    def draw(self, context):
        sc = context.scene
        row = self.layout.row()
        row.template_list("SHOT_UL_items", "", sc, "shot_items", sc, "shot_index", rows=5)
        col = row.column(align=True)
        col.operator("shot.item_add", icon='ADD', text="")
        col.operator("shot.item_remove", icon='REMOVE', text="")
```

`template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, *, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)`. `list_id` tells different list widgets apart (mandatory with the default `UI_UL_list` class); a non-empty value becomes the custom ID, otherwise the class name is used. `type` is `'DEFAULT'` or `'COMPACT'` here.

## Add / remove operators

```python
class SHOT_OT_item_add(bpy.types.Operator):
    bl_idname, bl_label, bl_options = "shot.item_add", "Add Shot", {'REGISTER', 'UNDO'}
    def execute(self, context):
        sc = context.scene
        it = sc.shot_items.add(); it.name = f"sh{len(sc.shot_items):03d}0"
        sc.shot_index = len(sc.shot_items) - 1
        return {'FINISHED'}

class SHOT_OT_item_remove(bpy.types.Operator):
    bl_idname, bl_label, bl_options = "shot.item_remove", "Remove Shot", {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context): return len(context.scene.shot_items) > 0
    def execute(self, context):
        sc = context.scene
        sc.shot_items.remove(sc.shot_index)
        sc.shot_index = min(sc.shot_index, len(sc.shot_items) - 1)
        return {'FINISHED'}
```

## Custom filtering

Override `filter_items(self, context, data, propname)` returning `(flags, order)`: a list of integers where `self.bitflag_filter_item` marks a row as shown (the upper 16 bits are reserved for internal use, the lower 16 are free for your own flags), and a list of new indices for reordering (empty for no reordering). `bpy.types.UI_UL_list.filter_items_by_name(...)` and `sort_items_by_name(...)` are ready-made helpers; `draw_item` may also take a trailing `flt_flag` argument to receive your flags.

## Gotchas

- Register the PropertyGroup before assigning the CollectionProperty; unregister in reverse and `del bpy.types.Scene.shot_items`.
- Do not modify data inside `draw_item`; drawing code runs on every redraw (practice).

## Verify

Add five items, rename one by double-click, filter by name with the list's search field, remove the active one and confirm the index stays valid; undo restores it.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `UILayout.template_list` full signature and `list_id` semantics; UIList example showing `draw_item(self, context, layout, data, item, icon, active_data, active_propname, index[, flt_flag])`, `filter_items`, `bitflag_filter_item` (upper 16 bits reserved), `UI_UL_list` helper `filter_items_by_name`, `sort_items_by_name`, `layout_type` enumeration (DEFAULT, COMPACT).
- Removed as unconfirmed: the `GRID` layout name (the 5.2 enum lists only DEFAULT and COMPACT) and the `collection.move` call (not found on the API pages).

Method: documentation only; no commands were run.
