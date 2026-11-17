---
id: creative-arts.animation.pipeline.cel-character-from-generated-master
name: cel-character-from-generated-master
category: creative-arts
field: animation
product: pipeline
tags: [cel, replacement-cels, gesture, pose-variant, img2img, limited-animation, blink, mouth-cel, expression-cel, eye-states, brow-states, emotion, hair-overlay, cut-out, paper-cut, head-paste, body-master, recolour, palette, consistency, dragon-ball, 2d, python, pillow, numpy, resvg]
level: practitioner
status: verified
description: "One generated line+flat master becomes a consistent 2D cast member: keep its pixels, swap eye, brow and mouth cels per emotion, re-overlay hair, cut the paper, paste the head on a body."
sources: []
licence: Apache-2.0
version: 12
updated: 2026-11-17
aliases: []
---

# Cel character from a generated master (replacement cels only)

Verified 22 Oct 2026: three humans built this way rendered a 73-shot episode in close,
medium and wide shots and read as 1990s Dragon Ball beside a Daima frame. Master
generation: `comfyui.dbz-line-and-flat-character-master`.

## Principle
Consistency comes from **not redrawing the design**. The master's nose, ear, hair and
costume are kept pixel for pixel; the eyes, brows and mouth are replacement cels drawn
in the master's ink colour and line weight, as TV anime does with eye and mouth sheets.
v3 swapped only lids and mouth; a cut built that way had every character wearing the
master's one expression in every shot ("not production polished"). v4 redraws BOTH
eyes and the brow per state so the shotlist's emotion is on the face.

## Per-character data (verified with a full-resolution diagnostic, never eyeballed)
Reading feature centres off a 64 px grid put mouths and eyes 20-40 px off and the owner
saw "lips and eyebrows not where they should be". Always render a **diagnostic sheet**:
the master with every cel box drawn on it (eye boxes red, mouth ellipse blue, brow boxes
green, 50 px grid) beside the rendered open/closed/wide states, cropped to the face at
100 %. Correct the numbers until each box sits on the feature, then keep the sheet with
the character.
- eyes: centre, half-width, patch half-height per eye (tall female eyes need a taller
  patch or the iris shows under the lid line);
