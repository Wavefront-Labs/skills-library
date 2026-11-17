---
id: creative-arts.animation.storyboarding.storyboarding
name: storyboarding
category: creative-arts
field: animation
product: storyboarding
tags: [storyboarding, story-art, panels, staging, composition, screen-direction, acting, shot-flow, boardomatic, revisions, grease-pencil]
level: advanced
status: draft
description: "Draw and assemble story panels that stage a scene: composition, screen direction, acting choices, shot flow, and the boardomatic, in a 3D/cel pipeline."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Storyboarding (story art)

Storyboarding is the first time the script becomes **pictures that move through time**.
A board is not illustration and not a shot list — it is *directing on paper*: deciding
where the camera is, who is where, what the acting is, and how one image cuts to the
next. In a production pipeline the board is where staging, performance intent, and edit are
locked cheaply, before a single locked asset is appended into a scene.

Distinct from `shotlist-boarding`, which produces the shot-list **data** (the JSON rows
the pipeline renders from). This skill is the craft of making the panels themselves.
The two meet at the boardomatic: boards drawn here, timed against the data there.
Pairs: `story-reel-editorial`, `layout-blocking`, `camera-cinematography`,
`grease-pencil-2d`, `screenwriting-craft`.

## The board tells the story in the fewest panels that are unambiguous
Every panel earns its place by answering a question the previous panel left open. The
sequence is the unit, not the drawing. Panel count is driven by **beats of change**:
a new panel when staging, composition, or acting changes — not on a timer. A held
two-shot that doesn't change for three seconds is one panel with a duration, not three
drawings. Draw clarity, not detail: a strong silhouette with a clear eyeline beats a
rendered portrait that reads slowly.

## Composition: stage the frame, don't just fill it
Each panel is a deliberate composition carrying the story moment:
- **Read in one second.** The subject must win the frame by size, contrast, placement,
  or lines of force. If the eye hunts, restage. Squint at the panel — the thing you
  still see is what reads; it must be the point.
- **Frame the correct size.** Choose the shot size for emotional distance: wide for
  context/isolation, medium for interaction, close for interiority. Boarding the wrong
  size is the most common note — don't board a confession in a wide.
- **Depth in three planes.** Place something foreground, mid, and back. A flat panel
  reads as flat staging and will translate to a flat 3D layout.
- **Lead the motion/look.** Leave space in front of a moving or looking subject (nose
  room). Space behind a looker reads as blocked or trapped — use it only on purpose.
- **Point with the frame.** Diagonals, doorways, railings, and light shafts are tools
  to aim the eye. In cel this doubles as line-economy: fewer, stronger lines.

## Staging and the 180-degree line
Staging is the choreography of bodies in space, drawn so the audience never gets lost:
- **Establish, then stay on the line.** Pick the axis between the two anchors (two
  characters, or character-and-object) and keep the camera on one side across the cut.
  Left-facing stays left-facing. Crossing the line without a neutral/on-axis transition
  flips screen direction and reads as a geography error — the single most disorienting
  board mistake. This is the same 180-line discipline that `layout-blocking` enforces in
  3D; fixing it on paper is free, fixing it after assembly is not.
- **Clear silhouettes, clear eyelines.** Pose every figure so the action reads in black
  silhouette. Draw eyelines deliberately: who looks at whom tells the audience who has
  power and what matters in the frame.
- **Entrances and exits respect direction.** A character exiting frame-right should
  re-enter frame-left in the next space, or the geography breaks.

## Acting choices: one clear idea per panel
A board performs. Each panel states **one acting intent** — a single, readable thought
or emotional beat — through pose, expression, and the line of action. Rules:
- **One idea per panel.** If a character is both scared and defiant, that's two panels
  (or the transition between them), not one muddy face.
- **Strong line of action.** The spine-to-intent curve should read from the thumbnail.
  This is the drawn ancestor of `twelve-principles` (pose, exaggeration) and feeds
  `animation-blocking-to-polish` directly — the key poses you board become the key poses
  animation blocks.
- **Board the change, not the hold.** The storytelling is in the *transition*: calm →
  alarm, open → guarded. Draw the before and after; the inbetween is animation's job.
- **Hands and eyes carry it.** In a cel show with simplified faces, the acting often
  lives in gesture and eyeline more than in the mouth.

