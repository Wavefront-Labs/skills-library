---
id: creative-arts.animation.blender.addon-development
name: addon-development
category: creative-arts
field: animation
product: blender
tags: [blender, addon-development, operators, panels, property-groups, extension-manifest, bpy, python, ui-layout, register, keymap, preferences, extension-build, pipeline-tools, operator-invoke-execute, property-group-registration, addon-preferences-class, addon-keymap, menu-registration, operator-undo-redo, addon-testing]
level: advanced
status: docs-checked
description: "Write a Blender add-on/extension: layout and blender_manifest.toml, Operator with props/poll/undo, panels, menus, PropertyGroups, preferences, keymaps, reload, build."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/extension_arguments.html
  - https://docs.blender.org/api/current/info_quickstart.html
  - https://docs.blender.org/api/current/bpy.types.Operator.html
  - https://docs.blender.org/api/current/bpy.props.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# addon-development

Goal: a tool artists click, with undo, a redo panel, saved settings and a one-file install — built the 4.2+ extension way (works as a legacy add-on with minor changes).

## Layout

```
my_tool/
  blender_manifest.toml
  __init__.py        # register/unregister only
  operators.py
  ui.py
  properties.py
  prefs.py
```
`blender_manifest.toml`:
```toml
schema_version = "1.0.0"
id = "my_tool"                 # unique, snake_case; module becomes bl_ext.<repo>.my_tool
version = "1.0.0"
name = "My Tool"
tagline = "Does one thing well"
maintainer = "Studio <pipeline@example.com>"
type = "add-on"
blender_version_min = "4.2.0"
license = ["SPDX:GPL-3.0-or-later"]
tags = ["Mesh", "Pipeline"]
# permissions = {files = "Writes caches next to the blend", network = "Fetches asset list"}
# wheels = ["./wheels/numpy-....whl"]   # bundled Python deps
# platforms = ["windows-x64", "linux-x64", "macos-arm64"]
```
Legacy equivalent: a `bl_info = {"name":..., "blender": (4, 2, 0), "category": "Object", "version": (1,0,0)}` dict in `__init__.py` and no manifest. Extensions **must** use relative imports (`from . import operators`) and must not rely on the module name (`__package__` gives it: `bpy.context.preferences.addons[__package__]`).

## Operator

```python
import bpy
from bpy.props import FloatProperty, BoolProperty, EnumProperty

class MYTOOL_OT_shrink(bpy.types.Operator):
    bl_idname = "mytool.shrink"          # category.name
    bl_label = "Shrink Selected"
    bl_description = "Scale selected mesh objects toward their origin"
    bl_options = {'REGISTER', 'UNDO'}    # UNDO is mandatory when the operator changes data (needs REGISTER too)

    factor: FloatProperty(name="Factor", default=0.9, min=0.01, max=1.0, subtype='FACTOR')
    apply: BoolProperty(name="Apply Scale", default=False)
    mode: EnumProperty(name="Mode", items=[('UNIFORM', "Uniform", ""), ('Z', "Z only", "")])

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and any(o.type == 'MESH' for o in context.selected_objects)

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.type != 'MESH':
                continue
            s = (self.factor,)*3 if self.mode == 'UNIFORM' else (1, 1, self.factor)
            ob.scale = [a*b for a, b in zip(ob.scale, s)]
        if self.apply:
            bpy.ops.object.transform_apply(scale=True)
        self.report({'INFO'}, f"Shrunk {len(context.selected_objects)} objects")
        return {'FINISHED'}

    def invoke(self, context, event):        # optional: dialog before running
        return context.window_manager.invoke_props_dialog(self)
```
Rules: do real work in `execute`; `invoke` for mouse/dialog (`invoke_props_dialog`, `invoke_confirm`, `fileselect_add` with a `filepath: StringProperty(subtype='FILE_PATH')`); return `{'FINISHED'}`, `{'CANCELLED'}`, or `{'RUNNING_MODAL'}` (`creative-arts.animation.blender.handlers-timers` for modal). Avoid `bpy.ops` inside operators when the data API does it (`ob.scale = …` instead of `transform.resize`) — ops depend on context and are slower. `self.report({'ERROR'}, msg)` shows a popup; `{'WARNING'}` in the status bar. Properties **must** use the annotation syntax (`name: Type(...)`).