- mouth: centre and half-width (centre sits a little below the master's own mouth);
- a skin sample point on the cheek (take the **median of a 15×15 patch**, never one
  pixel: a single pixel on a cheek line turned the mouth patch black);
- a hair sample point on hair fill (a sample on skin made the whole face "hair");
- head height (hair top to chin) and chin y; paper colour if the corners are not paper.

## Face symmetry first (mirror the clean half)
A generated front bust is never symmetric: one eye hides under the bangs, the mouth sits
30-50 px off the face axis, one cheek is wider. Viewers read this as "not quite anime"
before they notice anything else. Fix it in the master, not in the cels:
1. Axis = midpoint of the two MEASURED eye boxes (never the image centre or the nominal
   coordinates).
2. Make a mirrored-halves sheet: left half beside its reflection (L|L') and the right
   half's reflection beside it (R'|R). Pick the half where both eye, ear and jaw read
   clean, usually the one the bangs do not cover.
3. Reflect that half over the other about the axis for head rows only (down to the jaw
   row + 2). The collar below stays; the neck is symmetric enough that the seam never
   shows. Do this before hair/skin masks are built so every later step sees one face.
4. Rewrite the eye, mouth, nose and sample coordinates onto the kept side ONCE (eye =
   kept eye reflected; mouth and nose x = axis); a sample point on the discarded side
   now reads the reflected pixels.
5. Mirroring doubles the nose into an "M" (two bridge strokes meeting at the axis).
   Patch the nose with the LOCAL skin tone (two ellipses: a narrow tall one between the
   eyes, a wider low one over the nostrils) and draw one Toriyama tick: bridge curve on
   one side ending in a short nostril hook, stroke ≈ 14 % of the nose radius. Woman-type
   small "w" noses survive mirroring and need no patch.
Gate: mouth x offset from the eye axis = 0, both eye boxes equal width and height.

## Clean the master before any cel goes on (one flat per material)
A generated "line + flat" master is never flat. Four cleanups, in this order, all from
masks, no hand painting:
1. **Alpha pinholes**: fill holes in the paper cut (`binary_fill_holes`), or the plate
   shows through the hair as coloured dots.
2. **Paper fringe**: in the 4 px band inside the alpha boundary, drop every pixel
   brighter than ink (sum > 330). The generator leaves a pale rim outside the outline
   that reads as a grey halo on dark plates. The outline ink becomes the silhouette.
3. **Stray strokes**: small isolated ink blobs in the cheek zone (between the eye tops
   and jaw-20, 40..230 px from the face axis, bbox under ~40k px at 1024) are generated
   cheek lines and eye bags; paint them and a 10 px ring around them skin. Flag it per
   character: an old face keeps its wrinkles.
4. **Flat skin**: every skin-hued pixel (within 150 of the sample, same channel order,
   not ink or hair, 1 px clear of ink) becomes the sampled tone. Soft gradients under
   the eyes and across the cheeks are what viewers call "weird shading"; the shade pass
   puts the ONE hard shadow back. Cool highlight strands inside the hair mass (blue >
   red + 6) become the hair tone the same way.

## Cels
1. **Blink**: measure the eye, do not guess it: inside a window from the nominal top
   (so white brows above are excluded) take the bounding box of near-white (sclera)
   plus near-black pixels touching it (iris). Patch = that box padded ~10 px, as an
   ellipse, **clipped to non-hair pixels** except inside the box itself (a brown iris
   matches brown hair), filled with the **local skin tone** (median of a 13 px ring
   around the patch, ink and white excluded; a cheek sample is the wrong tone on a
   shaded face) and feathered 2 px. Lid = one stroke at 30 % up from the box bottom,
   width ≈ 16 % of the box half-width, alpha clipped to the patch. Blink patches go on
   BEFORE brow cels. Multiply alpha in int32: uint8 overflow erased every lid.
1a. **Expression cel (eyes + brow per state)**: one skin patch per eye covering the
   measured eye box plus the brow (box padded 12 px sideways, 12 px below, `brow gap +
   6` above), clipped to non-hair as for the blink, feathered 4 px. Patch tone is a
   **vertical gradient**: median of near-skin ring pixels above the patch centre
   (forehead, darker under the bangs) to median below it (cheek). A single tone left a
   light band at the hairline; the clean cheek sample alone was worse. Then draw:
   - eye: almond outline (inner corner lower than the outer), white, iris oval in the
     character's iris colour and size fraction (a dot pupil for a Trunks-type eye,
     ~0.55 of the width for a large female eye), pupil, one highlight, thick upper lid
     stroke (9 % of the box width) on top;
   - states: `open` = the box; `wide` = box grown 30 % up and 12 % down (alarm, shock);
     `half` = skin-toned lid shape over the top half with its own ink edge (hollow,
     suspicious, tired); `closed` = the blink lid line;
   - brow: one ink stroke above the eye at `gap`, inner end raised 22 % of the eye
     width for `up` (worry, dread), lowered for `down` (anger, resolve), `flat` for
     calm. Characters whose brows are hair-coloured keep their brow cel (1b) instead.
   Map the shotlist's per-character emotion to (eye state, brow state) once, in the
   renderer (shock/panic/alert = wide+up; hollow = half+flat; wary/resolve = open+down;
   placid = open+flat); blinks override the eye state for two drawings.
