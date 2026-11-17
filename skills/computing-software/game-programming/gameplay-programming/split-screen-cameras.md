---
id: computing-software.game-programming.gameplay-programming.split-screen-cameras
name: split-screen-cameras
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, camera-systems, split-screen-camera, local-multiplayer, viewport-rect, dynamic-split-screen, game-programming]
level: practitioner
status: draft
description: "Implement split-screen cameras: viewport layouts per player count, per-player UI and audio listeners, dynamic Voronoi-style splits, and the performance budget it costs."
sources: ["https://docs.unity3d.com/ScriptReference/Camera-rect.html", "https://docs.godotengine.org/en/stable/classes/class_subviewport.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UGameViewportClient"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Split-screen cameras

## Layouts
| Players | Layout |
|---|---|
| 2 | horizontal halves (wide view, best for racing) or vertical halves (taller view, better for 16:9 action) |
| 3 | 2+1 (one wide on top) or 4-quad with an empty/map quadrant |
| 4 | quadrants |
Keep each view's aspect sensible; a 32:9 sliver needs a wider FOV (adjust horizontal FOV, not vertical).

## Engine setup
- **Unity:** one Camera per player with `camera.rect = new Rect(0, 0.5f, 1, 0.5f)` etc. `PlayerInput`
  + `PlayerInputManager` with *Split-Screen* enabled assigns rects automatically. URP: each camera
  renders the full pipeline; overlay cameras stack per base camera.
- **Unreal:** local players via `UGameplayStatics::CreatePlayer`; the GameViewportClient's split-screen
  type (Project Settings > Maps & Modes > Local Multiplayer) sets the layout.
- **Godot:** a `SubViewportContainer` + `SubViewport` per player with its own `Camera3D`; share the
  world by setting each SubViewport's `world_3d = get_viewport().world_3d`.

## Per-player concerns
- **UI:** each player's HUD is scoped to their viewport (Unity canvas Screen Space - Camera per camera;
  Unreal per-player widgets via `AddToPlayerScreen`; Godot HUD inside each SubViewport).
- **Audio:** one listener only in most engines; options: listener at the midpoint, at player 1, or
  custom per-player panning. Pick deliberately.
- **Culling/LOD:** distance LOD per camera; avoid objects popping when one player looks at them.
- **Input:** device-to-player assignment and a join screen; disconnect/reconnect mid-game.

## Dynamic (Voronoi) split screen
Single view while players are close; split along the perpendicular bisector between them when the
distance exceeds a threshold, rotating the split line with their relative direction. Render each
camera to a texture and composite with a mask; blend the split line width in to avoid a pop.

## Performance
Each view re-runs culling, shadows and post-processing: budget roughly 1.6-1.9x frame cost for 2
players, more for 4. Common cuts: lower render scale per view, shorter shadow distance, fewer
dynamic lights, cheaper post FX in split mode.

## Verify
- [ ] Join/leave mid-session re-lays out views without a hitch.
- [ ] HUD elements never draw into another player's view.
- [ ] Frame time with max players stays within target on the lowest supported hardware.
