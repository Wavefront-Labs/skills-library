---
id: creative-arts.animation.blender.animation-blocking-to-polish
name: animation-blocking-to-polish
category: creative-arts
field: animation
product: blender
tags: [blender, blocking, stepped, breakdowns, spline, polish, workflow, dope-sheet, graph-editor, keyframe, favoring, overshoot, approval, pose-to-pose, animation-pipeline]
level: advanced
status: docs-checked
description: "The feature workflow in Blender: stepped blocking, breakdown pass, spline conversion and the chaos after, then polish — what each pass is for and when to show it."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/animation.html
  - https://docs.blender.org/manual/en/latest/animation/keyframes/keying_sets.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

The workflow stages, frame counts, timings and ratios in this skill are animation practice, not documented values; only the Blender tool names, menus and shortcuts were checked against the manual.

# Blocking → breakdowns → spline → polish (the shot workflow)

This is the spine every other animation skill hangs on. A shot is not
"animated" in one pass — it is built in four deliberate stages, each with a different
job, a different mindset, and its own approval gate. Skip a stage or blur two together
and you get the thing the owner keeps rejecting: lip-flap riding on idle sway, no
staging, polish lavished on a dead performance. Do `pose-planning-thumbnailing` first;
this skill assumes you already have thumbnails and a plan. Control names are the Rigify
set from `rigging` (`hand_ik.L/.R`, `foot_ik.L/.R`, `torso`/`chest`/`hips`, `head`,
`root`) plus the face controls from `facial-rig`.

## Stage 1 — Blocking (STEPPED, storytelling keys only)

Blocking is where you prove the shot *reads*. Nothing else. You set the strongest poses
— the ones from your thumbnails — on the frames where the story lands, and you look at
nothing but whether the acting works.

- **Set interpolation to CONSTANT (stepped) before you key anything.** Graph Editor ▸
  select all channels ▸ `T` ▸ **Constant** (Key ▸ Interpolation Mode), or set
  **Default Interpolation** in Preferences ▸ Animation ▸ F-Curves so every new key is
  stepped. Stepped means the rig snaps
  from pose to pose with no in-betweens — you are watching a slideshow of your keys, and
  that is exactly what you want. A spline in-between here will lie to you: it will make a
  weak pose look passable because the computer smoothed the gap.
- **Key only storytelling poses.** For a dialogue beat that's "dismiss, then anger leaks
  through", that might be just four poses across 90 frames: the pre-beat settle, the
  dismissive shrug at f12, the gear-change look-away at f48, the hard landing on "fine"
  at f66. Four poses, not forty. Each is a full-body key (choose the built-in **Whole
  Character** keying set in the Timeline's Keying popover, which keys the properties likely
  to be animated on a character rig and skips technical bones such as those Rigify
  generates, then insert with the rig selected) so the pose holds as one idea.
- **Key on whole-body, favour the extremes.** Every pose is a strong extreme from your
  thumbnails: clear silhouette, a line of action, weight over support. Push them further
  than feels comfortable — blocking that looks "about right" goes mushy the instant you
  spline it.
- **Set your timing here.** Because it's stepped, the spacing of the keys in the dope
  sheet IS the timing. Slide keys in the Dope Sheet (`G`) until the beats land on the
  right frames against the audio. A held pose that reads as a decision wants real
  screen time (practice: many frames, not a single frame).
- **Add the key storytelling breakdown if a transition is ambiguous**, but keep it
  stepped. If the look-away could read two ways, drop ONE stepped pose mid-transition to
  nail which way the head leads.

**Approval gate:** show blocking for acting/timing approval *before* going further. This
is the cheapest possible point to change the performance — there are four keys to move,
not four hundred. The director is approving the idea, the staging, and the timing, and
should be told explicitly it's stepped so nobody critiques smoothness. Get a yes on the
beats here or you will polish the wrong shot.

## Stage 2 — Breakdowns (still stepped, how you get from A to B)

Approved blocking tells you *what* poses; breakdowns define the *path* between them —
the single most important pass for making motion feel like it has intent rather than
being a straight computer tween. You stay stepped so you keep authoring the in-betweens
yourself instead of letting the spline invent them.

- **Add the breakdown pose between each pair of extremes** — the halfway (in spacing,
  not necessarily in time) pose that decides the arc of the transition. For a head turn
  from screen-left to screen-right, the breakdown is where the chin dips and leads, so
  the head arcs down-and-across instead of sliding flat.
- **Favouring:** a breakdown is almost never a true 50/50 average. Push it toward one
  extreme — "favour the second pose" — so the move hangs on the first pose then whips to
  the second, or vice versa. Favouring is how you control ease without a curve yet:
  breakdown near pose A = slow-out of A; breakdown near pose B = slow-into B.
- **Overshoot and settle, blocked as poses:** where a move should arrive with weight,
  add a stepped key *past* the target, then a key easing back. Hand reaches, overshoots
  the mug at f30, settles onto it at f36. You are blocking the overshoot as real poses so
  it survives the spline — overshoot added only in the graph editor later tends to read
  as an accident.
- **Break the arcs through the body:** chest leads, head follows a frame or two behind,
  hand drags. Offset these as breakdown poses now so the spline pass has the lag built
  in rather than everything arriving on the same frame.
- **This is where a shot becomes watchable while still stepped.** Good breakdowns make
  stepped blocking read almost like finished animation in staccato. That's the signal
  the pass worked.

**Approval gate (optional but recommended on hero shots):** a second look at blocking +
breakdowns catches arc and favouring problems while they're still cheap. On background
shots you can roll straight on.

## Stage 3 — Spline (convert, then survive the chaos)

Now you let the computer interpolate. **Expect it to look worse before it looks better**
— this is normal and every experienced animator braces for it.

