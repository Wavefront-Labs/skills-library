---
id: creative-arts.animation.pipeline.shot-renderer
name: shot-renderer
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, renderer, shotlist, staging, camera, automation, blender, data-driven]
level: practitioner
status: verified
description: "Data-driven shot renderer: read shotlist JSON, stage cast on marks, camera-by-size, lip-sync, beauty finish, skip missing assets."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Data-Driven Shot Renderer (shotlist → rendered shots)

The render-phase workhorse: ONE tool that reads `EPnn_shotlist.json` and renders
any shot, instead of a bespoke python script per shot (87 shots/ep × 10 = no).
This is the Disney "one tool, data in the seat" move — the shotlist IS the data.
Locked .blend assets + this renderer + the LLM directing = consistent episodes.

## What it does per shot
1. **Resolve assets** — `location` → set .blend (SET_MAP); `cast[]` → char .blend
   (CHAR_MAP). If any asset is missing, SKIP and log to the build queue (don't
   fake it). Only shots whose assets exist render.
2. **Stage cast** — each set has named MARKS (world pos + facing). Assign cast to
   marks (primary cast = mark A, second = mark B…). Staging marks are locked per
   set so a character stands in the same believable place every shot.
3. **Camera from shot `size`** (the key automation — see table).
4. **Animate** — lip-sync from the line's rhubarb json if `line_id` has VO
   (see vo-lipsync-pipeline); idle micro-motion (breath/sway) otherwise.
5. **Finish** — shotkit.beauty_comp + cinematic_render (shared MD tier).

## Camera-by-size (verified mapping, aim at primary cast head)
| size   | lens | distance | height      | DOF    | note |
|--------|------|----------|-------------|--------|------|
| WIDE   | 28mm | far      | eye/high    | off    | full body + environment, establish |
| MED    | 50mm | mid      | chest       | f4     | waist-up, dialogue default |
| CLOSE  | 85mm | near     | eye         | f2.2   | head/shoulders, emotion |
| INSERT | 60mm | macro    | at prop     | f2.8   | a prop/detail, not a character |
| FX/TITLE | n/a | —        | —           | —      | NOT a 3D shot: title card / glitch / grade done in comp or 2D — renderer skips, handled by fx pass |

Camera placement: put it on the set's "camera side" (keep the 180° line — see
layout-blocking), offset by shot angle hint in `camera` text (push/track/static
drive a small start→end move, not a new setup).

## Staging marks (per set, locked)
Define once per set from its layout: `MARKS = {'A': (pos, facing_deg), 'B': …}`.
Alley (verified): A=Dill (-0.55,1.1, face ~205°), B=Chip (0.35,3.9, face camera).
Marks live with the renderer's set config, not re-guessed per shot.

## Honest limits (what the renderer does NOT do)
- **No acting.** It gives lip-sync + idle. Hero performance beats (a big take, a
  gesture) are hand-animated per shot ON TOP (twelve-principles) — the renderer
  is the base layer, not the final for emotional shots.
- **Missing assets block shots.** A set or character not yet modeled = that shot
  waits in the build queue. The renderer renders the coverable subset; the queue
  drives what to build next.
- **FX/INSERT of non-existent props** need the prop built or a 2D/comp treatment.

## Gotchas (verified, bit me)
- **Face characters toward the CAMERA, not a mark's stored facing.** Cast is
  assigned to marks by index (cast[0]→A, cast[1]→B). A mark's `face_deg` was set
  for its usual occupant; a different character landing there inherits a turn that
  can point them AWAY from camera — and a back-to-camera character shows nothing
  (Chip's whole face is his screen → rendered as a blank casing until fixed).
  Fix: normalise the mark facing to [-180,180] and CLAMP to ±35° so the subject is
  always ~front/three-quarter to camera. The clamp, not the raw mark, is what
  staged on screen.
- **Self-lit characters (emissive screen/face) get NO front fill.** A fill washes
  the light casing/screen white and drowns the emissive features. Gate the fill:
  only add it when the primary is not the self-lit character.
- **Emissive face features must out-punch adjacent bloom.** A blazing backlight
  (doorway) blooms in comp over the subject; push the emissive eyes high
  (strength ~16) and keep glare threshold ≥1.0 so it bleeds less onto dark subjects.

## Verify
- [ ] Renders a shot you did NOT hand-author (proves it generalizes).
- [ ] Every character faces roughly camera (no back-to-camera blanks).
- [ ] Camera frames the primary cast correctly for the size.
- [ ] Cast stand on believable marks, facing right, 180° line held.
- [ ] Missing-asset shots are skipped + logged, not faked.

See layout-blocking (marks/180°), camera-cinematography (lens/size), shotkit,
vo-lipsync-pipeline, twelve-principles (the hand-anim layer on top).

## v2 capabilities (verified in production)
The renderer grew four verified layers beyond the original staging/camera/lip-sync core:
- **Expressions**: per-shot `emotion`/`look` tags pose the face (eyes/iris/mouth/head-tilt
  states; screen-face characters get their own state table incl. a one-bad-frame glitch).
  All feature transforms pivot about the GEOMETRY centre, never the object origin.
- **Coverage**: deterministic per-shot camera variety seeded from the shot id - yaw orbit
  with per-set clamps (180-line held), emotional height register (low = menace, high =
  vulnerable), rule-of-thirds aim offset, dutch roll on dread, raked two-shots, and no
  frozen cameras (a slow drift when no move is hinted).
- **Blocking**: action-text keywords (walks/runs/crosses/enters/crouches/turns) drive
  root-level locomotion into the mark with a cartoon step-bob - characters stop
  materialising rooted.
- **Speaker-correct lip-sync**: the viseme track lands on the cast member matching the
  line's speaker prefix, NOT blindly on cast[0].
- **--still mode**: one mid-shot frame for proof strips (see render-preflight).

## Batch hygiene (verified the hard way: a 2 h episode render killed at 7/87)
An episode is ~90 Blender launches at ~80 s each. Treat the batch like a render
farm job, not a script you watch:
- **Per-shot clips are the checkpoint.** Write each shot's finished clip to a
  `_clips/NNN_<shotid>.mp4` before moving on, and give the batch a `--resume` that
  keeps any clip already present. A killed run then costs the one shot in flight,
  not the two hours. `--shots=ID,ID` (re-render only what a QC row named, keep the
  rest) is the same mechanism from the other end.
- **One heavy job at a time on a workstation.** Blender (GPU + a few GB) next to a
  CPU neural TTS pass (another few GB, all cores) was what triggered the OS/host
  memory reaper. Queue them: render, then VO, then the re-render of the shots whose
  lines changed. Never start the second because "it's only 12 lines".
- **Don't edit the render path mid-batch.** Each launch re-imports the renderer,
  performance and character modules and re-links the character .blends, so a change
  landed mid-run gives shots 1–40 one look and 41–87 another, and the QC diff
  cannot tell a regression from the edit. Draft new behaviour in a module nothing
  imports yet, wire it in between batches, then `--shots=` the affected shots.
- **Synthesise VO to a side directory** (`--out=`), never into the directory the
  running render reads its wavs and rhubarb cues from; copy over once both are idle.

