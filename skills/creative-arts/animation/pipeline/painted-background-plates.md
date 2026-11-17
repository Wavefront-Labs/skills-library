---
id: creative-arts.animation.pipeline.painted-background-plates
name: painted-background-plates
category: creative-arts
field: animation
product: pipeline
tags: [background-painting, painted-backgrounds, plates, bg-plates, rick-and-morty, tv-cartoon, 2d-backgrounds, holdout, compositing, object-id, matte, procedural-painting, blender, freestyle, pil, set-dressing, continuity]
level: advanced
status: verified
description: "Painted BG plates for a 3D cartoon pipeline, R&M style: render set alone + id matte per locked camera, paint drawn detail per surface, render characters over it as a holdout pass."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Painted background plates (the TV-cartoon split, from a 3D pipeline)

Adult TV cartoons (Rick and Morty and its kind) look dense and crisp because the
backgrounds are **paintings**: a background artist draws every shelf, poster, crack and
pipe once per camera setup, and the characters are animated on top. A 3D cel pipeline
that renders sets and characters together gets bare walls and blocky kit shapes
instead. This skill rebuilds the split from a 3D pipeline: the set becomes a painted
plate per locked camera, the characters render alone over it. It is the craft companion
of `production-design.background-painting-in-show-style` (style sheets, paint order) and
`production-design.background-painting` (paint vs model, projection).

## 1. Preconditions

- **Locked cameras.** A plate is one still per setup. TV cartoons hold a handful of
  locked setups per scene, so this costs nothing in grammar; strip camera keyframes for
  plate shots. Push-ins become a 2D scale of the plate.
- **A flat render look already in place** (two-tone fills, one line weight), so the
  plate and the characters share a register.

## 2. Two render modes per shot

1. **Plate mode.** Hide everything that is not the set, render one frame from the locked
   camera -> `<shot>_base.png`. Then, in the same scene, give every set mesh a flat
   emission colour, turn off lines, shadows, raytracing and anti-aliasing, and render the
   **object-id matte** -> `<shot>_ids.png` plus a JSON of object name -> colour. The matte
   is what lets the painter know wall from ground from dumpster.
2. **Foreground mode.** Render the shot normally but with every set mesh as a
   **holdout** (`object.is_holdout = True`): it renders transparent yet still hides any
   character standing behind it. Film transparent, RGBA output, and exclude the set from
   the line pass (Freestyle line set `select_by_collection`, `EXCLUSIVE`, on a collection
   holding the set) - the plate carries its own drawn lines.
3. **Composite.** Overlay the RGBA frames on the still plate (ffmpeg `-loop 1` plate,
   `overlay=shortest=1`).

## 3. Painting the plate (the detail vocabulary)

Classify each matte object by name (wall/building, ground/floor/road, roof, props like
dumpster/barrier/crate) and paint inside its mask only:

- **Walls.** A location palette fill (brick red, tan, cream - pick per wall,
  deterministic), then **brick clusters, never a full grid** (2-4 groups of 3-6 bricks,
  brick height ~1/22 of the wall's on-screen height, darker fill + line); **one or two
  thin dark water streaks** (wide pale drips read as icicles); a grime band along the
  base; on big walls a **poster or flyer** (frame, picture block, three text strokes, a
  torn corner); a **drainpipe** down one edge with brackets; a vent / AC box with louvre
  lines; a **graffiti tag** (a dark stroke under a coloured stroke); an electrical box
  with conduit running down.
- **Ground.** Jagged crack polylines, a puddle (pale blue ellipse + a white highlight
  stroke), crumpled-paper litter, a shadow band where it meets the wall.
- **Props.** Grime at the base, scuffs and a dent arc, a sticker.
- **Finish.** Redraw **one even line on every boundary between real surfaces** from the
  matte (the solid wall fills cover the base render's lines), in the show's warm
  near-black (around RGB 44,32,27), 3 px at 1080p.

**Zone the features** on each wall (poster left-centre, vent top-right, graffiti low) so
they never stack. **Seed every feature by object name** and place it at fractions of that
object's visible bounding box: the same wall then carries the same poster in every shot
of the setup, which is background continuity for free.

## 4. Traps (each hit in production)

- **Linear vs sRGB.** Emission colours written to the JSON are linear; the PNG is sRGB.
  Convert the expected colours with the sRGB transfer function before matching, or no
  pixel matches and nothing gets painted.
- **Noisy matte.** At one sample, screen-space raytracing and shadows put speckle into
  flat colours. Turn them off for the id render, then mode-filter the label map (7 px).
- **Z-fighting kit pieces.** Two coplanar walls placed in the same spot interleave in the
  matte as fine stripes; painting both draws a dithered band. Real neighbours share a
  short edge; z-fighters share a huge one. Merge any pair whose shared-edge count exceeds
  ~15 % of the smaller area.
- **Thin geometry.** Cables and wires turn to noise at plate resolution; leave them out
  of the plate (the foreground pass can still draw them).
- **Holdout alpha.** A compositor graph on the foreground render must feed the render
  layer's Alpha to the Composite node or the RGBA frames come out opaque.

## 4b. Vocabulary per kind of set (verified on a kitchen, a street, a suburb, a park)

The painter needs one drawer per surface class, chosen from the object name and the
shot's location; anything unclassified keeps its own render (furniture already carries
kit detail and an outline).
- **Interior walls:** wallpaper stripes at ~1/18 of wall width with a small repeat
  motif, a darker **wainscot** band (~27 % of height, vertical panel lines), a pale
  baseboard.
- **Wood floor:** planks converging to a vanishing point, staggered board ends, a few
  knots.
- **Houses (single-mesh kit buildings):** one pastel per house from a small palette,
  clapboard lines every height/26, a darker roof band, framed windows in two rows with
  two-tone curtains and sills, a door with a knob and a house number, a grey foundation.
- **Road / sidewalk / lawn:** lane dashes (thicker toward the camera), tar patches,
  cracks; joint lines every ~130 px; grass tufts (V of three strokes, size by depth)
  and a few flowers.
- **Foliage and rocks:** scalloped leaf arcs in two greens; trunks with bark grooves;
  rocks grey-brown with angular cracks and moss patches. **Leave thin grass clumps
  unclassified** - outlined, they become black squiggles.

## 4c. Two more traps from the other sets

- **Merge only same-class surfaces.** The z-fight merge (§4) swallowed a house standing
  next to a long thin sidewalk strip - a long shared edge relative to the strip's area -
  and left a building blank. Require equal class before merging.
- **A dark base colour is not an outline.** "Keep the base render's lines on top"
  implemented as "sum of RGB below a threshold" excluded an entire dark road from
  painting. Outlines are *thin* dark strokes: a dark region survives a 7 px erosion, a
  stroke does not, so outline = dark and not (eroded then dilated).

## 5. Verify

- [ ] Plate and matte line up pixel for pixel; every wall, ground and prop gets painted.
- [ ] No speckle or striped bands anywhere in the plate.
- [ ] The same wall carries the same poster, vent and brick clusters in every shot of a
      setup.
- [ ] Characters behind set pieces are still hidden by them in the composite.
- [ ] Side by side with the reference show, the background reads as a drawn location
      (density, posters, grime, cracks), not as kit blocks.

Related: `production-design.background-painting-in-show-style`,
`production-design.background-painting`, `production-design.set-dressing`,
`methods.stylized-series-tier` (flat 2D branch), `blender.freestyle`.
