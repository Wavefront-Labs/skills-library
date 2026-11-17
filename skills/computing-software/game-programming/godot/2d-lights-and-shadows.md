---
id: computing-software.game-programming.godot.2d-lights-and-shadows
name: 2d-lights-and-shadows
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, pointlight2d, directionallight2d, lightoccluder2d, canvasmodulate, 2d-lighting, game-programming]
level: practitioner
status: docs-checked
description: "Light 2D Godot scenes with PointLight2D and DirectionalLight2D, LightOccluder2D shadows, CanvasModulate darkness, normal maps on sprites, and light masks."
sources: ["https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html", "https://docs.godotengine.org/en/stable/classes/class_pointlight2d.html", "https://docs.godotengine.org/en/stable/classes/class_lightoccluder2d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 2D lights and shadows

**Goal:** a dark dungeon lit by torches with sprites casting shadows.

## Pieces
- **CanvasModulate**: tints the whole canvas (set to dark blue-grey) so lights have something to
  brighten.
- **PointLight2D**: needs a `texture` (radial gradient texture works: GradientTexture2D fill Radial);
  `texture_scale`, `energy`, `color`, `blend_mode` (Add, Subtract, Mix).
- **DirectionalLight2D**: sun/moon light across the whole scene; `height` affects normal mapping.
- **LightOccluder2D** with an `OccluderPolygon2D` (draw in the editor or TileSet occlusion layers):
  casts shadows when the light's **Shadow > Enabled** is on.

## Shadows
On the light: `shadow_enabled`, `shadow_color`, `shadow_filter` (None, PCF5, PCF13) and
`shadow_filter_smooth` for soft shadows. TileMapLayer: add an occlusion layer in the TileSet and draw
occluders per tile.

## Normal and specular maps
Use `CanvasTexture` on Sprite2D: diffuse + normal + specular textures; lights then shade bumps.
Light `height` sets the light's virtual Z for normal calculations.

## Masks
`range_item_cull_mask` (which items a light affects) vs CanvasItem `light_mask`; `shadow_item_cull_mask`
vs occluder `occluder_light_mask`. Use to keep UI or foreground layers unlit.

## Performance
Many overlapping lights with shadows cost frame time. Limit shadowed lights, use smaller ranges, or fake glows with additive sprites.

## Gotchas
- Lights affect only items on the same CanvasLayer (and via `range_layer_min/max` z ranges).
- Unshaded materials (`CanvasItemMaterial.light_mode = Unshaded`) ignore lights, good for UI-like
  elements in the world.
- Pixel art: set light texture filter to nearest and keep shadow filter None for crisp edges.

## Verify
- [ ] Scene reads correctly at target darkness; frame time with all lights on is within budget.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed in the 2D lights tutorial and Light2D/LightOccluder2D class XML: `range_item_cull_mask`, `shadow_item_cull_mask`, `range_layer_min/max`, `shadow_color`, `shadow_filter`, `shadow_filter_smooth`, `occluder_light_mask`.
Removed: `cull_mode` (not found on the fetched pages), the one-CanvasModulate-per-layer rule and the mobile cost claim.
Method: documentation only; no commands were run.
