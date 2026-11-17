---
id: creative-arts.animation.character-design.anime-hair-as-one-mass
name: anime-hair-as-one-mass
category: creative-arts
field: animation
product: character-design
tags: [anime, hair, bangs, silhouette, hair-mass, scallop, tufts, messy-hair, character-design, drawing, vector, svg, procedural, generated-hair, failure-mode, daima]
level: practitioner
status: verified
description: "Draw anime hair as one solid mass with a scalloped edge and strand strokes; why generated clumps, headbands and radial spikes fail, and when to trace a master instead."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Anime hair as one mass

Verified across five drawn iterations of the same head beside Dragon Ball Daima
frames. Hair is where procedural drawing goes wrong first, and it goes wrong in the
same three ways every time.

## The construction that works
1. **Hair back**: a filled shape behind the head, drawn before the face so the face
   covers its inside. Its outline must NOT rise above the front mass at the crown, or
   you get a double outline.
2. **Hair front = ONE filled path**: the skull dome, the side hair down past the ears,
   and a **scalloped bottom edge** made of alternating tip and notch points
   (e.g. 13 points across the forehead: tips at the brow line, notches ~40 px higher,
   one long forelock tip over an eye). Round the tips (cubic with the control point
   pulled back toward the notch), keep the notches sharp.
3. **No vertical outlines between clumps.** Instead draw 3–6 short **strand strokes**
   rising from the notches (3 px, ~85 px long, opacity 0.85). Daima, Jujutsu Kaisen
   and most 2020s TV anime use exactly this: one mass, a few strands.
4. **Sheen**: a zigzag-edged lighter band across the upper front (opacity ~0.5), and a
   darker band on the underside of the mass just above the scallop (opacity ~0.45).
   The darker band must sit INSIDE the hair; if it crosses the eye line it reads as a
   headband.
5. **Two or three flyaways** at the crown, small (≤ 40 px); and one side flyaway over
   each ear for a messy character.

## The three failure modes (each one cost an iteration)
- **Headband**: any full-width line or band across the forehead — the inner edge of a
  dome drawn as a crescent, a highlight stroke, a shade band placed over the eyes.
  Fix: solid dome, soft fill-only sheen, shade band above the scallop notches.
- **Paper-cutout slabs**: clumps drawn as separate outlined shapes with straight sides
  read as Lego hair. Fix: one mass + scallop, strands instead of outlines.
- **Saw blade / Super Saiyan**: hair-back silhouettes generated from a regular spike
  function (alternating radius around an ellipse) read as a saw blade; hand-placed
  radial tufts read as a Saiyan crown. Real messy hair is irregular tufts that LIE
  ALONG the head and overlap, not spikes radiating from it. Either hand-draw each
  tuft following a reference silhouette, or (faster and better) **trace the hair from
  an approved master drawing** and reuse it — see
  `creative-arts.animation.vector-graphics.parametric-features-over-traced-master`.

## Finishing a generated hair mass to the Daima look (verified 26 Oct 2026)

Compared at the same scale, a Daima close-up (blue bob with bangs) and our generated heads differed in four
ways. Each was fixed as a pass over the hair mask of a flat line-and-colour master, in this order:

1. **Ink inside the hair becomes a dark tint of the hair colour**, not black: about 0.34 × the flat colour plus a
   small cool offset (+6, +8, +18). Daima's strand lines are dark blue on mid blue.
2. **Thin the thick strokes.** Black contours were about 12 px at 1024; Daima's hair lines are fine and near
   uniform. Erode the ink by 3 px to find thick-stroke cores, dilate the cores by 9 px to claim the whole
   stroke including antialiased edges, keep only the core dilated by 2 px, and return the rest to the flat
   colour. Thin strands vanish under the erosion, so they are kept untouched. Keeping a band of edge pixels
   instead leaves a halo that reads as a double line.
3. **One hard-edged highlight band** that follows the crown: hair-flat pixels whose vertical distance from the
   top contour is 5 to 10 % of the hair height, inset 6 px from the edge. Break it into about four dashes
   across the head with a slow sine mask, open it by 3 px, then round the corners with a Gaussian blur
   thresholded at 0.5. Colour it 1.10 × the flat colour plus 18. Column-gated dashes without the rounding
   looked like a row of rectangles.
4. **Clean the strays:** tint pale bluish pixels on the 3 px outline border, and recolour leftover cool-blue
   patches inside the hair to the hair's own shadow tone.

Run it after the bangs have been put back over the drawn eyes, as the last step of shading. Enable it per
character. White hair takes the same pass; its lines come out grey and its highlight band is nearly invisible.
Remaining differences from Daima: strand lines inside the mass are still the master's, not drawn long and
parallel from root to tip, and a few cool-blue patches at the temples survive.

## When to draw vs trace
- Neat hairstyles (bob, bowl, short back and sides): draw with the mass + scallop
  construction; it is fully parametric and holds across views.
- Messy / spiky / long hairstyles: trace the master; procedural attempts converge on
  one of the three failures above. Keep only the FEATURES parametric.

## Verify
Side by side at 640 px with a benchmark frame: no line crosses the forehead or the
eyes; clump boundaries are strands, not outlines; the silhouette has no repeating
period. Then look at the head at 160 px: it must still read as hair, not a helmet.
