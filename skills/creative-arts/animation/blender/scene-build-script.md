---
id: creative-arts.animation.blender.scene-build-script
name: scene-build-script
category: creative-arts
field: animation
product: blender
tags: [blender, scene-build-script, scene-assembly, manifest-driven, json, csv, collection-instance, pipeline]
level: advanced
status: docs-checked
description: "Assemble Blender scenes from JSON or CSV manifests: link or append assets by name, place collection instances with transforms, validate missing items and save."
sources:
  - https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
  - https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.instance_collection
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# scene-build-script

Goal: a layout or set-dressing description in data (from an editorial tool, a spreadsheet or another DCC) becomes an identical .blend every time.

## Manifest

```json
{"scene": "sh010", "frame_range": [1001, 1096],
 "assets": [
   {"name": "crate_a", "library": "//../lib/props.blend", "collection": "crate_a",
    "location": [1.2, 0, 0], "rotation_deg": [0, 0, 35], "scale": 1.0}
 ]}
```

## Build

```python
import bpy, json, math, sys
from mathutils import Euler

def link_collection(lib_path, coll_name):
    coll = bpy.data.collections.get(coll_name)
    if coll and coll.library:
        return coll
    with bpy.data.libraries.load(bpy.path.abspath(lib_path), link=True) as (src, dst):
        if coll_name not in src.collections:
            raise KeyError(f"{coll_name} not in {lib_path}")
        dst.collections = [coll_name]
    return dst.collections[0]

m = json.load(open(manifest_path))
sc = bpy.context.scene
sc.frame_start, sc.frame_end = m["frame_range"]
missing = []
for a in m["assets"]:
    try:
        coll = link_collection(a["library"], a["collection"])
    except (KeyError, OSError) as e:
        missing.append(str(e)); continue
    inst = bpy.data.objects.new(a["name"], None)
    inst.instance_type = 'COLLECTION'
    inst.instance_collection = coll
    inst.location = a["location"]
    inst.rotation_euler = Euler([math.radians(v) for v in a["rotation_deg"]])
    inst.scale = (a["scale"],) * 3
    sc.collection.objects.link(inst)
if missing:
    print("MISSING:", *missing, sep="\n"); sys.exit(1)
bpy.ops.wm.save_as_mainfile(filepath=out_path)
```

`link_collection` returns an already-linked collection of that name instead of linking again, so an asset placed 50 times is linked once and instanced 50 times (practice; it matches by name only).

## CSV variant

`csv.DictReader` with columns `name,library,collection,x,y,z,rz,scale`; convert strings to floats explicitly.

## Gotchas

- Start from an empty file (`bpy.ops.wm.read_factory_settings(use_empty=True)`) or a template so reruns do not stack duplicates.
- Linked collections are not editable; a library override (`creative-arts.animation.blender.override-hierarchy`) is needed if animators must pose the asset.
- Confirm the manifest's units and up axis match the scene's unit settings (practice).
- Fail on missing assets; a silently skipped item becomes a hole found in comp.

## Verify

Rebuild twice and diff `[(o.name, tuple(o.matrix_world.translation)) for o in sc.objects]`: identical; delete an asset from the library and confirm the build exits non-zero listing it.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `bpy.data.libraries.load(filepath, link=...)` context manager returning source and destination name lists, `Object.instance_type`, `Object.instance_collection`, `bpy.ops.wm.read_factory_settings(use_empty=)`, `bpy.ops.wm.save_as_mainfile`.
- The reuse behaviour is the script's own name check, now stated as such.

Method: documentation only; no commands were run.
