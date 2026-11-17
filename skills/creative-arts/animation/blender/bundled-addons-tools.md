---
id: creative-arts.animation.blender.bundled-addons-tools
name: bundled-addons-tools
category: creative-arts
field: animation
product: blender
tags: [blender, bundled-addons, looptools, bool-tool, extra-objects, copy-attributes, measureit, 3d-print-toolbox, f2, edit-mesh-tools, sun-position, import-images-as-planes, node-arrange, modelling-addons, looptools-ops, extra-mesh-objects, extra-curve-objects, copy-attributes-menu, images-as-planes]
level: practitioner
status: draft
description: "The small official Blender tool add-ons a modeller uses daily: LoopTools, Bool Tool, Extra Objects, Copy Attributes, MeasureIt, 3D Print Toolbox, F2, Edit Mesh Tools, Mesh Plane, Sun Position."
sources:
  - https://extensions.blender.org/add-ons/looptools/
  - https://extensions.blender.org/add-ons/bool-tool/
  - https://extensions.blender.org/add-ons/extra-mesh-objects/
  - https://extensions.blender.org/add-ons/copy-attributes-menu/
  - https://extensions.blender.org/add-ons/print3d-toolbox/
  - https://docs.blender.org/manual/en/latest/addons/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bundled-addons-tools

Goal: know which of the official small add-ons to reach for, where they live in the UI, and their settings that matter. Since 4.2 most of these moved from "bundled" to the **Extensions platform** (still Blender-Foundation-maintained): install via Preferences → Get Extensions (`creative-arts.animation.blender.extensions-addons`).

## LoopTools (Edit mode → `Ctrl V` vertex menu / right-click → LoopTools; sidebar `N` → Edit → LoopTools)

- **Circle** — makes a selected loop circular (*Fit: Best/Inside*, *Radius*, *Regular* spacing, *Flatten*). Round windows, bolt holes, eye sockets.
- **Relax** — evens out vertex spacing along a loop/surface without changing shape much (*Interpolation: Cubic/Linear*, *Input*, *Iterations 1–25*, *Regular*). The retopo smoother.
- **Space** — equal spacing along the selected loop (keeps shape).
- **Flatten** — projects selection to a best-fit plane (*Plane: Best fit / Normal / View*).
- **Bridge / Loft** — bridges two loops with options (*Segments*, *Interpolation Cubic*, *Twist*, *Reverse*, *Cubic Strength*; Loft chains several loops; *Min width*). Better than native Bridge when loops differ in count: it handles unequal vertex counts.
- **Curve** — turns a selection into a smooth curve through chosen points (*Restriction*, *Regular*).
- **Gstretch** — stretches a loop to match a Grease Pencil/annotation stroke (draw a stroke, select loop, Gstretch → fits silhouettes from a drawing).
Gotcha: tools act on *selected loops*; closed vs open loops change behaviour; Relax with high iterations shrinks.

## Bool Tool (Object mode sidebar `N` → Edit → Bool Tool; `Ctrl Numpad +/−/*//` shortcuts)

