---
id: creative-arts.animation.blender.pie-menus
name: pie-menus
category: creative-arts
field: animation
product: blender
tags: [blender, pie-menus, pie-menu, interface, keymap, extensions, wm-call-menu-pie]
level: practitioner
status: docs-checked
description: "Use and build Blender pie menus: stock pies (Z, ~, Tab, period), the Viewport Pies extension, keymap binding with wm.call_menu_pie, and a minimal Python pie."
sources:
  - https://docs.blender.org/manual/en/latest/interface/controls/buttons/menus.html
  - https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.call_menu_pie
  - https://docs.blender.org/manual/en/latest/editors/preferences/interface.html
  - https://docs.blender.org/api/current/bpy.types.Menu.html
  - https://extensions.blender.org/add-ons/viewport-pie-menus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# pie-menus

Goal: radial menus that become muscle memory — gesture direction, not reading.

## Stock pies (Blender keymap)

- Blender ships several pie menus in its default keymap; the keys depend on the keymap, so check Preferences > Keymap or hover a menu item to see its shortcut.
- Holding the key, flicking and releasing selects without a click; a quick tap opens the pie so you can click an item.

## Preferences > Interface > Pie Menus

- **Animation Timeout** (length of the opening animation), **Tap Key Timeout** (keystrokes held longer than this dismiss the menu on release; in 1/100 s), **Recenter Timeout** (how long the pie keeps the initial mouse position as centre, for fast dragged selections; in 1/100 s), **Radius** (pixels from the centre to the items), **Threshold** (distance from the centre before a selection can be made), **Confirm Threshold** (distance after which the selection is made; zero disables).

## More pies

- *3D Viewport Pie Menus* ("Various pie menus to speed up your workflow") is listed on extensions.blender.org; install it from Edit > Preferences > Get Extensions and check its preferences for the pies and keys it adds.

## Your own pie

```python
import bpy
class VIEW3D_MT_pie_mytools(bpy.types.Menu):
    bl_label = "My Tools"
    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("object.shade_smooth")
        pie.operator("object.shade_flat")
        pie.operator("object.origin_set").type = 'ORIGIN_GEOMETRY'
bpy.utils.register_class(VIEW3D_MT_pie_mytools)
```

`UILayout.menu_pie()` returns a sub-layout whose items are placed radially around the menu centre. Bind it with a keymap item for `wm.call_menu_pie` (parameter `name`) set to `VIEW3D_MT_pie_mytools`, for example in Preferences > Keymap (3D View > Object Mode) with *Add New*.

## Gotchas

- Keep a pie to a handful of items and nest sub-menus for more (practice, not from the docs).

## Checked

Blender 5.2 manual (blender-v5.2-release, editors/preferences/interface) and Python API 5.2, read 2026-10-27.
- Pie Menus preference names and meanings (Animation Timeout, Tap Key Timeout, Recenter Timeout, Radius, Threshold, Confirm Threshold): manual interface preferences page. `UILayout.menu_pie()` and `bpy.ops.wm.call_menu_pie(name=)`: API 5.2. The extension page 3D Viewport Pie Menus exists at extensions.blender.org/add-ons/viewport-pie-menus/.
- Removed as unconfirmed: the stock pie key list, the clockwise item order, the 8-item limit and key-stealing claims. Corrected the Tap Key Timeout meaning (it is not milliseconds).

Method: documentation only; no commands were run.
