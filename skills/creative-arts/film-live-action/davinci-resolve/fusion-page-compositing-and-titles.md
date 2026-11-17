---
id: creative-arts.film-live-action.davinci-resolve.fusion-page-compositing-and-titles
name: fusion-page-compositing-and-titles
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, fusion, fusion-page, fusion-compositing, compositing, node-graph, mediain, mediaout, merge-node, transform, planar-tracker, tracker-node, camera-tracker, delta-keyer, keying, ultra-keyer, paint-node, clone, clean-plate, rotoscoping, polygon-mask, b-spline, magic-mask-fusion, text-plus, fusion-titles, title-templates, macros, fusion-templates, lower-thirds, screen-replacement, corner-pin, split-screen, sky-replacement, wire-removal, color-space-in-fusion, fusion-cache, render-in-place, fusion-nodes, merge-node-use, fusion-flow, delta-keyer-use, fusion-keying, fusion-green-screen, fusion-tracking, camera-tracker-use, fusion-roto, paint-node-use, polygon-roto, text-plus-animation, fusion-text-animation, title-animation, fusion-macros, macro-creation, fusion-template-build, fusion-cleanup, object-removal-fusion, wire-removal-fusion]
level: practitioner
status: draft
description: "Use the Fusion page for the comps an editor needs: node basics, planar tracking for screen replacement, Delta Keyer keys, paint and roto cleanups, Text+ titles and macros saved as templates."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Definitive Guide to DaVinci Resolve - Fusion chapters; Fusion Visual Effects book)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Fusion section)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fusion page: compositing and titles

**Goal:** fix the shot and build the title inside the Resolve timeline, with a node
graph you can read next week, instead of round-tripping to After Effects for every
screen insert.

## 1. Orientation
Select a clip on the Edit page > Fusion page. The graph starts as `MediaIn1 -> MediaOut1`.
- Nodes connect **background (yellow)** and **foreground (green)** inputs; a **Merge**
  puts FG over BG. **Mask (blue)** inputs limit effects.
- Viewers: drag a node to viewer 1/2 (or press `1`/`2`). `Shift+Space` adds a node by
  search. `Ctrl/Cmd+T` Transform, `Ctrl/Cmd+Space`... learn the search.
- Inspector edits the selected node; keyframe with the diamond; the **Spline** and
  **Keyframes** editors adjust animation curves.
- Fusion works in the timeline's colour space by default; for linear-light comps set
  `Fusion Settings > ... ` or use **Color Space Transform** nodes to linear and back.
  Grades applied on the Color page come *after* Fusion.
- Fusion is per clip; to comp across clips, make a **Fusion Composition** (Effects >
  Fusion Composition) or compound clip first.

## 2. Screen replacement (planar tracking)
1. Add **Planar Tracker** after MediaIn; draw a polygon over the screen/sign, set
   *Pattern* to *Hybrid*, *Track to End*. Check for slips at the edges; add *Reference*
   frames on occlusions.
2. In the tracker: *Operation Mode: Corner Pin*; connect the new image (MediaIn2 - add
   via Media Pool drag) to the corner-pin input; adjust the corners on the reference frame.
3. **Merge** the result over the original. Add a soft **Polygon** mask to hold back
   fingers/foreground; blur/match grain (`Film Grain` node) and screen glow (`Soft Glow`).
Camera Tracker (3D solve) is for adding elements into moving-camera space; use when
planar fails because the surface isn't flat.

## 3. Keying
**Delta Keyer**: pick the screen colour with the eyedropper (view the *Matte* in
the viewer), tune *Gain/Balance*, use *Pre-Matte* for coarse cleanup, **Matte** tab
for low/high clipping and *Erode/Blur*, **Fringe** for spill. Add a **Clean Plate**
node before the keyer for uneven screens. Garbage-matte with a Polygon on the keyer's
mask input. Ultra Keyer for quick jobs. Despill then colour-match the FG with
**Color Corrector** before the Merge. Preview against a checkerboard.

## 4. Paint, roto and cleanups
- **Paint** node with *Clone* stroke (set the source offset) to remove wires, marks,
  sensors; *Stroke* mode with *Apply mode: Clone* and track the paint with a Tracker
  (connect Tracker to Paint > Position) for moving shots.
- Rotoscoping: **Polygon** or **B-Spline** masks; animate shape keyframes every few
  frames; feed into a Merge's mask or a Color Corrector to isolate. **Magic Mask** on
  the Color page is often faster for people; Fusion roto when you need clean edges.
- **Sky replacement**: Luma/Delta key the sky, track a sky plate with Tracker > Match
  Move, merge with a soft edge, match colour.
- **Split screens** (two takes of one shot): two MediaIns, a Polygon mask on the Merge,
  track if the camera moves.

## 5. Titles and Text+
Edit page > Effects > Titles > **Text+** is a Fusion node: typography (*Text*, *Layout*,
*Transform*, *Shading* tabs - outlines, shadows, fills); animate with the *Follower*
modifier (per-character animation: right-click text > *Follower*) or Text+ animation
presets. Build lower thirds as a Fusion comp (Text+, Background, Merge, animated
Transform) and **save as a Macro** (`select nodes > right-click > Macro > Create Macro`,
expose the controls you want, save to `Templates > Edit > Titles`) - it appears in
the Edit page Effects as a reusable title with Inspector controls.

## 6. Performance
Set `Fusion > Fusion Settings` memory; use **Render Cache** on the Edit page
(right-click clip > *Render Cache Fusion Output > On*) or **Render in Place**
(right-click > Render in Place) to bake heavy comps to media while keeping the
original on a track below.

## Gotchas
- Working in a gamma-encoded space for blurs/merges; halos and dark edges - go linear for compositing.
- Forgetting the Merge's `Apply Mode` and `Alpha Gain` when FG has premultiplied alpha.
- A planar track checked only at the start; it slid at frame 200.
- Text+ built with a non-licensed font; missing on the colourist's machine.
- Comps rendering every playback; cache or render in place before the review.

## Verify
- [ ] Node graph reads left to right with labelled nodes; MediaOut last.
- [ ] Tracks checked through the whole shot; masks hold back foreground.
- [ ] Keys reviewed on the matte view and against checkerboard; spill handled.
- [ ] Titles saved as macros; heavy comps cached before review.