## Panel and menus

```python
class MYTOOL_PT_main(bpy.types.Panel):
    bl_label = "My Tool"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "My Tool"   # N-panel tab
    bl_context = "objectmode"      # only show in object mode (optional)

    def draw(self, context):
        layout = self.layout
        s = context.scene.mytool
        col = layout.column(align=True)
        col.prop(s, "factor")
        row = col.row(align=True)
        row.operator("mytool.shrink", icon='FULLSCREEN_EXIT').factor = s.factor
        row.prop(s, "apply", toggle=True)
        box = layout.box(); box.label(text="Info", icon='INFO')
        box.prop(context.object, "name") if context.object else box.label(text="No object")
        layout.operator_menu_enum("mytool.shrink", "mode")
```
`bl_space_type`/`bl_region_type` pairs: `VIEW_3D`/`UI` (N panel), `PROPERTIES`/`WINDOW` + `bl_context = "object"` (Properties tab), `NODE_EDITOR`/`UI`, `IMAGE_EDITOR`/`UI`, `SEQUENCE_EDITOR`/`UI`, `TOPBAR`/`HEADER`. Sub-panels: `bl_parent_id`. `bl_options = {'DEFAULT_CLOSED'}`. Layout: `row/column(align=True)`, `split(factor=)`, `box()`, `prop(..., expand=True)` for enums, `prop_search` for data lookups, `template_list` for UILists, `template_ID`, `template_icon_view`. Menus: subclass `bpy.types.Menu` with `draw`; append to existing ones with `bpy.types.VIEW3D_MT_object.append(draw_fn)` (and `.remove` on unregister); `bpy.types.VIEW3D_MT_add` etc. Header buttons via `VIEW3D_HT_header.append`.

## Properties that persist

