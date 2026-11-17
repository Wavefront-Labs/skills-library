---
id: creative-arts.animation.vector-graphics.parametric-features-over-traced-master
name: parametric-features-over-traced-master
category: creative-arts
field: animation
product: vector-graphics
tags: [vtracer, resvg, svg, trace, vectorise, character-consistency, master-drawing, draw-once, parametric-face, layers, head-body-split, hair-overlay, python, pillow, anime, 2d-puppet, generated-art]
level: practitioner
status: verified
description: "Turn one approved character still into a consistent, animatable 2D asset: vtracer trace, split head/body/hair paths by bbox and colour, map a parametric face onto it, re-overlay the bangs."
sources: [https://github.com/visioncortex/vtracer]
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Parametric features over a traced master

The consistency trick that worked when prompt-based generation could not: **draw (or
generate) the character once, trace it to vectors, and never regenerate.** Everything
that must change per frame (eyes, brows, nose, mouth) is drawn parametrically from
the same shapes; everything that must stay identical (hair, skin, clothes) comes from
the one trace. Verified on three traced humans (teenager, heavyset older man, bob-haired woman)
and 40+ frames of lip-sync each: zero identity drift, because there is only one source.

## 1. Trace the master
```python
import vtracer
vtracer.convert_image_to_svg_py("master.png", "master.svg", colormode="color",
    hierarchical="stacked", mode="spline", filter_speckle=6, color_precision=6,
    layer_difference=24, corner_threshold=60, length_threshold=4.0,
    splice_threshold=45, path_precision=3)
```
An 832×1216 anime still becomes ~470 KB of paths and renders clean at any size.
`hierarchical="stacked"` matters: regions are painted back-to-front, so the FIRST
`<path>` is the background — drop it to put the figure on alpha.

Render with `resvg_py` (pure wheel, no Cairo DLL hunting on Windows):
```python
png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=1664))
```

## 2. Split the trace into layers by geometry and colour
Parse every `<path>`, take its `d` numbers as x/y pairs, record `min_y`, `max_y` and
`fill`. Then:
- **head paths** = `max_y < NECK_Y` (the neck line in trace space, e.g. 272 of 1216);
- **body paths** = the rest;
- **hair paths** = head paths whose fill is not skin (`r>225 and g>195`) and not
  white (`all > 240`).
Keep the original path order inside each group (it is the stacking order).

## 3. Map the parametric face
Draw the features in their own box (e.g. 1000 px head, eye line y=470, face centre
x=500) with `creative-arts.animation.character-design.anime-face-construction`.
Measure two landmarks on the master: face centre x and eye-line y (e.g. 428, 203),
and the brow-to-chin distance to get the scale (e.g. 62/317 ≈ 0.215). Wrap the
features in `<g transform="translate(cx,eye_y) scale(k) translate(-500,-470)">`.
Draw features only: no skin fill, no hair; the master already has both. Line widths
in the feature box must be ≥ 8 px so they survive `k` (a 4 px nose stroke vanished at
0.2).

## 3b. Drop the master's own eyes
The trace still carries the master's eye and brow strokes under your features; on a
character drawn with closed or lidded eyes they show as a second, shut eye beside the
open one. Remove any head path darker than the skin by ≥ 60 (sum of RGB) whose bbox
centre sits in the eye band (eye line ± 30 px, within ± 115 px of the face centre) and
is < 40 px tall. Hair paths are exempt (bangs cross the band on purpose).

## 3c. Classify hair by a sampled colour, not "not skin"
"Anything not skin and not white" worked for a pale character with dark hair and
failed for a dark-skinned character with grey hair (the face became "hair" and was
overlaid on top of the features). Sample the hair colour from the master (region
median at the crown) and the skin from the cheek; hair = within 95 of the hair
sample, or any dark line that starts above the eye line.

## 4. Stack
`head paths` → `features` → `hair paths again` (a second copy on top). The re-drawn
bangs cover the eye the forelock is supposed to hide and restore every strand that
crosses the brow. Body is rendered separately so the head can bob without the torso.

## 5. Views
A 3/4 read for dialogue: use the 3/4 feature set (far eye at 0.72 width, nose and
mouth shifted toward the far side) and translate the head and hair groups by ~3 px
in trace space for parallax. This holds to roughly ±20°; wider turns need a second
master traced the same way.

## Gotchas
- Sample the master's palette by **region medians**, not single pixels (a single pixel
  landed on a highlight and gave white hair). Use the sampled hair colour for any
  hair you add so the two sources match.
- `rembg` (isnet-anime) left the full bbox on a white-background still; dropping the
  trace's background path is cleaner than matting.
- Do not clear the master's head and draw your own hair unless the hairstyle is
  neat; see `creative-arts.animation.character-design.anime-hair-as-one-mass`.

## Verify
Render the figure beside the master at the same size: hair, clothes and silhouette
must be pixel-identical except at the features. Render 12 feature variants: same
person in every tile. Then render 40 lip-sync frames and flip through them: nothing
but mouth, eyes and head position may change.

## When not to use this
A colour-traced painted master never reaches TV-anime line quality (no outline layer,
blobby edges, features in a second style). If the target is a cel look, generate a
line+flat master and keep its pixels, swapping only blink and mouth cels:
`creative-arts.animation.pipeline.cel-character-from-generated-master`.
