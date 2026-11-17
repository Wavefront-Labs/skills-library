---
id: computing-software.game-programming.godot.visual-shaders
name: visual-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-shaders, visual-shader, node-based-shaders, visualshadernodecustom, game-programming]
level: intro
status: docs-checked
description: "Build Godot visual shaders: graph types and outputs, parameters, common node recipes, expression and custom nodes, and when to convert to text shaders."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html", "https://docs.godotengine.org/en/stable/classes/class_visualshadernodecustom.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visual shaders

**Goal:** artists build and tweak shaders with nodes, with reusable custom nodes for team-specific maths.

## Setup
New `ShaderMaterial` > Shader > New **VisualShader** (Create Shader dialog, Type = VisualShader); modes
mirror Shader.Mode: Spatial, CanvasItem, Particles, Sky, Fog. The toolbar's shader type drop-down
switches between Vertex, Fragment and Light, which changes the built-in nodes available. Each has an
**Output** node with ports matching the text shader built-ins (Albedo, Alpha, Emission, Normal Map...).

## Parameters
Add Parameter nodes (FloatParameter, ColorParameter, Texture2DParameter): they become uniforms with
names, hints and defaults, editable on the material and settable via `set_shader_parameter`.

## Recipes
- **Scrolling texture**: Input `TIME` × Vector2 speed + `UV` -> Texture2D UV.
- **Fresnel rim**: `Fresnel` node (power) × color -> Emission.
- **Dissolve**: noise texture R -> `Step`/`SmoothStep` against parameter -> Alpha (with alpha scissor) + edge
  emission.
- `Expression` node: write shading-language expressions inline with ports you define (usable in all
  shader modes) instead of building node chains.

## Custom nodes (reusable)
```gdscript
@tool
class_name VisualShaderNodeRemap extends VisualShaderNodeCustom
func _get_name() -> String: return "Remap"
func _get_category() -> String: return "MyNodes"
func _get_return_icon_type() -> PortType: return PORT_TYPE_SCALAR
func _get_input_port_count() -> int: return 5
func _get_input_port_name(p: int) -> String: return ["value", "in_min", "in_max", "out_min", "out_max"][p]
func _get_input_port_type(_p: int) -> PortType: return PORT_TYPE_SCALAR
func _get_output_port_count() -> int: return 1
func _get_output_port_name(_p: int) -> String: return "result"
func _get_output_port_type(_p: int) -> PortType: return PORT_TYPE_SCALAR
func _get_code(i: Array[String], o: Array[String], _m: Shader.Mode, _t: VisualShader.Type) -> String:
    return "%s = %s + (%s - %s) * (%s - %s) / (%s - %s);" % [o[0], i[3], i[4], i[3], i[0], i[1], i[2], i[1]]
```
Appears in the Add Node menu under the category.

## Visual vs text
- Visual: discoverable, artist-friendly, live previews per node.
- Text: easier for complex logic and loops. The editor's show-generated-code button displays the text
  shader a graph produces (the graph is converted to a script shader behind the scenes).
- Large graphs become hard to review; keep them small with custom nodes and Expression nodes.

## Verify
- [ ] Parameters exposed with sensible ranges; material instances tweak them without editing the graph.
- [ ] Custom node library works for all team members (scripts committed, @tool).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: creating a VisualShader through the Create Shader dialog; Vertex, Fragment and Light shader types in the toolbar; Shader.Mode values (spatial, canvas_item, particles, sky, fog); Fresnel and Expression nodes; the `VisualShaderNodeCustom` virtual methods used in the example (`_get_name`, `_get_category`, `_get_return_icon_type`, `_get_input_port_count/name/type`, `_get_output_port_count/name/type`, `_get_code(input_vars, output_vars, mode, type)`); `VisualShaderNodeFloatParameter` is translated to `uniform float`. Removed the unconfirmed triplanar-node and Convert-to-Shader claims.

Method: documentation only; no commands were run.
