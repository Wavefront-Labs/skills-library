---
id: creative-arts.animation.vector-graphics.shapes-paths
name: shapes-paths
category: creative-arts
field: animation
product: vector-graphics
tags: [vector, vectorcraft, shapes, paths, bezier, svg, inkscape, blender-curves, 2d, logo, hud, title, graphics]
level: advanced
status: draft
description: "Vector and bezier craft for 2D elements, logos, titles and HUD: primitives, path/booleans, SVG, Inkscape/Blender curves, converting vector to geometry."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: vectorcraft — shapes, paths, and vector-to-geometry craft

**What it is:** resolution-independent 2D built from math, not pixels — the right tool
for logos, titles, HUD/analog overlays, UI, icons, and flat 2D assets that must stay
crisp at any size. Our headless engine is an Illustrator-like CLI `vectorcraft-cli.exe`
(built to `<CRAFT_BIN>/`) that emits SVG; the same craft applies in Inkscape and to
Blender curves. This skill is the *craft* under the mechanism: how to think in paths,
not just how to call the tool.

## 1. When 2D vector beats 3D (choose this first)
Reach for vector instead of modelling/rendering when:
- the element is **flat and graphic** — a title card, a lower-third, a logo, an icon, a
  HUD readout, a hand-painted sign, the metered counter overlay;
- it must stay **razor-crisp at any scale** (titles over 4K, UI that zooms);
- it's **screen-space**, not world-space — it sits on top of the picture, not inside
  the lit set;
- **iteration speed** matters: re-colour, re-type, re-layout in seconds vs a re-render.
Reach for 3D when the element lives in the lit, camera-moved world. Rule of thumb: if a
camera move would cause parallax on it, it's 3D; if it rides flat on the comp, it's
vector. (Vector pieces then composite in over the render — see effectcraft/titles-hud.)