1b. **Brows** (when the master's brows carry the wrong mood, e.g. a stern old man):
   a feathered local-tone patch over the master brows and the character's own brow
   shape in the hair colour with an ink outline.
2. **Mouth**: skin ellipse over the master mouth (1.5× half-width wide, −0.6/+1.6×
   tall), then: closed = one stroke; small/open/wide = dark-red interior with a 9 %
   ink outline and a teeth band on open/wide. Render the SVG at master size (resvg)
   and composite; raster ellipses first, strokes second.
3. **Hair back on top** after a blink so bangs cover the lids again. Hair mask =
   pixels within 60 of the hair sample median, dilated 5 px, **kept only if connected
   to the sample point** (flood on the mask), plus ink pixels within 9 px of it.
   Without the connectivity rule the mask grabbed sclera, shirt and iris.

## Auto cel shading (the single biggest "flat, not anime" tell)
A line+flat master has no shadow tone; DBZ has one hard shadow everywhere. Derive it
from the masks you already have, light fixed upper-left, shadow = flat x (0.74, 0.71,
0.78) (darker, slightly cooler, same hue; a blue-shifted multiplier read purple):
- **Underside bands**: close each material into a mass (ink lines closed with
  MaxFilter/MinFilter 5 px at 1024), then `mass & ~shift(mass, toward the light)`;
  44 px for hair, 30 px for cloth. Per-stroke bands (14 px on the raw flats) follow
  every pen stroke and read as noise; wide bands on closed masses read as spikes'
  undersides and fold shadows.
- **Casts**: hair mask moved down 36 px / right 6 px onto skin = bangs shadow, but
  only above the eye tops (side locks moved down land on the cheeks as blocks);
  the pasted head's jaw silhouette moved down 22 px onto the body = neck/collar
  shadow (apply on the final composite so bust neck and body neck shade alike).
- **Never on**: ink (sum < 220), eye whites (sum > 750 above the chin only: white
  cloth below the chin must shade), skin clumps (faces take casts only; a band on
  the skin flat drew a stripe along the jaw and blotches by the eyes).
- Clean the mask with GaussianBlur(3 px) > 50 %: slivers thinner than ~6 px vanish.
- **Crisp 2-tone cloth**: the generated master's soft fold shading survives flat
  recolour (outside its tolerance). Snap pixels at 1-2.2x the recolour tolerance
  that share the sample's channel order (blue cloth never catches warm skin) to
  target x shadow: one flat, one shadow, nothing soft.
- Resize RGBA with **premultiplied alpha**: plain LANCZOS on straight alpha bleeds the
  transparent pixels' colour into the edge (a light halo around every figure).
- Body masters get the same 1.5x img2img pass as heads (832x1216 -> 1248x1824, denoise
  0.3): lines at medium shot stop looking soft. Coordinates stay in 832 space times the
  scale; the silhouette comes from the clean original master (hi-res paper is textured).

## Paper cut-out
- Paper colour = brightest 12×12 corner median unless given explicitly (hair or
  costume fill some corners).
- Flood from edge midpoints and corners **only where the seed is paper** (tolerance
  22; 40–48 ate a white blouse on grey paper and a hoodie that touched the corners).
- Paper-coloured pockets walled off by hair (white hair on paper) are removed too,
  but only above `chin − 20` and never inside the eye ellipses (whites of the eyes).

## One head for every shot size (preferred)
A separately generated bust and body never match exactly (hair, colours). Instead
crop the **body master's head** (tight box, ~1.15× head height), scale it to 1024 and
run img2img at denoise 0.3 with the same style tags: lines come back crisp at 2.5×
and the drawing is the same head the medium and wide shots show. Cut its alpha from
the body master's silhouette (crop + resize of the body cut-out, 3 px erosion), never
by colour: the hi-res pass textures the paper. Record the crop box with the master.

## Full figure = body master + bust head (when a bust master is kept)
- Body master generated separately ("cowboy shot"); recolour its flats to the bust
  palette with (body sample -> bust sample) pairs (mask = within 50 of the body
  sample median, fill with the bust median).
- **Cut the body's head by material, not by a row.** A straight row cut always shows:
  it slices the hood/collar that rises behind the head, or the body's own jaw. Above
  the neck row remove the body's skin (within 130 of its skin sample, same channel
  order), its hair (within 110 of the hair median, only above neck - 25: a white
  collar at jaw level is not white hair) and thin ink not touching cloth; keep only
  cloth components that continue below the neck row (hood, collar) plus their ink.
  Thin ink vs dark cloth: a black turtleneck survives MinFilter(9), a line does not.
