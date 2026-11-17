---
id: computing-software.game-programming.unity.ugui-canvas-rebuild-performance
name: ugui-canvas-rebuild-performance
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, ugui, canvas-rebuild, canvas-batching, ui-performance, profiler, game-programming]
level: advanced
status: draft
description: "Keep uGUI cheap: split canvases by update frequency, avoid layout and graphic rebuild cascades, disable raycast targets, and read Canvas.SendWillRenderCanvases in the profiler."
sources: ["https://unity.com/how-to/unity-ui-optimization-tips", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/UIBasicLayout.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# uGUI canvas rebuild performance

**Goal:** HUD costs well under 1 ms; changing one number doesn't rebuild the whole screen.

## How rebuilds work
A Canvas batches all its graphics into meshes. Any change to a child (text, color, size, enable)
marks the Canvas dirty and **re-batches the whole Canvas** (`Canvas.BuildBatch`), plus layout
rebuilds (`LayoutRebuilder`) up the hierarchy for Layout Groups and Content Size Fitters.

Profiler markers: `Canvas.SendWillRenderCanvases` (layout + graphic rebuild), `Canvas.BuildBatch`
(batching, can be on a worker), `Layout.Rebuild`, `Graphic.Rebuild`.

## Rules
1. **Split canvases by change rate**: static frame on one Canvas, a timer/ammo on a nested
   sub-canvas, health bars on another. Nested Canvases isolate rebuilds from their parent.
2. **Avoid Layout Groups on dynamic content**; they rebuild on any child change. Use them to lay out,
   then disable the component, or position via anchors.
3. **Turn off Raycast Target** on every non-interactive Graphic (fewer raycast candidates).
4. **Hide by disabling the Canvas component** (`canvas.enabled = false`), not `SetActive(false)`:
   disabling the GameObject destroys batches and triggers OnDisable/OnEnable rebuilds.
5. **Don't animate UI with the Animator** on large hierarchies: it dirties every frame even when
   values don't change. Tween only what moves.
6. **Text**: TextMeshPro; set text only when the value changes; `SetText("{0}", value)` avoids
   string allocation.
7. **Overdraw**: full-screen transparent images cost fill rate on mobile; check Scene view Overdraw
   mode. Use a Canvas Group alpha to fade whole panels.
8. World-space canvases for hundreds of health bars: batch into one canvas or render as sprites.

## Diagnose
- Frame Debugger: count UI draw calls; different materials/textures or interleaved depth break batches
  (use sprite atlases).
- Profiler > UI and UI Details modules show batch count and which canvas rebuilt.

```csharp
int last = -1;
void Update() { if (ammo != last) { last = ammo; ammoText.SetText("{0}", ammo); } }
```

## Verify
- [ ] Idle HUD: no `Canvas.SendWillRenderCanvases` spikes when nothing changes.
- [ ] Changing a counter only rebuilds its sub-canvas (UI Details module).
