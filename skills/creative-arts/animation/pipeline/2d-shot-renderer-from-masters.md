---
id: creative-arts.animation.pipeline.2d-shot-renderer-from-masters
name: 2d-shot-renderer-from-masters
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, 2d, shot-renderer, shotlist, data-driven, painted-background, master-plate, crop-by-size, two-shot, staging, cutout, puppet, lip-sync, on-twos, pillow, anime, consistency, draw-once, establishing-shot, slow-push]
level: practitioner
status: verified
description: "Render every shotlist shot in 2D from drawn masters: crop the location painting by size, stage the cast on slots, lip-sync the speaker, light, write frames on twos."
sources: []
licence: Apache-2.0
version: 8
updated: 2026-11-17
aliases: []
---

# 2D shot renderer from masters (shotlist → frames)

The 2D twin of `creative-arts.animation.pipeline.shot-renderer`: one data-driven tool
that reads the shotlist and renders any shot from ONE painted master per location and
ONE drawn asset per character. Verified on an 87-shot episode across five locations,
~0.3 s per drawing on CPU, no GPU in the loop.

## Inputs (all drawn once)
- Location master: a 1344×768 painting at the WIDE locked camera
  (`creative-arts.animation.comfyui.background-master-from-blockout`).
- Cast assets: `creative-arts.animation.vector-graphics.parametric-features-over-traced-master`
  or a pure vector character. Each declares `head_px` (head height in the 2× raster)
  and `chin` (chin y in the same units) so the renderer frames by head size.
- Shotlist rows: `size`, `cast`, `line_id`, `dur_s`; Rhubarb cues per line.

## Framing by size (crop the master, never repaint)
| size | zoom into master | head height on screen | chin at |
|---|---|---|---|
| WIDE | 1.0 (whole master) | ~280 px | 70 % of frame height |
| MED | 1.5 toward the speaker | ~380 px | 80 % |
| CLOSE | 2.3 toward the speaker | ~760 px | 90 % |
Close-ups at 640 px (59 % of a 1080 frame) still read as medium shots beside Dragon
Ball frames, where the face fills 65-75 % of the height; 760 px is the match.
The crop centre is pulled half-way toward the speaker's slot so the background
parallax matches the staging. CLOSE plates get the close-up treatment (2 px blur,
8 % warm overlay, soft vignette); the characters stay sharp.

## Staging slots
- Single: speaker at 56 % of width (50 % for CLOSE), 3/4 view.
- Two-shot (≥ 2 cast, speaker known): speaker at 66 %, other at 30 %, both 3/4.
- Cast-less non-FX shots (establishing wides, empty street): the plate alone with a
  4.5 % slow push over the shot's duration, so the frame is never static. Without
  this the cut has dead frames where the 3D pipeline used to put set dressing.
- FX and paper-insert shots are skipped; they keep their own frames.

## Per-frame loop (on twos)
Each cast member's expression comes from the shotlist row's per-character `emotion`
through one table to (eye state, brow state); the cel character draws it
(`cel-character-from-generated-master` v4). Speaker mouth from the cue map, everyone blinks on the same cadence, only the
speaker dips on vowel onsets, 1 px/s settle on all, then the scene-lighting pass
(`creative-arts.animation.pipeline.2d-character-scene-lighting-pass`) on the merged
character layer, composite over the plate, contrast 1.12. Cache head rasters per
`(char, view, mouth, eyes)`: ≤ 8 per character per shot (brow is fixed per shot).

## Colour script per location (the gap to 2020s anime)
Flat 1990s cels beside a Daima frame look unlit. Give every location a colour script:
character key and shade colours, a plate tint colour with its strength (6-22 %), and a
contrast. Examples that read: alley = warm key (255,205,150) with a cool blue shade
(90,100,150) and a 22 % blue plate tint; golden-hour field = (255,200,120) key, violet
shade, 20 % orange tint; overcast street = near-white key, grey-blue shade, 18 % blue
tint, contrast 0.96. Scene light is one hard cel terminator (one shadow tone), never a
gradient, and ink stays ink.

**Derive each location's script from the script, not from the look of the painting.** One street was configured as an
"overcast street" (near-white key, 18 % blue tint) because its painting is a white house with blue shadows, while the shot list
says that street is "impossibly gold" every evening. The result was cold blue wide shots in the scene whose whole point is the
false gold. For each location, grep the action lines for light words (gold, dusk, grey, dead light, flat) and set the key,
shade and tint to match. A pale painting that is cool by nature needs a strong tint: 20 % barely moved a blue-white house, and
38 % of a warm orange (255,196,118) turned it a cream gold while the dark windows and doors kept their shadows. Characters
in blue clothes stay blue; that contrast is what lets them read in gold light. Check the colour in the worst-matching wide
shot, not in a thumbnail, and keep the story's exceptions (the alley mouth where "the gold hasn't come back") on the cool script.