## Shot flow: board the edit, not just the shots
The sequence must cut. Board transitions on purpose:
- **Match the cut to the beat.** Cut on action, on a look, or on a line's end. Boarding
  tells editorial *where* the cut wants to be.
- **Vary the sizes.** Avoid cutting between two near-identical sizes/angles (a "jump");
  alternate wide/medium/close to give the eye rhythm and the scene shape.
- **Mind the eye-trace.** Place the subject of panel B where the eye already is after
  panel A, or deliberately move it to create a jolt. Random eye-trace across cuts reads
  as choppy even when each panel is fine.
- **Arrows and notes.** Annotate camera moves (push, truck, pan) and in-frame action
  with arrows. A board without move-arrows under-specifies the shot for layout.

## Boarding in a 3D/cel pipeline: three legitimate methods
The board does not have to be hand-drawn. Pick the method per shot by what's cheapest
for the information needed:
1. **Hand panels (or `grease-pencil-2d`).** Fastest for acting, composition, and 2D FX
   intent. Draw thumbnails first (postage-stamp size) to find the staging, then clean
   only the panels that survive. Use Grease Pencil when you want the panels to live in
   the same file as the eventual layout, or to reuse a drawn FX element later.
2. **3D blockout boards.** For complex camera moves, continuity of a built environment,
   or tricky geography, pose proxy/locked assets in Blender and grab viewport frames as
   panels. This is the bridge to `layout-blocking` and overlaps with previsualization —
   a 3D board *is* a rough previs frame. Cheaper than hand-drawing a hard perspective.
3. **Hybrid.** 3D-grab the environment and camera, draw the acting over it in Grease
   Pencil. Best of both: correct geography, expressive performance.

Whatever the method, the output normalizes to the same thing: numbered panels with
durations, shot-size, move notes, and a dialogue/action caption — ready for the
boardomatic.

## The boardomatic (story reel)
A boardomatic is the panels cut to the soundtrack scratch VO and timing — the story
first played at speed. It is where the board stops being drawings and becomes the
movie's skeleton.
- **Time to the VO.** Hold each panel for its real intended duration against the
  recorded scratch dialogue, not an even beat. A joke that dies on paper dies here too —
  and here it's still free to fix.
- **Cut on the boarded transitions.** Honor the cut points you drew; if a cut fights the
  VO, that's a note back to the board or the script.
- **This is the input to `story-reel-editorial`.** The boardomatic is the first pass of
  the reel; editorial then refines pacing and the board iterates against it. In a
  data-driven pipeline, panel durations here seed the per-shot timing that
  `shotlist-boarding` carries forward.

## Revision workflow: version, don't overwrite
Boards live or die by iteration, so make iteration cheap and traceable:
- **Thumbnail → rough → clean.** Never clean a panel before the sequence works at
  thumbnail scale. Cleaning doomed panels is the biggest waste of board time.
- **Version sequences, not individual panels.** Keep `seq_v01`, `seq_v02` so a note
  ("go back to the v2 staging on the gate") is recoverable. Date and tag each pass.
- **Carry the note on the panel.** When a note lands ("too wide," "cross the line,"
  "no clear eyeline"), write it on the panel and address it in the next version so the
  reasoning survives the revision.
- **Push new panels through the boardomatic before declaring done.** A panel that reads
  in isolation can still break the cut; the reel is the only real test.

## Verify
A boarded sequence is done when:
- [ ] Every panel **reads in one second** at thumbnail scale (squint test: the subject
      is the thing that survives).
- [ ] Shot **sizes vary** across cuts — no jump-cut between near-identical framings.
- [ ] The **180-degree line** holds across the whole sequence (or every crossing uses a
      neutral/on-axis transition); screen direction is consistent entrance-to-exit.
- [ ] Each panel states **one acting intent** with a clear line of action and
      deliberate eyeline.
- [ ] Every camera move and in-frame action is **annotated** (arrows / notes); layout
      could be staged from the board alone.
- [ ] Panels carry **durations, shot-size, and captions** and normalize to the
      pipeline's panel format regardless of draw method.
- [ ] A **boardomatic** exists, cut to scratch VO, and plays without an unintended
      attention drop — handed clean to `story-reel-editorial`.
- [ ] Sequence is **versioned** (`seq_vNN`), with notes carried on the affected panels.

If any box fails, revise the sequence (not just the panel) and re-run the boardomatic.