## 2. The vectorcraft mechanism (headless)
```bash
V="<CRAFT_BIN>/vectorcraft-cli.exe"
"$V" run --cmd <ID> --params '<JSON>' [--cmd ... --params ...] --export out.svg
"$V" convert out.svg out.png --scale 2        # rasterize crisp
```
- Multiple `--cmd/--params` pairs chain in order into one document.
- **CRITICAL: inline JSON must use forward-slash paths.** It rejects backslash escapes
  (`\`). Write Windows paths as `<DRIVE>:/dir/file`.
- Drive it from Python with `subprocess` + `json.dumps(params)` (avoids quoting hell);
  write the Python with the Write tool, not bash heredocs.

## 3. Primitives, paths, and the bezier mental model
- `file.new` → `{"width":1920,"height":1080,"units":"Pixels","backgroundContents":"transparent"}`
- `shape.rectangle` → `{"x","y","width","height","radius"?,"rotation"?}`
- `shape.ellipse` → `{"x","y","width","height"}` (x,y = top-left of bbox)
- `shape.star` / `shape.polygon` → center + radius/points
- `path.create` → `{"closed":true|false,"d":"M x y L x y C c1x c1y c2x c2y x y Z"}`

**Think in anchors + handles.** An SVG/bezier path is anchor points joined by segments;
curved segments carry *handles* (control points) that pull the curve. Core `d` commands:
- `M x y` move (pen up, start a new subpath); `L x y` line; `Z` close.
- `C c1x c1y c2x c2y x y` cubic bezier (two handles → smoothest, most control);
  `Q cx cy x y` quadratic (one handle); `A` arc.
Craft rules that separate clean vector art from lumpy:
- **Fewest anchors that describe the form.** Every extra anchor is a place the curve can
  kink. Put anchors at *extrema* (top/bottom/left/right of a curve) and at corners,
  nowhere else.
- **Handles ~1/3 the segment length**, tangent to the curve, for even "G1/G2"
  continuity. Mirror handle directions across an anchor for a smooth pass-through; break
  them for a deliberate corner.
- **Close shapes with `Z`**, don't overshoot the start point — an unclosed near-loop
  leaves a hairline gap that shows when filled.

## 4. Paint, stroke, and booleans
- `paint.setFill` applies to the **last created shape**:
  `{"color":"#rrggbb"}` or
  `{"gradient":{"kind":"linear|radial","angle":90,"stops":[{"offset":0,"color":"#..","opacity":1},...]}}`.
- Shapes carry a **default black stroke** → free cartoon outlines; rely on it for toon
  art, override when you don't want it. Keep stroke weight consistent across a set of
  icons so they read as one family.
- **Boolean/path ops** are how complex shapes are really built: union to weld, subtract
  to punch holes (a ring = big circle minus small circle), intersect to clip. Build
  compound forms from simple primitives booleaned together rather than hand-drawing a
  hard outline — fewer anchors, cleaner result.

## 5. Working pattern (helper funcs in Python)
```python
import json, subprocess
V = r"<CRAFT_BIN>/vectorcraft-cli.exe"
def run(cmds, out):
    a = [V, "run"]
    for c, p in cmds: a += ["--cmd", c, "--params", json.dumps(p)]
    a += ["--export", out + ".svg"]; subprocess.run(a, capture_output=True)
    subprocess.run([V, "convert", out + ".svg", out + ".png", "--scale", "2"], capture_output=True)
def rect(c,x,y,w,h,col,r=0): c.append(("shape.rectangle",{"x":x,"y":y,"width":w,"height":h,**({"radius":r} if r else {})})); c.append(("paint.setFill",{"color":col}))
def ell(c,x,y,w,h,col):      c.append(("shape.ellipse",{"x":x,"y":y,"width":w,"height":h})); c.append(("paint.setFill",{"color":col}))
def path(c,d,col,closed=True): c.append(("path.create",{"closed":closed,"d":d})); c.append(("paint.setFill",{"color":col}))
c = [("file.new",{"width":1920,"height":1080,"units":"Pixels","backgroundContents":"transparent"})]
# ...build back-to-front...
run(c, "<OUT_DIR>/title")
```

## 6. Logos, titles, and HUD (the real deliverables)
- **Logo/title:** design on a grid, lock an optical centre (not the geometric one —
  heavy shapes read low, so nudge up). Keep a tight, consistent stroke weight; build
  letterforms or marks from booleaned primitives so they stay editable. Export a
  transparent SVG master + 2× PNG for compositing.
- **HUD / analog overlay:** a HUD is a kit of aligned parts (frame, ticks, a numeric
  readout, a needle). Keep the **same canvas size per part** so they overlay pixel-exact
  when stacked or animated — don't crop to content. Emissive/bright fills for the "live"
  elements (the counter, the green seam). Lay out on a baseline grid so numbers don't
  jitter between frames.
- Animate screen-space vector overlays in effectcraft over the render; keep the vector
  source as the editable master.

## 7. Curves in Blender & Inkscape; vector → geometry
Vector art crosses into 3D two ways:
- **Import SVG into Blender** (`bpy.ops.import_curve.svg`) → it arrives as curve objects.
  `Convert to Mesh` or add **Extrude/Bevel** on the curve to turn a logo/sign into real
  geometry you can light in the set (a storefront sign, a 3D title). Set the curve's
  `fill_mode` before converting or an open path won't cap.
- **Inkscape** is the interchange hub: clean/simplify paths (`Path → Simplify` to cut
  anchors), convert text/strokes to paths (`Object to Path`, `Stroke to Path`) so the
  file is self-contained, boolean ops (`Path → Union/Difference/Intersection`), then
  save as plain SVG for Blender or vectorcraft. Converting stroke-to-path before export
  avoids width-scaling surprises downstream.
- **Gotcha:** many engines fill by even-odd/nonzero winding — a hole subpath must wind
  *opposite* the outer path or the "hole" fills solid. If a counter (the hole in an "o")
  fills in, reverse that subpath's direction.

## 8. Expert tips
- Draw back-to-front (painter's order); later shapes cover earlier.
- `--scale 2`+ on convert for crisp antialiased raster.
- Rotations are degrees; `line(x1,y1,x2,y2,w)` = a rotated thin rounded rect.
- Store reusable draw helpers per character/UI family so a sheet re-renders identically.

## Verify
- [ ] Element is genuinely flat/screen-space (else it should be 3D).
- [ ] Paths use the fewest anchors, placed at extrema/corners; all closed with `Z`.
- [ ] Shapes build from booleaned primitives where possible; stroke weight consistent
      across a family.
- [ ] HUD/overlay parts share one canvas size and overlay pixel-exact.
- [ ] SVG master exported transparent; raster via `convert --scale 2`+.
- [ ] On vector→mesh: fill/winding correct (no filled counters), curve capped as intended.

See also: `../scripting/scripting-basics.md` (SVG import in bpy), titles-hud,
`character-sheets.md`, `paint-gradients.md`, `export-convert.md`.