```python
class MYTOOL_Props(bpy.types.PropertyGroup):
    factor: bpy.props.FloatProperty(default=0.9, min=0, max=1)
    apply: bpy.props.BoolProperty()
    target: bpy.props.PointerProperty(type=bpy.types.Object, poll=lambda self, o: o.type == 'MESH')
    items: bpy.props.CollectionProperty(type=SomeOtherGroup)
# register: bpy.types.Scene.mytool = bpy.props.PointerProperty(type=MYTOOL_Props)
# unregister: del bpy.types.Scene.mytool
```
Attach to `Scene` (per file), `Object`, `WindowManager` (not saved — UI state), or the add-on preferences (per user). `update=` callbacks run on change (don't modify the same property inside). `options={'HIDDEN'}`/`{'SKIP_SAVE'}` on operator props keep them out of the redo panel/last-used memory.

## Preferences and keymaps

```python
class MYTOOL_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    cache_dir: bpy.props.StringProperty(subtype='DIR_PATH')
    def draw(self, context): self.layout.prop(self, "cache_dir")
# access: bpy.context.preferences.addons[__package__].preferences.cache_dir
```
Keymap: in register — `kc = bpy.context.window_manager.keyconfigs.addon; km = kc.keymaps.new(name="Object Mode", space_type='EMPTY'); kmi = km.keymap_items.new("mytool.shrink", 'S', 'PRESS', ctrl=True, alt=True); addon_keymaps.append((km, kmi))`; remove them in unregister. Keep keymaps minimal; users rebind in Preferences → Keymap (filter by the operator name).

## Registration

```python
classes = (MYTOOL_Props, MYTOOL_OT_shrink, MYTOOL_PT_main, MYTOOL_Prefs)
def register():
    for c in classes: bpy.utils.register_class(c)
    bpy.types.Scene.mytool = bpy.props.PointerProperty(type=MYTOOL_Props)
    bpy.types.VIEW3D_MT_object.append(menu_fn)
def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    del bpy.types.Scene.mytool
    for c in reversed(classes): bpy.utils.unregister_class(c)
```
Order: PropertyGroups before the classes that reference them. Class naming convention (practice, as in Blender's own templates): `PREFIX_OT_name`, `PREFIX_PT_name`, `PREFIX_MT_name`, `PREFIX_UL_name`. No work at import time other than definitions; no `bpy.context` access at register (there's no window context on startup/background).

## Develop–reload loop

- Edit files in an external editor; *Preferences → Add-ons → Install from Disk* (installs into a local repository) once, then edit the installed copy in place — or, for a legacy add-on, add your folder as a *Script Directory* (Preferences → File Paths) that has an `addons/` subfolder.
- `F3 → Reload Scripts` (or `bpy.ops.script.reload()`) re-imports; because submodules cache, add at the top of `__init__.py`:
  ```python
  if "bpy" in locals():
      import importlib; importlib.reload(operators); importlib.reload(ui)
  ```
- Console: Window → *Toggle System Console* (Windows) or launch from a terminal; `print()` and tracebacks land there. *Developer Extras* + *Python Tooltips* show property paths; right-click → *Copy Data Path* / *Edit Source* opens Blender's own UI code — the best reference for layouts.
- Test headless: `blender -b --python-expr "import bpy; bpy.ops.preferences.addon_enable(module='bl_ext.<repo>.my_tool'); bpy.ops.mytool.shrink(factor=0.5)"`.

## Build, validate, distribute

- `blender -c extension validate ./my_tool` (manifest + structure checks), `blender -c extension build --source-dir ./my_tool --output-dir ./dist` → `my_tool-1.0.0.zip`. `--split-platforms` when bundling platform wheels.
- Distribute: a local repository folder (drop the zip, `blender -c extension server-generate --repo-dir=./dist` makes `index.json`), a studio HTTP repo, or upload to extensions.blender.org (held for review by the moderation team; needs a Blender ID).
- Version bump every release; keep `blender_version_min` honest (test on it) and set `blender_version_max` only when known-broken.
- Legacy packaging: zip the folder so `__init__.py` sits one level down.

## Gotchas

- Do no `bpy.context` or `bpy.data` work at register time (practice); defer it to an operator or handler.
- Properties defined with `=` instead of `:` silently become class attributes and don't show.
- UI `draw` runs every redraw — never do heavy work or create data there.
- Extensions can't `import` other add-ons by fixed module name (the repo prefix varies); communicate via `bpy.types` registration or keep code in one package.
- `bpy.props` in a `PropertyGroup` referenced by `PointerProperty` must be registered first; unregister in reverse.
- Extensions live under `bl_ext.<repository_module_name>.<id>` (4.2+); preferences lookups by a hard-coded name break — use `__package__`, and never replace it with a literal string.

## Verify

- Fresh Blender: install the built zip from disk, enable; the N-panel tab appears, operator runs, `Ctrl Z` undoes it, the Adjust Last Operation panel shows factor/mode and re-runs live.
- `blender -c extension validate` prints no errors; `blender -b --python-expr` enabling + running the operator exits 0 with no traceback.
- Disable the add-on: menus/keymaps/N-panel disappear (unregister complete); re-enable works without restarting.
- Saved file reopens with the Scene properties intact; preferences persist across sessions.

## Checked

Blender 5.2 manual (blender-v5.2-release branch) and Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- Manifest keys, required fields, tagline limits, platforms, wheels, permissions and the `blender --command extension build/validate` / `--split-platforms` options: manual extensions pages and extension command-line page.
- Legacy-to-extension rules (`__package__`, relative imports, `bl_ext.<repo>.<id>` namespace): manual add-ons page.
- `WindowManager.invoke_props_dialog`, `invoke_confirm`, `fileselect_add`, `bpy.ops.script.reload`, `bpy.ops.preferences.addon_enable(module=)`, property flags HIDDEN and SKIP_SAVE, subtype FACTOR, operator flags REGISTER/UNDO, space/region type names: API 5.2.
- Removed as unconfirmed: the `extensions/user_default/` symlink advice, the VS Code debugging extension, the `_RestrictContext` error text, idname-format and built-in-panel-replacement claims, the undo-after-invoke claim.

Method: documentation only; no commands were run.