## Camera verbs from the shotlist (the energy is written; render it)
A shotlist that says "whip to the alley", "snap", "push in", "smash to black" and renders
every cast shot locked has thrown away its pacing. Draw plate and cast locked, then
move the camera on the finished frame per drawing:
- push = eased zoom 1.00→1.10 over the shot; pull = the reverse; empty plates push by
  default unless "static".
- track / pan / drift = lateral slide of 4 % of the width; tilt = 5 % vertical.
- whip / snap = land at 1.08 zoom from a 25 % lateral offset over the first 2 drawings,
  smeared (average of the frame and ±14 px copies), then hold tight.
- handheld / hits / bolts / flex = ±5 px shake seeded per frame.
- "bad frame" fx = one inverted drawing mid-shot; "smash to black" = last 2 drawings black.
Keep HUD/counters on top, after the camera move, so they do not shake. Clamp the crop
to the frame; the move is a crop+resize, so the plate must be painted 10 % larger than
the tightest size.

## Micro-motion (holds are never frozen)
Per character a phase from its name: body sway 2.5 px horizontal at 0.9 rad/s and 1.5 px
vertical at 1.4 rad/s; the speaker's head additionally rotates ±1.3 degrees at 0.7 rad/s
about a pivot at 60 % of its height (not in wides). Cheap, and a 3-second hold now reads
as a living drawing.

## Hand-off
Write `f_0001, f_0003, …` into the shot's render folder, then run the episode cutter
in its "reuse frames" mode with no plate overlay (the frames are already composited).
The cutter holds each drawing 2 frames from the numbering gap.

## Staging on a painted master, and patching one for continuity (verified 26 Oct 2026)

Two scenery failures were flagged by an independent review and the owner, and both were fixed without repainting.

**Stand characters where the painting has floor.** A painted master has a perspective of its own. In an alley master, the
only walkable floor was a narrow left corridor, and a large dumpster filled the foreground in the middle. Slots at 0.5 to
0.66 of the width put characters in front of the dumpster with their feet on it, which read as "standing on the
dumpster". Compose the frame with a floor map in mind: find, per master, the x range where the ground is visible, and
override the generic slots per location and shot size. Alley wide: one character at 0.24, two at 0.20 and 0.36. A
generic slot table is fine for sets where the floor spans the frame.

**Make the picture agree with the line.** A kitchen master showed a full stove and kettle while the script line was
"A warranty for an oven. There is no oven." Remove the object from the painting rather than the line:
1. Cover the lower part by copying a plain cabinet block from elsewhere on the same counter run, at the same y so
   the counter top stays level, with a 14 px feathered left edge and a 6 px top edge.
2. Cover the wall behind it with a **flat** colour sampled as the median of a clean patch of that wall. Tiling strips
   of the wall instead left visible seams and fragments of the old shelf.
3. Start the fill below any other object on that wall (a picture frame) so it isn't clipped.
4. Check it at 100 % zoom, not the thumbnail: the seams only showed in a crop.
Save it as a new master file and point the master table at it, keeping the original.

**Keep figures off props painted into the master.** A painted prop (a roadside sign) has an x range in the master, and the
generic two-shot slots (0.30 and 0.66) put a figure straight in front of it, so the board read as growing out of the head.
Measure each painted prop's x range once and override the slots for that location and size (sign spans 0.21-0.38: wide
two-shots at 0.50 and 0.72). Single figures at 0.56 were already clear.

**Overlapping painted objects (four cars nose to tail) are removed, not nudged.** Painted objects cannot be moved apart, since
the hidden parts do not exist. Paint the extras out with `creative-arts.animation.comfyui.remove-object-from-painted-master-by-masked-inpaint`
and re-render every shot of that location (all sizes show the master); an emptier street also matches "empty gold street".

## Lessons
- Keep `head_px` and `chin` in the same units as the raster you paste (the 2× trace
  render). A chin given in master units put a character's chin 400 px below the frame.
- Rim light on cool fills (a light-blue hoodie) turns orange; weight the rim by 0.35
  where blue > red.
- Pass the cast's view per slot, not per shot: the off-speaker in a two-shot still
  faces inward.

## Verify
Render one shot per size per location; a contact sheet beside a benchmark frame
must show the same medium, speaker mouths changing, and no character cut at the
neck. Then cut the whole episode: every non-FX shot has frames and the cutter
reports no slates.