- **Auto Boolean** (destructive): *Difference* (`Ctrl Numpad −`), *Union* (`Ctrl Numpad +`), *Intersect* (`Ctrl Numpad *`), *Slice* (`Ctrl Numpad /`) — active = target, other selected = cutters; cutters are deleted/applied.
- **Brush Boolean** (non-destructive): same ops but keeps the cutter as a live Boolean modifier with the cutter displayed as *Bounds/Wire* in a `Bool_Tool` collection; *Apply*/*Remove* per cutter; *Solver* Exact/Fast via the modifier; *Self Intersection*, *Hole Tolerant* on the modifier.
- Workflow for hard-surface: Brush Difference, keep cutters editable, apply before export (`creative-arts.animation.blender.hard-surface-modeling`). Cutter normals must point outward; apply scale on both.

## Extra Mesh Objects / Extra Curve Objects (`Shift A → Mesh/Curve → Extras`)

Parametric primitives: *Round Cube* (bevelled cube with *Arc Div*), *Gears*, *Gem*, *Pipe Joints*, *Honeycomb*, *Torus Knot*, *Math Function* (surface z = f(x,y) or parametric), *Regular Solids*, *Rock Generator*, *Teapot*, *Wall/Bricks*, *Steps/Stairs*, *Diamond*, *Beam Builder*, *Triangles*, *Supertoroid*, *Vertex/Single Vert* (the famous *Add Single Vert* for extrude-modelling). Curves: *Spirals*, *Profiles*, *Braid*, *Knots*, *Celtic links*, *Curly curves*, *Bevel/Taper profiles*, *Simple Curve* (polygons, arcs), *2D shapes*. All have redo panels (`F9`) — set parameters before leaving the operator.

## Copy Attributes Menu (`Ctrl C` in Object mode and Pose mode)

Object mode: copy from active to selected — *Location/Rotation/Scale*, *Visual Location*, *Drawing Options*, *Modifiers* (`Ctrl L` also does Modifiers), *Constraints*, *Object Collections*, *Selected Modifiers/Constraints*, *Font settings*, *Camera settings*, *UV Maps*, *Vertex Groups* (object data links are the native `Ctrl L` menu). Pose mode: copy *Pose Location/Rotation/Scale*, *Constraints*, *IK settings*, *Bone Shape*, *Bone Color*, *Local/Visual Transform* — the rigger's bulk-copy.

## MeasureIt (sidebar `N` → View → MeasureIt Tools)

Viewport dimension annotations: select two verts → *Segment* (distance), *Area*, *Angle*, *Arc*, *Label*, *Link* (between objects), *Origin*; styling (font size, colour, precision, units); *Show/Hide* toggle; **Render** measures into the image (needs *Render* tick). For reference images and client drawings; *Mesh Debug* shows vertex/edge/face indices and normals — a quick way to read indices for scripting.

## 3D Print Toolbox (sidebar `N` → 3D-Print)

Analyse: *Solid* (non-manifold/bad contiguous edges), *Intersections*, *Degenerate* (zero-area), *Distorted* (non-planar faces > angle), *Thickness* (walls thinner than X — colours faces), *Edge Sharp*, *Overhang* (angle). **Clean Up**: *Make Manifold*, *Distorted* (triangulate), *Isolated*. *Volume/Area* statistics, *Scale to Volume/Bounds*. Export (STL/OBJ/PLY/X3D) with *Scale* — mm for slicers. Run `Check All` before any print/Boolean-heavy export.

## F2 (Edit mode `F` enhanced)

Replaces/extends `F`: with one vertex selected, `F` creates a face from the surrounding edges intelligently (loop fill); with an edge selected it extrudes a quad; preferences *Auto Grab*, *Adjust UV*, *Extend Vert*. The retopologist's tool — `F` repeatedly to fill a quad strip.

## Edit Mesh Tools (Edit mode → *Mesh → Mesh Tools* / `N` panel)

Grab bag: *Offset Edges*, *Multi Extrude*, *Edge Fillet Plus*, *Random Vertices*, *Extrude Along Path*, *Vertex Align*, *Mesh Cut Faces*, *Split Solidify*, *Face Inset Fillet*, *Edge Roundifier*, *Pen Tool*, *Relax/Shrink-Fatten*, *Mesh to Wall*, *Select Tools* (*Checker select by angle*, *loops by edge count*…).

## Import Images as Planes (`Shift A → Image → Mesh Plane`, 4.2+ core: *Add → Image → Mesh Plane*)

Imports images as textured planes: *Material* (Principled/Shadeless/Emission), *Use Alpha* (blend mode), *Size: Absolute/Camera Relative/DPI/DPBU*, *Align to View/camera*, *Animate Image Sequences*, *Offset* for stacks — reference cards, billboard cutouts, 2.5D cutout backgrounds.

## Sun Position (World properties → Sun Position)

Puts a Sun light where the real sun is: *Latitude/Longitude* (or map), *Date/Time/UTC zone*, *Daylight Savings*; binds *Sun Object*, rotates an *HDRI* environment to match (*Sync Sun to Texture* with a *Bind Texture to Sun* on an environment image) and draws the sun path. Exterior lighting matches for archviz/VFX.

## Node Arrange (node editor `N` → Arrange)

*Arrange Nodes* (auto-layout a spaghetti tree), *Align Nodes*, *Node Spacing*; one click after importing materials from other apps. Pairs with `creative-arts.animation.blender.node-wrangler`.

## Others worth knowing

**AnimAll** (animate vertices/UVs/shape key points directly — `N` → Animate), **Storypencil** (GP storyboards → VSE), **Collection Manager** (`M` popup for collection visibility), **Modifier Tools** (apply/toggle all in one), **Carver**/**Hard Ops**-style cutting via *Knife Project* native, **Curve Tools**, **Simplify Curves+**, **Precision Drawing Tools (PDT)** (CAD-style numeric input), **Archipack/Archimesh** (parametric archviz), **Rigify** and **BlenRig** (rigging — `creative-arts.animation.blender.rigging`), **Ivy Generator**, **Sapling Tree Gen** (procedural trees), **Cell Fracture** (`creative-arts.animation.blender.destruction-rbd`), **Bsurfaces** (GP-stroke retopo), **Dynamic Sky**, **Magic UV**, **TexTools** (UV/baking), **Pose Library** legacy, **Mesh: Snap Utilities Line**, **Interface: Quick Favourites** (native). Each is an Extension or a core add-on; search the platform by name.

## Gotchas

- Many of these moved in 4.2: if a menu entry is missing, it's an Extension now (Bool Tool, LoopTools, Extra Objects, MeasureIt, Import Images as Planes → core *Mesh Plane*).
- LoopTools and native Bridge Edge Loops both exist; LoopTools has its own submenu — don't confuse their *Segments* options.
- Bool Tool Brush cutters live in a hidden collection; deleting the collection breaks modifiers.
- Copy Attributes requires the **active** object as source; it copies to all other selected.
- 3D Print Toolbox *Make Manifold* can weld things you didn't intend; check the result visually.

## Verify

- LoopTools → Circle on a messy 16-vert loop gives an exact circle; Relax ×3 evens spacing with no shrink beyond tolerance.
- Bool Tool Brush Difference leaves a live Boolean with the cutter in *Bool_Tool*; Apply bakes it, mesh manifold per 3D Print Toolbox *Solid*.
- Copy Attributes → Modifiers copies the stack to ten selected props identically.
- Sun Position with a known lat/long/time matches the HDRI's sun disc after *Sync Sun to Texture*.
