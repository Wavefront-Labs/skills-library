---
id: creative-arts.animation.editorial.continuity-supervision
name: continuity-supervision
category: creative-arts
field: animation
product: editorial
tags: [continuity-supervision, continuity, screen-direction, 180-rule, axis-of-action, eyeline-match, prop-continuity, costume-continuity, lighting-continuity, state-tracking, catch-before-render, script-supervisor, editing]
level: advanced
status: draft
description: "Guard continuity across shots: screen direction/180-line, eyeline matching, prop/costume/lighting continuity, state tracking, and catching errors before render."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Continuity supervision — keeping the world consistent across every cut

Continuity supervision is the discipline of making sure that what the audience sees in one
shot agrees with the shot before and after it: characters face consistent directions, look
at the right off-screen points, hold props in the right state, wear the right costume, and
sit under consistent light. In live action a script supervisor does this on set; in a cel
3D pipeline it is an **editorial and pre-render** responsibility, and its governing virtue
is **catch it before render** — a continuity error found on the farm or in the final cut is
the most expensive error in the show. This skill guards the cuts that `editorial-pacing`
makes and the assets that `production-design`, `prop-design`, and `costume-design` lock. It
is tightly coupled to `layout-blocking` and `camera-cinematography`, where screen direction
is actually set.

## 1. Screen direction and the 180-degree line (axis of action)

The single most common and most jarring continuity break. The rule: for a given scene,
draw an imaginary **line of action** (between two characters, or along a character's
movement) and keep the camera on **one side** of it across all coverage. Then:

- **Character A stays frame-left looking right; Character B stays frame-right looking left**,
  in every shot. Cross the line and A suddenly appears to face the wrong way — the audience
  loses the geography.
- **Movement keeps direction.** A character exiting frame-right must enter the next shot
  from frame-left (continuing left-to-right travel). A car driving screen-right stays
  screen-right across cuts or it reads as turning around.
- **Legitimate line crossings** must be *shown*: a cut on a camera move that crosses, a
  neutral head-on shot as a buffer, or a character physically crossing in frame. A hidden
  cross is an error; a motivated one is fine.
- **Check this at layout**, before animation — fixing an axis break after blocking means
  re-staging and re-animating the shot.

## 2. Eyeline matching

Where a character looks must point, across the cut, at what they're looking at.

1. **Height and direction must agree.** If A (seated) looks up-and-right at B (standing),
   B's reverse must have the camera/eyeline looking down-and-left at A. Mismatched eyelines
   make two people in the same room feel like they're in different rooms.
2. **Off-screen look targets are real points in space.** When a character looks at an
   off-screen object, the look direction and angle must match where that object actually is
   in the staging — track the object's position even when it's not on camera.
3. **Keep eyelines consistent through a conversation.** Don't let a character's gaze drift
   from one reverse to the next; lock the eyeline target per shot.
4. In the 3D pipeline, eyelines are driven by the rig's aim/look constraints staged against
   the real set layout — verify them against the set, not by eye on an isolated character.

## 3. Prop and costume continuity (state tracking)

Props and costumes carry *state* that must march correctly with story time and never reset
across a cut.

- **Prop state.** The glass that is half-full must not be full in the reverse and half
  again in the next wide. The lit cigarette shortens; the door that was opened stays open.
  Track each hero prop's state (full/empty, on/off, intact/broken, position) per shot.
- **Costume state.** A torn sleeve stays torn; a wet coat stays wet until the story dries
  it; a removed hat stays off. Costume variants (`costume-design`) must be the right variant
  in each shot.
- **Position hand-off.** An object set down in shot A is where it's picked up in shot B —
  same screen position and state. A character's pose/hand at a cut should roughly match
  across the cut (the "matching action" of a match cut).
- **Use the asset registry.** Because props/costumes are locked assets with registered
  variants (`production-design`), continuity tracking = making sure each shot links the
  correct variant and sets the correct animated state. A continuity log per sequence (shot,
  prop states, costume variant, notable positions) is the working document.

## 4. Lighting continuity

Light must be consistent within a scene and move correctly with story time.

- **Within a continuous scene**, key direction, color, and intensity match across all
  coverage — a character warmly lit from the left in the wide can't be cold-lit from the
  right in their close-up (unless the staging justifies it).
