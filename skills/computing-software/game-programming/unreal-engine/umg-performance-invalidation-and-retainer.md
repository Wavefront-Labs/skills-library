---
id: computing-software.game-programming.unreal-engine.umg-performance-invalidation-and-retainer
name: umg-performance-invalidation-and-retainer
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, umg, invalidation-box, retainer-box, global-invalidation, slate-performance, widget-reflector, volatile, ui-optimization, game-programming]
level: advanced
status: draft
description: "Optimise Unreal UMG: removing bindings and ticks, Invalidation Boxes and global invalidation, volatile widgets, Retainer Boxes, and measuring with stat slate."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/optimization-guidelines-for-umg-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/invalidation-in-slate-and-umg-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-slate-widget-reflector-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG performance: invalidation and retainer boxes

**Goal:** HUD and menus costing well under a millisecond of game thread time, even with many widgets.

## Measure first
- `stat slate` and `stat ui` for Slate tick/paint/prepass time; Unreal Insights with the Slate trace
  channel (`-trace=default,slate`) for per-widget detail.
- Widget Reflector (Tools > Debug > Widget Reflector): pick widgets, see hierarchy, toggle
  "Show invalidation" / paint-time visualisation.

## Remove per-frame work
1. **Property bindings** (Bind dropdown) evaluate every frame. Replace with event-driven setters (see
   unreal-engine umg-cpp-widgets-with-bindwidget).
2. Widget **Tick** (Event Tick in WBP / `NativeTick`): disable when not needed; set the widget's Tick
   Frequency to Never in the class defaults when it has no tick logic.
3. Collapse (`ESlateVisibility::Collapsed`) instead of Hidden for widgets not shown: Hidden still
   takes part in layout (prepass).
4. Avoid deep nesting of panels; large Canvas Panels are expensive (each child is a draw layer).
   Prefer Overlay/Horizontal/Vertical boxes.

## Invalidation
- **Invalidation Box**: caches the layout and paint of its children; they are only re-laid out or
  repainted when invalidated (a child changes). Wrap static or rarely changing parts (frames, menus).
- **Global Invalidation** (`Slate.EnableGlobalInvalidation 1`, project setting) applies the same idea
  to the whole widget tree; any widget that changes every frame must then be marked **Volatile**
  (`bIsVolatile` / "Is Volatile" checkbox) or it causes full invalidations.
- Widgets with per-frame animation inside an Invalidation Box also need Volatile, or move them outside.
- Check effectiveness: `Slate.InvalidationDebugging` and Insights counts of invalidated widgets per
  frame.

## Retainer Box
Renders its children to a render target at a set phase/frequency (e.g. every 4th frame) and draws the
texture otherwise. Good for complex widgets that can update at lower rates (minimaps, decorative
panels) and for applying a material effect to a whole widget group. Costs render target memory;
text may blur if scaled.

## Other wins
- Pool list entries: `ListView`/`TileView` with entry widget recycling instead of creating a widget per
  item in a ScrollBox.
- Font atlases: limit font sizes and families; enable distance field fonts where appropriate.
- Lazy-create menus on first open; keep the HUD minimal on mobile.

## Verify
- [ ] `stat slate` game-thread UI time under budget (e.g. < 0.5 ms) during gameplay.
- [ ] No WBP uses property bindings (asset audit).
- [ ] Insights shows near-zero invalidations per frame on static screens.
