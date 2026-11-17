---
id: creative-arts.animation.character-design.anime-face-construction
name: anime-face-construction
category: creative-arts
field: animation
product: character-design
tags: [anime, face, eyes, construction, proportions, cel-shading, line-weight, modern-anime, daima, dragon-ball, character-design, drawing, vector, svg, parametric, mouth-shapes, brows, rim-light]
level: practitioner
status: verified
description: "Construct a modern-anime face (front and 3/4) that holds up beside a Dragon Ball Daima frame: proportions, eye build, lid weights, mouth set, cel shadow and rim light."
sources: []
licence: Apache-2.0
version: 8
updated: 2026-11-17
aliases: []
---

# Anime face construction (front and 3/4)

How to build a face that reads as 2026 TV anime, verified by iterating a drawn head
beside Dragon Ball Daima dialogue frames until the gap was polish, not construction.
Numbers below are for a 1000 px head box (chin at y≈707, eye line at y=470); scale
everything together.

## Proportions
- **Skull wide, jaw soft, chin small.** Face outline ≈ 425 px wide at the cheekbones
  (x 288–712), 507 px tall (y 200–707). The jaw curves in from the cheek at y≈590 to a
  small rounded chin. A narrow pointed chin is the first "not anime" tell.
- **Eye line at mid-face** (y=470), eyes wide apart: centres at x=405 and 595
  (190 px apart, each ~125 px wide). Brows ~80 px above the eye line.
- **Nose = one short stroke** below the eyes (y 522–580), plus a tiny shadow blob; no
  nostrils, no bridge.
- **Mouth centre at y≈632**, between nose and chin. Open mouths are much larger than
  you expect: a "wide" shout is 150 px across and 110 px tall.
- **Neck** short and wide (136 px across), under the chin, drawn BEFORE the face so
  the chin covers it.

## The eye (the whole appeal lives here)
Build in this order, bottom to top:
1. **White**: a tall almond, top 74 px above the eye line, bottom 54 px below.
2. **Iris**: vertical oval, rx 43 ry 52, offset 6 px toward the nose. Large, so it
   touches both lids.
3. **Lid-shadow band**: a darker oval across the top of the iris (ry 24, opacity 0.85).
   Without it the eye looks like a sticker.
4. **Pupil**: dark vertical oval rx 17 ry 24.
5. **Two highlights**: a big one upper-outer (rx 13 ry 11) and a small one lower-inner
   (rx 6 ry 5). Both pure white; this is what makes the eye "wet".
6. **Upper lid**: the heaviest line on the face (12 px), curving over the top and
   thickening into a short outward flick at the outer corner (10 px).
7. **Lower lid**: thin (3.5 px), not closed at the corners.
States: `open`, `half` (scale the top half by 0.55 for a lidded look), `closed`
(one 9 px curve bowed downward). Blinks are 2 frames of `closed`.

## Applying the eye recipe to a generated cel master (verified 26 Oct 2026)