- **Across story time**, light changes deliberately and monotonically: a sunset scene gets
  progressively warmer/lower; it doesn't bounce brighter then darker between cuts.
- **Practicals stay consistent**: a lamp that's on stays on and lights faces the same way
  in every shot of the scene. In the cel pipeline this means the shots in a scene share a
  lighting setup/rig so the cel ramp reads identically (pairs with `lighting`).

## 5. The catch-before-render discipline

The entire value of continuity supervision is **where** you catch the error. Enforce gated
reviews, cheapest first:

1. **Reel/board review.** Screen direction, eyeline intent, and major prop/costume beats are
   visible on boards — catch axis breaks and state resets here, when a fix is a redraw.
2. **Layout review.** The real staging exists; verify the 180-line, eyelines against the
   set, and prop positions. This is the critical gate — most continuity errors are cheapest
   to fix at layout.
3. **Blocking/animation review.** Verify matching action across cuts, prop state animation,
   and that the correct asset variants are linked.
4. **Pre-render review (last gate).** A pass of each sequence *in cut order* checking the
   full continuity checklist. Nothing goes to the farm with an open continuity note — a
   re-render is the whole shot's compute cost paid twice.
5. **Final-cut review.** A last continuity watch of the assembled cut in order; by here
   errors are expensive, so this is a safety net, not the main defence.

The habit that makes it work: **always review shots in cut order, side by side with their
neighbours**, never in isolation. Continuity only exists *between* shots, so an isolated
shot review can't see it.

## 6. The continuity log

Maintain a per-sequence log as the working document: for each shot — screen-direction side
(axis), each character's frame position and look direction, hero prop states and positions,
costume variant, lighting setup. Update it as the reel matures from boards to final. This
log is what lets one person (or an automated pre-render check) verify a 50-shot sequence
without holding it all in their head, and it ties directly to the `production-design` asset
registry for variant correctness.

## 7. Worked example — a continuity log entry

A three-shot beat at the diner counter, logged so a 50-shot sequence stays consistent
without anyone holding it in their head:

```
SEQ 04 — Diner confrontation   | axis: along the counter, camera stays NORTH side
SH 0410  WIDE   A frame-left (look R) · B frame-right (look L) · coffee: A half / B full
                 · A costume: coat ON · key: warm practical from counter lamp, left
SH 0415  OTS→B  B frame-right (look L, down to seated A) · coffee B: full
                 · B costume: apron tied · key matches 0410 (warm, left)
SH 0420  CU  A  A look UP-right (to standing B) · coffee A: half, mug in right hand
                 · A coat ON · key warm from left — MATCHES
```

The log makes three checks trivial: (1) A is always frame-left/look-right and B frame-right/
look-left — axis held; (2) A's coffee is "half" in both her shots, B's is "full" in both his
— no state reset across cuts; (3) key light is warm-from-left in all three — lighting
continuous. If shot 0420 came back from the farm with A's coffee full or the key swung to the
right, the log catches it at pre-render, not in the final cut. The log is kept against the
`production-design` asset registry so "coat ON" resolves to the correct locked costume variant
and "mug in right hand" to the registered half-full prop variant.

## Verify

- [ ] Each scene has a defined **axis of action**; across all coverage the camera stays on
  one side, character screen-positions and look-directions are consistent, and movement
  keeps direction (exits/entries match). Any line cross is **motivated and shown**.
- [ ] **Eyelines match** in height and direction across reverses, off-screen look targets
  point at their real staged positions, and gaze is consistent through each conversation.
- [ ] **Prop and costume state** is tracked per shot and never resets across a cut; objects
  hand off in the same position/state; the correct locked **asset variant** is linked in
  each shot.
- [ ] **Lighting** is consistent within each continuous scene (key direction/color/intensity,
  practicals) and changes monotonically with story time.
- [ ] Continuity is checked at **gated reviews** (reel → layout → blocking → pre-render →
  final), with layout and pre-render as the hard gates; **nothing renders with an open
  continuity note**.
- [ ] Shots are reviewed **in cut order, side by side with neighbours**, not in isolation.
- [ ] A **per-sequence continuity log** (axis, positions, look directions, prop/costume
  state, lighting setup) exists and is kept current from boards to final.