- **Convert:** select all channels in the Graph Editor ▸ `T` ▸ **Bézier**, and set handle
  type to `V` ▸ **Auto Clamped** as a starting point (Auto Clamped prevents the phantom
  overshoots that plain Auto handles throw on every key). The stepped slideshow becomes
  smooth motion.
- **The chaos:** suddenly things float, drift, overshoot where you didn't want them, and
  slip-slide. This is because the spline is now inventing every in-between according to
  the curve shape, and the default curves are bland and slow-in/slow-out on *everything*,
  including things that should snap. Breakdowns you blocked keep it from being total mush
  — that's why they came first.
- **Do NOT start polishing randomly.** Work the body big-to-small: get the `root`/`torso`
  path clean first, then `hips`/`chest`, then limbs (`hand_ik`/`foot_ik`), then head,
  then face. A clean spine curve makes every downstream limb easier.
- **Kill the first obvious lies:** feet that now slide during contacts (lock `foot_ik`
  flat across the plant — see `body-mechanics`), hips that float where they should drop,
  arcs that the spline straightened. Fix path and timing here, not texture.
- **Check it against the blocking read.** If splining weakened a beat, your extremes
  weren't pushed far enough — go back and push the blocking pose, don't try to rescue it
  with curves. Re-approval is rarely needed here; spline should deliver the approved
  blocking, just smooth.

## Stage 4 — Polish (the pass that sells it)

Polish is everything that turns clean motion into a living performance. It is the
longest pass and the one with no single "done" — you stop when the shot reads and the
budget's spent, not when it's perfect.

- **Curve cleanup:** go through the Graph Editor and remove float — the slow aimless
  drift on channels that should be still or should snap. Flatten dead channels, sharpen
  curves that should be snappy (flat-then-fast), delete redundant keys (`X`), simplify.
  This is the craft in `graph-editor-polish` — do that pass here.
- **Overlap and follow-through, refined:** the drag you blocked gets tuned to the frame —
  forearm trails the upper arm by a couple of frames, hand trails the forearm, Ivy's antennae/hair
  whip and settle after the head stops. Offset keys in the Dope Sheet (`G X <n>`).
- **Settles:** nothing hard-stops. Every arrival gets a small overshoot-and-settle over
  few frames (practice: heavier = more frames, less overshoot). A head that stops dead on the target
  reads as CG; one that eases past a hair and settles reads alive.
- **Texture / breaking the even-ness:** vary the amplitude and timing so no two moves
  are identical. Add moving holds (the character keeps a hair of motion during a held
  pose — never a frozen frame). This is where you break the "dead-even" look directly.
- **Eye darts and blinks (the thought):** eyes lead every change — the eye darts to the
  target a frame or more *before* the head turns to it (practice). Add blinks on thought changes and
  direction changes (not on a metronome). This is `facial-animation` / `lip-sync`
  territory and it is where "acting" actually lands; a polished body with dead eyes still
  reads dead.
- **Final once-over at speed and in silhouette:** play at 24fps real-time, then view in
  silhouette (a flat matte) to confirm poses still read. Polish that only works frame-by-
  frame but mushes at speed isn't done.

**Approval gate:** final/polish review. The director is now signing off the finished
performance. In a data-driven pipeline the shot then goes to the renderer; the
procedural baseline from `procedural-idle-life` rides UNDER this hand work as the
always-on floor, never as a replacement for it.

## Where the other skills plug in

- `pose-planning-thumbnailing` → feeds Stage 1 (you block the thumbnails).
- `acting-performance` → *what* the poses mean; done before blocking, verified at Stage 1.
- `body-mechanics` → weight/arcs you block in Stage 2 and refine in Stage 4.
- `graph-editor-polish` → the curve craft of Stage 4.
- `facial-animation` / `lip-sync` → the eye/mouth layer in Stage 4.
- `mocap-retarget` → when motion comes from capture, you skip 1-3 and enter at Stage 4
  polish over baked curves.

## Verify (pass/fail)

- [ ] Blocking was done **stepped** with only storytelling poses, and shown for
      acting/timing approval before any splining. (fail = polishing an unapproved read)
- [ ] A **breakdown pass** exists: breakdown poses with deliberate **favouring** and
      blocked-in **overshoot**, authored while still stepped. (fail = straight computer
      tween between extremes)
- [ ] After spline conversion, feet are locked on contacts and hips/arcs match the
      blocked read — no float, no slide, no weakened beats. (fail = spline chaos left in)
- [ ] Polish pass present: curve cleanup, overlap/follow-through, settles on every
      arrival, moving holds, eye darts leading head turns, blinks on thought changes.
      (fail = clean but dead)
- [ ] Shot reads at full 24fps real-time **and** in silhouette, not only frame-by-frame.
      (fail = mush at speed)
- [ ] Each approval gate was hit in order (blocking → [breakdowns] → polish); nothing was
      polished before its read was signed off. (fail = wasted the budget on the wrong shot)

See `pose-planning-thumbnailing`, `acting-performance`, `body-mechanics`,
`graph-editor-polish`, `facial-animation`, `lip-sync`, `twelve-principles`,
`procedural-idle-life`.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: `T` Interpolation Mode and `V` Handle Type (Auto Clamped) in the Graph Editor Key menu; Preferences > Animation > F-Curves Default Interpolation / Default Handles; built-in Whole Character keying set (selected in the Keying popover; ignores technical bones such as Rigify's); Dope Sheet `G` to move keys. Fixed: "New F-Curve Defaults" is Default Interpolation under F-Curves; `I` ▸ Whole Character replaced by the keying-set selection. Removed: 8-16 frame hold, 2-3f/4-10f/1-3f timing figures (marked as practice).
Method: documentation only; no commands were run.
