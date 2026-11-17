---
id: creative-arts.animation.blender.bpy-material-nodes-api
name: bpy-material-nodes-api
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-material-nodes-api, node-tree-api, nodes-new, shader-nodes]
level: practitioner
status: verified
description: "Build material node trees from Python: nodes.new type names, socket names across versions, links, image textures with colour space, node layout and assigning materials."
sources:
  - https://docs.blender.org/api/current/bpy.types.Nodes.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeBsdfPrincipled.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-material-nodes-api

Goal: generate materials from texture sets or data.

## Example: PBR material from files

```python
import bpy
def pbr(name, base, rough, normal):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True                               # deprecated since 5.0: no effect, always True
    nt = mat.node_tree; n = nt.nodes; L = nt.links
    bsdf = n.get("Principled BSDF")
    if bsdf is None:                                   # build the basic tree if the material is empty
        bsdf = n.new("ShaderNodeBsdfPrincipled"); out = n.new("ShaderNodeOutputMaterial")
        L.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    def tex(path, x, y, data=False):
        t = n.new("ShaderNodeTexImage"); t.location = (x, y)
        t.image = bpy.data.images.load(path, check_existing=True)
        if data: t.image.colorspace_settings.name = "Non-Color"
        return t
    b = tex(base, -600, 300);              L.new(b.outputs["Color"], bsdf.inputs["Base Color"])
    r = tex(rough, -600, 0, True);         L.new(r.outputs["Color"], bsdf.inputs["Roughness"])
    nm = n.new("ShaderNodeNormalMap"); nm.location = (-250, -300)
    t = tex(normal, -600, -300, True);     L.new(t.outputs["Color"], nm.inputs["Color"])
    L.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return mat
ob.data.materials.append(pbr("Crate", base_p, rough_p, nrm_p))
```

## Finding type names and sockets

- Turn on Python Tooltips (Preferences > Interface) to see Python information for properties. `nodes.new(type)` takes the node's `bl_idname` (such as `ShaderNodeTexImage`), not `node.type`.
- Principled BSDF socket names in 5.2 include `Base Color`, `Roughness`, `Normal`, `Specular IOR Level`, `Coat Weight`, `Subsurface Weight`, `Emission Color` and `Emission Strength`. Socket names change between releases, so check `node.inputs.keys()` for your version or index by identifier.
- `node.inputs.keys()` lists sockets.

## Layout

Set `node.location` so artists can read the tree. Use frames (`NodeFrame`) to group. Unused default nodes: remove with `n.remove(node)`.

## Gotchas

- `images.load` with `check_existing=True` reuses an image already loaded instead of duplicating it.
- In Blender 4.5.14 a new material has `use_nodes` False until you set it, so the `use_nodes = True` line is still needed there. `nodes.new("TEX_IMAGE")` (a `node.type`) fails with "Node type TEX_IMAGE undefined".
- If a node has several sockets with the same name, index by position or by `socket.identifier`.
- Materials on object vs data: `ob.material_slots[i].link = 'OBJECT'` for per-object materials on shared meshes.

## Verify

Open the Shader Editor: nodes laid out readably, data maps set to Non-Color, and the render matches a hand-built material.

## Checked

2026-10-27 against the Blender 5.2 Python API (Material.use_nodes deprecated since 5.0, Nodes.new takes bl_idname, NodeLinks.new, MaterialSlot.link values 'OBJECT'/'DATA') and 5.2 node sources (Principled BSDF sockets Base Color, Roughness, Normal, Specular IOR Level, Coat Weight, Subsurface Weight, Emission Color, Emission Strength and output BSDF; Material Output Surface input; Normal Map Color/Normal; Image Texture Color output), plus the manual Preferences > Interface page (Python Tooltips). Removed the unconfirmed 4.0 rename list. Run check, 2026-11-01, Blender 4.5.14 LTS headless: the `pbr()` function ran with three generated PNGs (5 links, Principled/Output/3 Image Texture/Normal Map nodes); socket names Base Color, Roughness, Normal, Specular IOR Level, Coat Weight, Subsurface Weight, Emission Color, Emission Strength exist on the Principled BSDF and its output is BSDF; `keyframe_insert("default_value")` on a socket created an action; `check_existing=True` returned the same image; MaterialSlot.link is OBJECT or DATA. Unrun: the 5.0 deprecation of use_nodes, Python Tooltips preference, the render comparison in Verify.

Method: documentation checked against the 5.2 API pages; the code was run headless in Blender 4.5.14.
