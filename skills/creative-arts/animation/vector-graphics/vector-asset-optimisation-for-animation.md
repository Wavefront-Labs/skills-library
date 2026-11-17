---
id: creative-arts.animation.vector-graphics.vector-asset-optimisation-for-animation
name: vector-asset-optimisation-for-animation
category: creative-arts
field: animation
product: vector-graphics
tags: [vector, vector-graphics, optimisation, svg, svgo, path-simplification, file-weight, real-time-engine, game-engine, lottie, after-effects, inkscape, curve-reduction, import-performance, performance-budget]
level: practitioner
status: draft
description: "Optimise vector exports (SVG/curves) for animation pipelines: path simplification, SVGO cleanup, Lottie/JSON weight, and real-time engine import budgets."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector asset optimisation for animation

**What it is:** making a vector asset lean *after* it's already correct and rigged —
file weight, point count, and import/render cost — so a shot or a real-time engine
doesn't choke on it. This is downstream of `shapes-paths` (building the art) and
`vector-rigging-for-2d-animation` (posing it); optimisation never changes what the
asset looks like at rest, only what it costs to move, load, and render. If you find
yourself redrawing the art to optimise it, you've wandered into the wrong skill.

## 1. Know which cost you're actually paying
Three different budgets, often confused:
- **File weight** (disk/network) — matters for web delivery (an SVG icon set loaded
  in a browser) and for Lottie/JSON animation files shipped to a mobile app.
- **Path complexity** (anchor/point count) — matters for *render* cost: a renderer
  (SVG rasterizer, a game engine's vector-to-mesh tessellator, After Effects'
  shape-layer evaluation) re-walks every anchor every frame something on that path
  animates. More anchors on an animated path = more per-frame cost, independent of
  file size.
- **Import/parse cost** — matters at *load* time: a scene with hundreds of separate
  small SVGs each importing as its own draw call/object is slower to open and heavier
  at runtime (more objects for the engine to manage) than fewer, merged assets, even
  if the total point count is identical.
Pick the fix that targets the actual bottleneck — simplifying paths doesn't help a
too-many-draw-calls problem, and merging objects doesn't help a too-many-anchors-on-
one-path problem.

## 2. Path simplification (the SVGO / "Simplify" pass)
- **Inkscape:** `Path → Simplify` (Ctrl+L) reduces anchor count while preserving the
  curve shape within a tolerance; run it once after drawing, and again after any
  boolean op (unions/subtracts tend to leave redundant collinear points at the seam).
  Pressing it repeatedly on the same path keeps simplifying — watch for the shape
  visibly degrading and back off.
- **SVGO** (`npx svgo input.svg -o output.svg`) is the standard CLI/Node tool for
  automated SVG optimisation in a build pipeline: it strips editor metadata
  (Inkscape/Illustrator namespaces, empty groups, comments), collapses redundant
  transforms, rounds coordinate precision, and merges paths where safe. Typical web
  icon SVGs shrink 40–70% with no visible change at `--precision 2` or `3` decimal
  places — **gotcha:** dropping precision too far (0–1) visibly chips corners and
  breaks pixel-snapped alignment in small icons; check at actual display size, not
  zoomed in.
- **Don't simplify an asset that's about to be rigged/mesh-deformed** before deciding
  final anchor placement — simplification can relocate anchors away from the joint
  lines you need for clean mesh weighting (see `vector-rigging-for-2d-animation`
  section 1). Simplify raw art, then re-check anchor placement at joints before
  rigging; or rig first and simplify only the parts that stay rigid.
- Coordinate precision and transform flattening matter more than they look: a chain
  of nested group transforms (common from Illustrator/AE exports) costs real parse
  time to resolve on every frame of playback; SVGO's `convertTransform` /
  `collapseGroups` plugins flatten this once, offline, instead of at runtime.

## 3. File weight for delivery (web / Lottie / mobile)
- **Strip what the viewer never needs:** editor metadata, hidden/unused layers,
  unreferenced `<defs>`, and (for icon sets) duplicate near-identical paths that
  should be one symbol referenced via `<use>` instead of N copies.
- **Lottie (Bodymovin export from After Effects):** the JSON balloons fast from (a)
  too many keyframes on a property that could ease with far fewer, (b) masks/mattes
  (expensive to evaluate on mobile renderers — avoid where a boolean path op at
  export time would do), and (c) embedded raster images smuggled into an otherwise-
  vector file (check — these defeat the entire point of using Lottie and bloat the
  JSON hugely). Thin keyframes with AE's built-in keyframe reduction before export,
  not after — cleaning JSON by hand is a trap.
- **Gotcha I've hit:** Lottie players vary in which SVG/AE features they actually
  support (some gradients, some blend modes, some expressions silently fail). Test
  the actual exported file in the actual target player (lottie-web, a native iOS/
  Android player) before calling an asset done — "it looked right in AE" is not
  verification. This cross-player gap is **unconfirmed in detail by me beyond having
  been bitten by it once** — re-check current player support tables per project.

## 4. Real-time engine / game-engine budgets
- Vector art entering a real-time engine (Unity's Vector Graphics package, a custom
  SVG-to-mesh importer) gets **tessellated into triangles at import or runtime** — a
  curve with more anchors and a higher tessellation tolerance setting produces more
  triangles. Set the lowest tessellation tolerance that still looks clean at the
  asset's *actual on-screen size* — a HUD icon rendered at 64px doesn't need the
  triangle density a full-screen logo does.
- **Batch draw calls:** many separate small vector objects each cost a draw call;
  where the engine supports it, pack icon/UI sets into a single atlas or merge static
  (non-independently-animated) shapes into one mesh at build time. Reserve separate
  objects for parts that genuinely animate independently.
- Static vector backgrounds/props that never deform are often cheaper **pre-baked to
  a raster/sprite** at the target resolution than kept as live vector + tessellation
  cost every frame — vector's resolution-independence is wasted if the camera
  distance never changes.

## 5. A practical checklist order
1. Finish the art and rigging first (optimisation is a cleanup pass, not a drawing
   constraint) — see `vector-rigging-for-2d-animation`.
2. Flatten transforms, strip metadata (SVGO or Inkscape save-as-plain-SVG).
3. Simplify paths that are NOT load-bearing for rigging (background/static elements
   first; animated-rig parts last and carefully).
4. For delivery: re-check file size and, for Lottie, keyframe count and masks.
5. For real-time: set tessellation tolerance against actual on-screen size, batch
   draw calls, pre-bake truly static elements to raster.
6. Re-verify visually at 100% / actual target size after every automated pass —
   automated simplifiers occasionally produce a subtly wrong curve on a complex
   boolean result; a diff-by-eye at final size catches it cheaply.

## Verify
- [ ] Identified which budget (file weight, path complexity, import/draw-call count)
      is actually the bottleneck before picking a fix.
- [ ] Ran path simplification (Inkscape Simplify or SVGO) and visually diffed the
      result at actual display size, not just zoomed in.
- [ ] For Lottie: checked keyframe count, masks/mattes, and absence of smuggled
      raster images; test-played the exported file in the real target player.
- [ ] For real-time import: tessellation tolerance set against actual on-screen size,
      not a default; static non-animated elements considered for pre-baking to raster.
- [ ] Optimisation pass happened AFTER art/rig were finalised, and anchor placement
      at rig joints was re-checked if simplification ran before rigging.

See also: `shapes-paths.md` (the art this optimises), `vector-rigging-for-2d-
animation.md` (poseability constraints on which anchors can move),
`svg-pipeline-for-motion-graphics.md` (runtime SVG for motion graphics — a
different consumer with its own weight/perf concerns).