- The body's chin/mouth lines just under the cut are painted neck skin; its jaw/ears
  peeking out beside the pasted head (skin not under the head or the 40 px neck
  column below it, above jaw + 40 px) are erased.
- **`chin` = the jaw outline's bottom ink row, measured** (first ink run below the
  mouth at the face centre and +-60 px), not an eyeballed number: three of three
  busts were 30-45 px off, so the keep cut sliced the chin above its outline and
  drew a straight edge. Keep bust rows above `chin + 2`; in the last 130 rows keep
  only skin, ink within 4 px of skin (the jaw line), hair and the mouth ellipse,
  never the bust's collar strokes. Paste with the bust jaw 2 px below the body's
  neck row, which must sit in pure neck skin (below the body's jaw, above its
  collar; measure the skin-only rows).
- Scale the bust so its head height equals the body's head height (re-measure
  `head_px` = hair top..jaw whenever `chin` moves).
- Eyes: measure each eye box, then give both the mean top and bottom: a 5 px
  height difference between the measured boxes read as misaligned eyes.
- Use the **bust for close-ups, the full figure for medium and wide**: a medium shot
  with the bust leaves a floating head when the generation was head-only, and the
  full figure's head lands near native resolution at medium.

## Gesture variants (arms are not at the sides forever)
The body master is arms-at-sides; dialogue needs arms crossed, a hand on a wall, a wave.
img2img the body master (same style tags + the pose words, denoise **0.85**, master size)
gives a new pose in the same costume; the head drifts, and that is free because the
pasted bust head replaces it. Verified: arms crossed / hugging self, one hand raised
open-palm (used as "hand on the invisible wall"). Rules learned:
- denoise 0.62 keeps the master's pose; 0.75 keeps the costume but not the pose; 0.85
  changes the pose; above that the costume mutates (pockets, logos, two-tone sleeves);
- a variant whose costume comes back near the paper colour is cut to shreds by the
  flood; prompt a different paper or re-seed;
- recolour the variant's fills to the palette from samples in the VARIANT (tolerance up
  to 120 on a two-tone hoodie, never below the shoe line), then keep only the largest
  connected component of the alpha (paper streaks go) and remove paper pockets only on
  the leg rows (pale highlights above the waist are not pockets);
- a raised hand lives above the neck line where the body's head is cut off: declare the
  columns to keep there, and turn light fill in that zone to skin;
- anything that overlaps the head (hand over mouth, fists at the cheeks) is lost under
  the pasted head: do not generate those as body variants;
- props in hand (grocery bags) did not survive at any denoise; draw them as a layer.
- **the variant's own hair survives behind the pasted head** unless you cut it: the hoodie recolour (tolerance 120) turned the
  variant's dark hair into hood-blue, the connected-cloth test then kept it as cloth, and a third, blue-grey Dill hairstyle
  showed around the real head in a medium shot (found in review, fixed 28 Oct). For any variant, mark everything above
  `neck - 45` (832-space rows, about the hood height) as head and drop it, before the raised-hand keep columns apply.
  Check every pose shot at 100 % around the head; the bust variant never shows it, only the full-figure one does.
Drive it from the shotlist with a per-character `pose` on the few shots that need one.

## Pseudo 3/4 turn and rim light (cheap polish that reads)
- **Turn**: squeeze the far half of the head (left of the eye axis) to 0.72 width, keep
  the near half, re-centre so the silhouette stays over the neck; flip the result for
  the other facing. In a two-shot the speaker looks screen-left, the listener
  screen-right; singles stay front. Do the turn AFTER the full-figure head mask (the mask
  uses front-view coordinates) and before the resize. It is a limited-animation cheat,
  not a drawn 3/4: use it at medium size and smaller.
- **Rim light**: a band ~8 px inside the outline ink on edges facing the key (mask minus
  itself shifted toward the light), 45 % warm white over the flat, never over the
  shadow or ink. Put the band inside the ink: on the outline itself it disappears.
