---
id: creative-arts.animation.blender.pose-planning-thumbnailing
name: pose-planning-thumbnailing
category: creative-arts
field: animation
product: blender
tags: [blender, planning, thumbnails, poses, silhouette, line-of-action, staging, eyeline, reference, acting-out, key-poses, shot-planning, storytelling, pre-blocking]
level: advanced
status: draft
description: "Plan a Blender shot before touching the rig: thumbnail strong storytelling poses, silhouette and line of action, act out reference, plan eyeline and staging."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pose planning & thumbnailing (before you touch the rig)

The dead-even look the owner rejects is usually decided *before* anyone opens Blender —
in the planning that didn't happen. A feature animator spends a real chunk of a shot's
time thinking, acting, and scribbling thumbnails, then blocks fast and confident because
the thinking is done. This skill is that front end: it produces the strong storytelling
poses that `animation-blocking-to-polish` Stage 1 blocks. Plan poorly and you polish a
dead performance; plan well and blocking is almost mechanical. Control/face names are the
Rigify + `facial-rig` sets.

## Start from the beat, not the rig

Before any drawing, know what the shot is DOING (this overlaps `acting-performance` —
do that reading here):

- **One idea per beat.** Break the shot into beats and write the single intention of each
  in four words or fewer ("dismiss it", "anger leaks", "she caves"). If you can't, you
  don't know the beat yet and the pose will be mush.
- **Find the changes.** Acting lives in the transitions — where the character decides,
  looks away, lands on a word. Mark those frames against the audio; they become your key
  storytelling poses.
- **Know the camera.** You pose for ONE camera. A pose that reads in a 3/4 front shot can
  be invisible in profile. Set/know the shot camera before thumbnailing — you're
  designing what *that lens* sees, not a sculpture in the round.

## Thumbnail the storytelling poses

Thumbnails are small, fast, ugly drawings — 10-30 seconds each, matchstick figures are
fine. The point is quantity and clarity of idea, not draftsmanship. (Can't draw at all?
Act the pose and shoot a phone photo, or rough-pose the rig in a throwaway file — but
drawing is faster to iterate and forces you to commit to a read.)

For each key beat, thumbnail the pose that says the beat in one image, and test it
against three things:

- **Silhouette.** Fill the pose solid black in your head (or squint at the thumbnail). If
  you can't tell what the character is doing from the black shape alone, the pose doesn't
  read. Keep the storytelling elements (the pointing hand, the turned head, the slumped
  shoulder) OUTSIDE the body mass where they register on the silhouette — hands crossed
  in front of the torso vanish. This is the single most useful test in animation.
- **Line of action.** One clean sweeping line (C-curve or S-curve, or a strong straight
  for rigid/stubborn) through the whole body from head to feet. It unifies the pose and
  carries the energy. A pose with no line of action, or with two fighting lines, reads as
  limp. Draw the line first, hang the figure on it.
- **One idea.** The pose commits to the beat's single intention and nothing else. Don't
  stack three ideas into one pose — they cancel and you get neutral mush (the dead-even
  look at its source). Push it further than feels safe; strong poses survive splining,
  timid ones go mushy.

Thumbnail the **extremes** (the storytelling keys), not the in-betweens — those are the
poses you'll block stepped. Lay them in a row to see the shot as a sequence of reads; the
flow from pose to pose IS the shot.

### Worked example: "It's fine. / I said it's fine."

Two beats, ~90 frames, 3/4 front camera on Dill:

- **Beat 1 — dismiss (subtext: it is not fine), ~f0-40.** Thumbnail: weight on the back
  foot, shoulder turned slightly away from the other character, a limp dismissive hand
  flick *out past the silhouette* so the gesture reads. Line of action: a lazy backward
  C, leaning away. Eyeline: breaks contact, glances down/aside on the flick — the
  look-away IS the subtext.
- **The change, ~f40-48.** The decision to stop pretending. Thumbnail the transition
  pose: the weight starts coming forward, the eyes snap back to the other character. This
  is the beat the whole shot hangs on; thumbnail it specifically, don't let blocking find
  it.