A side-by-side of a Daima close-up against three cast faces showed the cast's eyes as flat white ovals with a
small black dot, one highlight and one heavy black line. The recipe above fixed that when drawn into the
measured eye box (the box found from the master's own white and near-black pixels), with these adjustments:

- **Clip the iris, shadow band and highlights to the eye shape** (an SVG `clipPath` of the white). The lids then
  cut the iris, and nothing bleeds onto the skin. Make the iris `ry` up to 0.62 of the eye height so it
  touches both lids, and sit it 6 % of the eye height below centre.
- **Lift near-black irises.** A character whose iris is (22, 20, 20) reads as having only a pupil. Give each
  cast member an iris colour (a blue-grey, a warm brown) and derive three tones from it: base, a 0.55× top
  band, and a 1.35× lower crescent.
- **Lid-shadow on the white too:** a hard-edged pale blue-grey band across the top 22 % of the eye white.
- **Line:** the eye uses a dark brown (about #2b1a14), thinner than the face contour. The upper lid is tapered:
  1.5× line width overall, a 2.4× thick segment over the outer half, then a short wing past the outer corner.
  The lower lid is a short, thin, open curve that covers only the middle 45 % of the lower edge.
- **Lashes only where the character design calls for them:** three short ticks fanning from the outer upper
  corner (tick length 20 % of eye height), none for a male adult.
- **Keep the states:** `closed` must stay a single lid curve for blinks, and `half` keeps its skin-coloured lid
  patch. Check all four states beside the old render before accepting the change. Closed and half render
  from the same code path as before, so differences there mean a regression.
- **Size:** Daima eyes are larger relative to the face than a generated master's. Scale the measured eye box about
  its own centre (nudged up by 4 % of its height) before building both the skin patch and the drawing. The
  patch then covers the old eye and the drawing is not clipped. Per character: 1.2x for a teen lead, 1.25x for a
  young woman, 1.1x for an angry old man. 1.35x made a lead's eyes merge across the nose bridge and press into
  the bangs. Check the wide state (it grows another 30 % upward) and the closed state (the patch fill can show as
  soft blobs on dark skin) at the chosen scale.

## Brows baked into a generated master, and small-head level of detail (verified 26 Oct 2026)

**Baked-in brows.** A generated master can draw one expression into the brows, for example thick white slanted bands
that make a placid old man look permanently angry, however the eyes and mouth change. An independent review flagged
exactly that: furrowed brows on friendly lines. Fix it by erasing and redrawing:
1. Find the brow shapes: label connected near-white components (min channel > 190) inside a box around each brow, and
   keep the large ones (> 1,500 px) whose centroid is above the eye line. Eye whites sit lower and are skipped. The
   two sides come out as equal-area components when the master was mirrored.
2. Dilate each component by 10 px to take its outline, add it to the skin patch mask, and let the existing local-tone
   patch fill it. Hair stays protected by the hair mask.
3. Draw the new brow as two strokes of the same path: the ink outline at 1.9x the width, then the hair colour on top.
   Widths around 19 px at 1024 look bushy for an old man.
4. Open a drawing area for it: an ellipse above each eye, 40 px wider than the eye box and 38 px either side of the
   brow line, added to the patch mask. Without it, the brow is clipped to the old patch.
5. Pull the nose-side end back 16 % of the eye width and the outer end in 2 %. Left at the default extension, the two
   brows meet over the nose as a unibrow.
6. The brow state then drives the face: `up` worried, `flat` calm, `down` stern. The master's own brows can no longer
   override the expression.

**Small-head level of detail.** In wide and medium shots a head is a quarter to a sixth of its close-up size. At that
size a heavy winged lid, a lower-lid line and a dark iris top band merge with the brow stroke and read as spectacle
rims or a dark ring around each eye, which a reviewer described as the lead "wearing glasses". For heads in WIDE and
MED shots draw the eye as white, iris, pupil and highlights with a single lid stroke at 1.25x width, drop the wing, the
lower lid and the iris top band, and raise the brow line 1.7x so it separates from the lid. Cache face renders per level
of detail, or the close-up version will be reused.

**Mouth by emotion.** Cap the mouth one step down (`wide` to `open`, `open` to `small`) on low-energy lines such as
dread, wary, placid and hollow. Lip-sync data alone drives the widest shapes, and a teeth-and-tongue grin on a dread
line breaks the performance.

## Brows
Thick (13–14 px), expressive, drawn after the eyes. Three states carry most dialogue:
`worried` (inner ends raised), `neutral` (gentle arc), `angry` (inner ends pulled down
and in, strong tilt ~30°). A brow variant that is only 5 px different is invisible on
screen; make the states obviously different.

## Ears, and brows hidden by bangs (verified 28 Oct 2026)
Read from four full-resolution frames of the Daima opening (Goku 3/4 and shouting, the super form, a three-up of the
pointed-ear gods; pull frames from the source video at the second you want, a 640 px contact frame is too small for ears):
- **Ear = thin rim, one inner "C" fold, and a hard-edged shadow in the bowl below the fold.** Daima fills the lower bowl
  with the cool cel-shadow tone, never a gradient and never a highlight. The shadow follows the light (upper left), so it
  sits on the lower inner part of the ear on both sides.
- **Do it as a skin-only multiply.** One SVG path per ear in the final head coordinates, multiplied by the same shadow tone
  as the body flats (about 0.74, 0.71, 0.78) at 0.95 weight, only where the pixel is skin-coloured, so the ear's ink fold
  stays untouched. A grey-blue multiplier (0.58, 0.66, 0.82) read as a bruise; the shared shadow tone reads as a cel shadow.
  Find the path by drawing a coordinate grid on a 3x crop of each ear: the two ears are not mirror images in position
  (here 250-345 and 737-850 of 1024).
- **A character whose bangs cover the brows has no visible brow, by design.** Brow states drawn under the bangs overlay never
  show, so carry that character's emotion with the lid, eye size and mouth, and keep the brow work for characters whose
  brows are visible (the old man's white brows). Do not lift the bangs to reveal them.
- Ears hidden by hair (a bob cut) need nothing; dark skin makes the ear shadow too faint to matter at shot size.

## Mouth set (drives lip-sync)
Four shapes are enough for TV: `closed` (a single 5 px curve), `small` (round, 60 px),
`open` (teeth band on top, tongue below, 120 px), `wide` (150 px, teeth and tongue).
Interior is dark red-brown, never black; teeth are an off-white band along the upper
lip; tongue a lighter red ellipse at the bottom. In a 3/4 view squeeze the far half of
the mouth by ~10 % and shift the centre toward the far side.

## Nose and mouth finishing to the Daima look (verified 26 Oct 2026)

Compared at the same scale, a Daima shouting close-up and the cast: the open mouth was a rounded D with a sliver
of tooth and a pink dot, and the nose was a lone hook line. These rules, applied in the face-patch step of the
cel pipeline (skin patched with the local tone first, then drawn over), closed most of the gap:

**Mouth** (all inside one SVG group):
1. Draw the opening as a path, fill it deep maroon (#4a1620), and **clip everything else to that path** with a
   `clipPath`, so teeth and tongue can never poke past the lips.
2. **Upper teeth** as one white band (#f6f2ea) from the top of the opening to about 0.34 r below the mouth line,
   with a slightly curved lower edge, a thin grey outline (#9a8f90) and a thin **centre divider**.
3. **Tongue** as two tones, a pink (#d27a86) mound at the bottom and a lighter (#eaa1ab) cap on it.
4. **Outline** is thin dark brown (#3a1a14, 0.07 r), not black. The closed mouth is one brown curve (0.08 r).
5. **Lower lip:** a short curve about 0.32 r below the opening, covering the middle 40 % of its width, plus a soft
   chin-shadow wedge under it in the local skin tone × 0.86.
6. Make the open shapes a little wider than the old ones: 1.15 r open, 1.3 r wide.

**Nose** (front or slight 3/4):
1. One shadow tone only, the local skin × 0.84: a small **side-plane wedge** on the side away from the light and
   an **under-nose crescent** about 0.9 nose-radii wide.
2. A thin brown line (0.10 nose-radii) for the bridge hook. No nostrils.
3. Two tiny **cheek-tick wedges** beside the nose at the level of the eyes' lower corners, in the same tone.

On pale skin the 0.84 tone reads as beige; check it against the face before pushing it darker. Check all
four mouth states in a speaking shot, not just on the sheet: the sheet showed the mouth, but only the shot
showed that the lip-sync states still switched.


## Light and line
- **One cel shadow side** (skin darkened, opacity 0.85) along the side away from the
  key light, from temple to jaw, plus a shadow band under the bangs and a small
  nose-side blob. **One rim light** stroke (pale warm, 7 px, opacity 0.55) along the
  lit edge. These two strokes are most of the difference between "flash cartoon" and
  anime.
- Line colour is warm near-black (`#2e1d18`), never pure black. Silhouette lines
  6 px, interior lines 3–5 px, upper lids 12 px. Uniform line weight everywhere is the
  second "not anime" tell.

## 3/4 view
Keep the near eye at full size; draw the far eye at 0.72 × width (all x offsets
scaled). Move the nose and mouth centre ~50 px toward the far side; nose becomes a
small profile bump. Only the near ear shows. Everything else is the same shapes, so
the character stays on model.

## Verify
Put the drawing at 640 px beside a benchmark frame (Daima, Jujutsu Kaisen, Rick and
Morty close-up). Check: eye height ≥ 1/4 of face height; upper lid visibly heavier
than every other line; a shadow side and a rim light both present; a wide mouth at
least 1/3 of face width. Then render the 12-variant sheet (4 mouths × 3 eyes): every
tile must read as the same person at a glance.