- **Hair vs skin**: when the master's hair flat is within ~100 (sum of channel
  differences) of the skin flat, recolour hair-coloured pixels inside the hair mass to a
  `hair_tone` further from skin, or the hairline vanishes at wide sizes.

## Daima finishing passes on the face and the clothes (verified 26 Oct 2026)

Each pass is a rule read off a full-resolution Daima frame, applied to the flat master as a mask operation, and checked
side by side and in a real shot. Details are in `character-design.anime-face-construction` (eyes, size, nose, mouth, baked-in
brows, small-head level of detail), `character-design.anime-hair-as-one-mass` (hair) and this list for the body:

- **Switches per character in the config:** `eyestyle=dict(lash, scale)`, `hairstyle`, `mouthstyle`, plus `brow_cut`
  and `browfill` for a master with brows baked in. A module-level `LOD` flag, set from the shot size, selects the
  small-head eye. Anything that depends on it must be part of the cache key.
- **Body line tint:** interior strokes of the body become a dark tint of the fill they border (nearest flat colour x 0.42
  plus a small cool offset); the outer contour is left dark. Find strokes as dark pixels minus their 3x3 morphological
  opening, repeated 3 px at 1024, so only thin strokes qualify. Selecting "dark pixels" alone turned navy trousers and a
  black skirt into streaks of nearest-colour garbage, because large dark fills are not line. Restrict to pixels at least
  9 px inside the silhouette.
- **Small-head lid weight:** at the small-head level of detail the single upper-lid stroke was 1.25 x the eye stroke width
  and the face read as heavy-lidded (like glasses) in wides. 0.8 x keeps the eye open and legible at about 180 px heads;
  judge it beside the previous frame at the same crop, since the difference is small.
- **What did not transfer:** volume, overlap and fold placement. Those need a 3D form under the drawing (see
  `comfyui.on-model-drawing-from-3d-guides`).

## Failure modes
- Mirror step moved a sample point onto an ink line → hair mask of 54 px, no hair
  shading, and the flat-skin rule then ate the hair. After ANY mirror or sample change,
  print the hair-mask pixel count (hundreds of thousands at 1024, not tens) and keep
  samples on the axis or on the kept side.
- Mouth patch too small → the master's smile line survives beside the new mouth.
- Patch filled with the sampled skin median → a visible ellipse edge on dark/shaded skin;
  fill every patch (eye, mouth, nose) with the local median around it.
- Open mouths at < 1.2× the mouth radius read as polite murmurs; anime jaw drops are
  open ≈ 1.2 r, shout ≈ 1.8 r tall, kept above the jaw row (the full-figure cut).
- Eye patch too short → iris remnants below the lid line (tall eyes).
- Sample on ink/skin → black patch or a face-sized "hair" mask.
- Corners not paper → whole master opaque (white box in the shot). Set paper
  explicitly or regenerate on light-blue paper.
- Closed-mouth default drawn as a smile makes every hold grin; give each character a
  closed shape matching their mood.

## Verify
- 20-state sheet per character (4 mouths × {open flat, open up, wide up, half down,
  closed}): one person in all 20, no patch edges or light bands, bangs over the eyes
  in every row, the iris never shows under a half lid.
- Full-figure sheet: hoodie/hair colours identical to the bust at 100 % zoom.
- Mirrored-halves sheet after the mirror step: both halves identical, no "M" nose, no
  doubled hair spike at the axis.
- One close, one medium two-shot, one wide rendered over the plate: no white box,
  chins at the framing line, heads the sizes the shot spec asks for.

## Screen-faced characters
A mascot with a screen for a face (CRT robot) needs no eye/mouth cels: paint the screen
glass dark and draw the vector face into the screen box (scaled to its width). The body
master and its hi-res head come from the same tags with `cute simple mascot robot, solo,
1robot`; busy seeds show extra gadgets, pick the plain one.

## Render discipline
A full-episode render in foreground chunks: with 1024 px heads 19 shots overran a 10-minute
chunk and the chunk died silently, leaving the old frames in the cut. Keep chunks to ~9
shots and, before cutting clips, check every shot's newest frame is from this run.