- **Beat 2 — shut it down (subtext: anger leaking), ~f48-90.** Thumbnail: weight forward
  onto the front foot, shoulders squared to the target, chin slightly down, a sharper
  straighter line of action (stubborn = straight, not curved). Hand now still and set,
  not flicking. Direct, locked eyeline. The silhouette is wider and more frontal than
  beat 1 — the body language reversed, which is what sells the gear-change.

Three thumbnails (two extremes + the change) with frame numbers = a plannable shot. Note
the eye snaps back at ~f40 (2-3f before the body commits) and a blink on the gear-change.

## Act it out and shoot reference

Feature animators are performers with a mouse. Get up and **act the beat** — multiple
takes, to the audio, exaggerated. You'll discover timing, weight shifts, and gestures you
would never invent sitting still. Shoot it on a phone from the shot camera's angle.

- Reference is for **timing, weight, and ideas you can steal**, not for rotoscoping. A
  frame-accurate copy of a human reads as mocap, not animation; take the essence and
  push it. Note on the footage where the weight shifts and where the accents land — those
  frame numbers seed your blocking timing.
- For a creature or Chip (the floater), act the *intent* and *weight* even if the body's
  wrong — how it leans into a decision, how it recoils — then translate to the anatomy
  (see `creature-locomotion`).

## Plan eyeline and staging

The eyes carry the thought; stage for them deliberately before blocking:

- **Eyeline:** decide exactly where the character is looking each beat and where it darts
  on each change. Eyes LEAD — the eye goes to a new target 1-3 frames before the head
  follows. Map the eye targets now (what are they looking at, and when do they break
  contact?) so blocking has a plan instead of a dead forward stare. For a two-shot, nail
  that the eyelines actually connect — characters looking at each other must genuinely
  point at each other's eyes for that camera.
- **Staging:** arrange the pose and the character's placement so the important thing is
  the clearest thing in frame and nothing competes with it. Keep the key gesture off the
  body's silhouette, don't let a twin pose (both arms identical, symmetrical stance) flatten
  the energy — break symmetry so the pose has a front foot, a lead hand, a tilt. Plan the
  negative space; the shape of the gap around the character reads as much as the figure.

## Hand off to blocking (key-poses-first discipline)

The output of this skill is a planned shot ready for `animation-blocking-to-polish`:

- A row of thumbnail extremes (the storytelling poses), each with a frame number against
  the audio.
- Eye targets and the beat where each change/dart happens.
- Reference footage with weight-shift and accent frames noted.

**Key-poses-first discipline:** you block ONLY these planned storytelling poses first,
stepped, and prove the read before adding anything. The temptation to start smoothing or
adding detail before the key poses are approved is exactly what produces the dead shot —
resist it. If the thumbnails are strong and the read works stepped, the rest of the
pipeline is execution. If you skipped planning and are "finding it in the rig", you'll
burn the budget discovering the shot doesn't work after you've already polished it.

## Verify (pass/fail)

- [ ] Every key beat has **one four-word intention** written down, and the shot's
      **changes/transitions** are marked against the audio. (fail = no plan, dead-even)
- [ ] A **thumbnail extreme exists for each storytelling pose**, with a frame number —
      not a vague mental picture. (fail = finding it in the rig, over budget)
- [ ] Each key pose passes **silhouette** (readable as a black shape, gesture off the
      body mass) and has a clear **line of action**. (fail = unreadable / limp pose)
- [ ] Each pose commits to **one idea**, pushed, with broken symmetry — not three ideas
      averaged into neutral. (fail = mush)
- [ ] Poses are designed **for the shot camera**, and **eyelines/eye targets** are planned
      per beat (eyes lead the head). (fail = reads from the wrong angle / dead stare)
- [ ] Reference was **acted and shot** (timing/weight noted), used for essence not
      rotoscope. (fail = invented stiffly or copied frame-for-frame)

See `acting-performance` (the beat reading this builds on), `animation-blocking-to-polish`
(where these poses get blocked), `body-mechanics` (weight in the poses), `facial-animation`
(eyeline/thought), `twelve-principles`, `creature-locomotion` (non-biped intent).
