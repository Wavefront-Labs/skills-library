---
id: computing-software.game-programming.godot.multimesh-instancing
name: multimesh-instancing
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-performance, multimesh, gpu-instancing, multimeshinstance3d, foliage, game-programming]
level: practitioner
status: docs-checked
description: "Draw thousands of identical meshes in one call with MultiMesh/MultiMeshInstance2D/3D: setup, per-instance transforms, colors and custom data, visible counts and culling caveats."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html", "https://docs.godotengine.org/en/stable/classes/class_multimesh.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MultiMesh instancing

**Goal:** grass, crowds of simple units, asteroid fields and bullets rendered with one draw call.

## Setup (code)
```gdscript
@onready var mmi: MultiMeshInstance3D = $Grass

func _ready() -> void:
    var mm := MultiMesh.new()
    mm.transform_format = MultiMesh.TRANSFORM_3D
    mm.use_colors = true                       # per-instance color
    mm.use_custom_data = true                  # per-instance vec4 (INSTANCE_CUSTOM)
    mm.mesh = preload("res://grass_blade.mesh")
    mm.instance_count = 20000                  # set formats BEFORE instance_count
    for i in mm.instance_count:
        var pos := Vector3(randf_range(-50, 50), 0, randf_range(-50, 50))
        mm.set_instance_transform(i, Transform3D(Basis(Vector3.UP, randf() * TAU), pos))
        mm.set_instance_color(i, Color(0.4, randf_range(0.6, 0.9), 0.3))
        mm.set_instance_custom_data(i, Color(randf(), 0, 0, 0))     # e.g. wind phase
    mmi.multimesh = mm
```
- `visible_instance_count` (-1 = all) draws a prefix of instances: cheap way to grow/shrink pools.
- Bulk updates: `RenderingServer.multimesh_set_buffer(mm.get_rid(), packed_float32_array)` sets all instance data
  at once; see the MultiMesh `buffer` docs for the layout. Faster than per-instance calls each frame.

## Shader use
```glsl
shader_type spatial;
void vertex() {
    float phase = INSTANCE_CUSTOM.r * 6.28;
    VERTEX.x += sin(TIME * 2.0 + phase) * 0.1 * VERTEX.y;    // sway increases with height
}
void fragment() { ALBEDO = COLOR.rgb; }
```

## Culling caveat
A MultiMesh is culled as **one object** with one AABB: all or nothing. Split large fields into chunks (one
MultiMeshInstance per terrain cell) so off-screen chunks are culled.

## 2D
`MultiMeshInstance2D` with `TRANSFORM_2D` for swarms of sprites; give it a texture and a QuadMesh.

## Gotchas
- No per-instance collision or picking; keep gameplay data separately.

## Verify
- [ ] Frame debugger / monitors show draw calls dropped (one per chunk).
- [ ] Off-screen chunks are culled (visible object count drops when looking away).

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: MultiMesh class XML and the MultiMesh tutorial (`use_colors`, `use_custom_data`, set formats before `instance_count`, `visible_instance_count`, `multimesh_set_buffer`).
Removed: `INSTANCE_COLOR` shader name, the Populate Surface menu, 12-floats layout, `visibility_range_end`, instance_count clearing the buffer and the cast_shadow tip (none confirmed in fetched pages).
Method: documentation only; no commands were run.
