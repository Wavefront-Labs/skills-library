---
id: creative-arts.animation.blender.previsualization
name: previsualization
category: creative-arts
field: animation
product: blender
tags: [previs, previsualization, blocking, proxy, camera, timing, staging, blender, shotlist, auto-previs, feasibility]
level: advanced
status: docs-checked
description: "Build a cheap 3D previs in Blender: proxy assets, cameras blocked to the shotlist, timed to VO, to lock timing, staging and feasibility before production."
sources:
  - https://docs.blender.org/api/current/bpy.types.TimelineMarker.html
  - https://docs.blender.org/api/current/bpy.types.Camera.html
  - https://docs.blender.org/manual/en/latest/animation/markers.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

The workflow, lens choices, resolutions and timings in this skill are production practice, not values from the Blender manual; the Blender marker/camera behaviour and Python properties were checked against the manual and API docs.

# SKILL: Previsualization (previs)

Previs is a **rough, fast, throwaway 3D pass of a sequence** built to answer three
questions before production commits: does the timing work, does the camera/staging
work, and is it *feasible* to build and shoot. In a production pipeline, previs sits between the
boardomatic and full `layout-blocking`: the board proves the sequence in pictures,
previs proves it in 3D space and real time, layout then builds it for keeps. Previs is
cheap on purpose — if a previs shot is pretty, you over-built it.

Distinct from `layout-blocking` (which assembles the *real* shot from locked assets for
final animation) and from `storyboarding` (2D panels). Previs is the 3D dress rehearsal
in between. Pairs: `camera-cinematography`, `shot-renderer`, `shotlist-boarding`,
`story-reel-editorial`, `animation-blocking-to-polish`.

## The previs contract: block, don't build
Everything in previs is a stand-in. The rules keep it fast:
- **Proxy everything.** Characters are a sized capsule + a cube "head" with a forward
  arrow (so facing reads); sets are blocked greyboxes at true scale; props are the
  primitive that gives the silhouette. Never append the locked, finished asset — that
  belongs to layout.
- **True scale is non-negotiable.** The one thing previs must get right is *metric
  scale*. A proxy character is a real-height capsule; a doorway is real width; the
  camera lens is a real focal length. Everything else is a lie, but scale is truth, or
  the timing and staging you lock are wrong.
- **Grey, flat, fast.** One flat material, no textures, EEVEE viewport or a
  Workbench render. If you're lighting previs, stop.
- **Throwaway by default.** Previs feeds decisions, not the final file. The camera
  animation and timing are the deliverables; the geometry is scaffolding.

## Build a previs scene from the shotlist (data-driven)
In a shotlist-driven pipeline the JSON is the source of truth, so previs is generated from
it, not hand-assembled. Each shot row carries at least: `shot_id`, `duration`,
`camera` (position/target/lens), `set`, and the characters with rough marks. Drive the
scene from that:

    import bpy, json
    shots = json.load(open("<REPO>/episodes/ep01/shotlist.json"))["shots"]
    fps = bpy.context.scene.render.fps
    t = 1
    for s in shots:
        cam = bpy.data.objects[f"cam_{s['shot_id']}"]  # one camera per shot
        cam.location = s["camera"]["loc"]
        cam.data.lens = s["camera"]["lens_mm"]
        # bind camera to the shot's frame range via a Timeline marker
        m = bpy.context.scene.timeline_markers.new(s["shot_id"], frame=t)
        m.camera = cam
        t += round(float(s["duration"]) * fps)
    bpy.context.scene.frame_end = t

Binding **one camera per shot to a timeline marker** (in the UI: select the camera and
marker, `Marker → Bind Camera to Markers`, `Ctrl B`; in Python `marker.camera`, the
"camera that becomes active on this frame") gives you the whole sequence playing as cuts
in the viewport — the camera switches at each marker exactly as the edit will. This is the 3D equivalent of the boardomatic, and it is the same marker/
camera convention `layout-blocking` will reuse, so the previs camera blocking *is* the
first draft of the real cameras.

## Block the cameras to the shot, hold the grammar
Previs is where camera decisions get cheap and testable. Block, in viewport:
- **Lens for the intent.** Wide (18-24mm) opens space and distorts for energy; long
  (85mm+) compresses and isolates. Pick the lens that serves the beat, per
  `camera-cinematography` — previs is where you discover the board's "close-up" actually
  needs an 85mm from across the room, not a 35mm shoved in a face.
- **Hold the 180-line across cuts.** Because every camera plays in sequence off the
  markers, line breaks show up immediately as a facing flip. Catch them here.
- **Block the move, time the move.** If the shot pushes in, keyframe the push on the
  proxy camera and *watch it at speed*. A move that's too fast or too slow is a timing
  bug you fix in two keyframes now, not a reshoot later.
- **Check feasibility.** Does the camera clip the set? Can the character actually reach
  the mark in the shot's duration? Is there room for the crane move the board drew?
  Previs exists to find the "we can't actually shoot this" before anyone builds it.

## Time to the VO
Timing is the headline deliverable. Load the scratch VO as a sound strip in the Video
Sequencer (or a speaker in the scene) and set each shot's marker spacing from the real
line delivery, not an even guess.
- **Cut against the recorded dialogue.** A line that needs 2.3 seconds gets 2.3 seconds
  of shot; the shotlist `duration` is then *updated from previs*, not the other way
  around. Previs is allowed to push timing back upstream.
- **Play it at real speed, repeatedly.** The entire value of previs is watching the
  sequence at 24fps with sound. Scrubbing lies; playback tells the truth. If a beat
  drags or a cut lands early, retime the markers and play again.
- **Feed the reel.** Export the previs playblast (`shot-renderer` in a flat/preview
  mode) and cut it into the story reel so editorial judges real 3D timing, not panels.
  This closes the loop with `story-reel-editorial`.

## Our shot-renderer as auto-previs
Because the pipeline is data-driven, the same `shot-renderer` that produces final frames
can produce previs frames straight from the shotlist — point it at proxy assets and a
flat/workbench render preset. That makes previs *regenerable*: change a camera or a
duration in the JSON, re-run the renderer, get an updated previs with zero manual
re-assembly. Treat this as the default:
- Keep a `previs` render preset (Workbench or flat EEVEE, reduced resolution and samples,
  proxies substituted for locked assets by name).
- Re-run on any shotlist change; the previs playblast is a build artifact, not a
  hand-made file.
- This is the bridge that makes previs continuous with the rest of the pipeline rather
  than a one-off department.

## Staging and acting in previs (rough, but real)
Previs blocks performance at the coarsest useful level — enough to judge timing and
staging, never to judge acting:
- **Marks and facings, not poses.** Slide the proxy capsule to its mark at the right
  frame; rotate it to its facing. That's the performance resolution previs needs — where
  a body is and which way it points, timed to the line. Finger acting is animation's job.
- **Key the big moves on 2s or steps.** Block proxy motion in stepped/constant
  interpolation so you read *timing* (when the move happens) without being seduced by
  smooth tweens. This is the same stepped-blocking habit as
  `animation-blocking-to-polish`, one resolution cruder.
- **Eyelines and crosses.** Make sure two characters can actually look at each other on
  the boarded eyeline and that a cross doesn't walk a proxy through a wall — cheap geometry
  problems to find now.
- **Negative space for the cut.** Leave the proxy where the next shot's eye-trace expects
  it; previs is where you confirm the board's cut flow survives real 3D space.

## How previs hands off to layout and animation
Previs outputs, in priority order: **updated per-shot durations**, **blocked cameras**
(positions, lenses, moves on markers), and **rough character marks/timing**. Layout
(`layout-blocking`) inherits the cameras and marks and replaces proxies with locked
assets; animation (`animation-blocking-to-polish`) inherits the timing and the staging
intent as its first blocking pass. Nothing about the previs *geometry* survives — only
the decisions. If layout finds itself keeping previs meshes, previs was over-built.

## Common previs failures
- **Over-building.** Textured, lit, detailed previs wastes the one advantage previs has:
  speed. Grey and fast, always.
- **Wrong scale.** The one thing you can't fake. A capsule at the wrong height makes
  every timing and framing decision a lie.
- **Scrub-only review.** Decisions made while scrubbing are wrong; previs must be judged
  at real-time playback with VO.
- **Previs that outlives its purpose.** Once layout has the cameras and timing, the
  previs file is done. Keep the decisions (in the shotlist), discard the scaffolding.

## Verify
A previs pass is valid when:
- [ ] Every proxy is at **true metric scale** (character heights, doorways, lenses all
      real).
- [ ] The scene is **driven from the shotlist JSON** (one camera per shot, bound to a
      timeline marker) and regenerates when the JSON changes.
- [ ] The full sequence **plays as cuts** in the viewport at real-time 24fps with the
      **scratch VO** loaded — judged at playback, not scrub.
- [ ] Every camera has a **lens chosen for the beat** and the **180-line holds** across
      all cuts.
- [ ] Each blocked **camera move is watched at speed** and retimed until it reads.
- [ ] **Durations have been pushed back to the shotlist** where previs found the board's
      timing wrong.
- [ ] A **previs playblast** (via `shot-renderer` preview preset) is cut into the story
      reel for `story-reel-editorial`.
- [ ] The scene contains **only proxies** — no locked/final assets, no lighting, no
      textures. If it's pretty, it's over-built.

Pass all boxes before layout begins; layout inherits the cameras and timing, not the
geometry.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and current Python API docs.
Confirmed: `TimelineMarker.camera` ("camera that becomes active on this frame"); `scene.timeline_markers.new(name, frame=)`; `Camera.lens` (focal length in mm); Bind Camera to Markers (`Ctrl B`) behaviour; Workbench render engine; stepped (Constant) interpolation via the Graph Editor. Removed: "EEVEE Next" naming, "no AA passes, half-res" preset details and fixed lens ranges (no doc coverage; practice).
Method: documentation only; no commands were run.
