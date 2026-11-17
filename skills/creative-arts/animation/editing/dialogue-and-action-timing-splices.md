---
id: creative-arts.animation.editing.dialogue-and-action-timing-splices
name: dialogue-and-action-timing-splices
category: creative-arts
field: animation
product: editing
tags: [cut-on-action, j-cut, l-cut, split-edit, lead-frame, lag-frame, overlap-trim, dialogue-cutting, frame-precise, splice, pacing, premiere, resolve, avid, trim-mode]
level: practitioner
status: draft
description: "Frame-precise splice placement for dialogue and action cuts: cut-on-action offsets, J/L split edits, lead/lag trims."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dialogue and Action Timing Splices

**Goal: place the actual cut point on the frame that reads as invisible (action) or as
natural speech rhythm (dialogue), not on the frame the shot happens to end.** This is a
different problem from `creative-arts.animation.editing.rough-cut-assembly-and-story-
reels` (which alternate wins) and from `creative-arts.animation.editing.animatic-
assembly` (locking a shot's total `dur_s` across pipeline maturities) — those answer
*which* clip and *how long*; this skill answers **exactly which frame the splice falls
on inside an already-chosen clip**, which is where a cut reads as smooth or as a jolt.

## Cutting on action

A cut hidden inside continuous motion reads as invisible because the eye is tracking
movement, not the frame line. The splice point is not "where shot A ends" — it's a
frame *inside* the action, matched on both sides:

- Find the motion's peak energy (a hand crossing frame, a foot planting, a head
  turning through its fastest arc) and cut on the frame closest to that peak in **both**
  clips, not just the outgoing one. A cut one or two frames early/late from true match
  is the single most common cause of an action cut feeling "off" without an obvious
  reason why.
- For a turn/whip-pan style cut, cutting a few frames *into* the blur on each side
  (rather than at the first/last sharp frame) hides the join better than a clean-to-
  clean cut — the eye is already in motion-blur tolerance.
- When two takes don't have frame-matched motion (common with alternate boards/angles
  that weren't shot to match), add 2-6 frames of overlap trim on the incoming clip so
  the new motion has a beat to establish before the cut lands, rather than matching an
  impossible frame.

## Dialogue splices: lead and lag

A straight cut exactly at a line's first/last phoneme reads clipped, because real
speech has breath and consonant attack before the sound a transcript marks as the
start:

- **Lead-in**: start the incoming clip 2-4 frames *before* the audible onset of the
  line (at 24fps) so a soft consonant or breath isn't guillotined. Too much lead and
  you hear a mouth-open silence; too little and the first consonant is clipped.
- **Lag-out**: hold the outgoing clip 2-6 frames past the last audible phoneme,
  especially on a sentence ending in a plosive or sibilant — cutting exactly on
  perceived silence usually cuts off the tail of the sound still decaying.
- **Cut on the breath, not the word**, when trimming a line for pace: removing the
  in-breath before the next line (rather than words within a line) shortens pace
  without making the actor sound like they're skipping syllables.

## J-cuts and L-cuts (split edits)

A straight cut moves picture and sound on the same frame; a split edit moves them on
different frames:

- **J-cut**: next shot's **audio** starts before its picture (so you hear the next
  speaker start before you cut to them) — used to motivate a cut by giving the audience
  a reason (a new voice) before the picture changes.
- **L-cut**: current shot's **audio** continues after the picture has cut away (so
  dialogue plays over a reaction shot of the listener) — used to show how a line lands
  rather than who's saying it.
- In Premiere/Resolve, build these by unlinking A/V on both clips and dragging only the
  audio or video edge past the other's cut point; in Avid, use "Add Edit" + drag the
  unlinked sync point. Keep both clips' audio and video selected as separate linked
  groups so a later ripple-trim doesn't re-sync them back to a straight cut by accident.

## Gotchas

- **Frame rate changes the lead/lag numbers.** 2-4 frames at 24fps is ~83-167ms; the
  same splice at 30fps needs 3-5 frames for an equivalent feel. Don't copy a frame count
  across a project with a different fps without converting to ms first.
- **Trim-mode vs. ripple matters.** A dialogue lead/lag trim should usually be a
  **roll trim** (moves the cut point, both clips' total duration on the timeline stays
  fixed) so fixing a splice doesn't push every downstream clip's timecode. Reach for
  ripple only when you intend the overall cut to get shorter/longer.
- **Match the motion, not the pose.** A cut matched on two static end-poses that looks
  fine paused will still jolt in playback if the velocity into the pose differs between
  clips — scrub at normal speed, not frame-by-frame, to judge the final feel.

## Verify

- [ ] Play the cut at real speed (not frame-stepped) and confirm the splice doesn't
      read as a jolt — frame-accurate on paper can still feel wrong at speed.
- [ ] For an action cut, confirm the motion's energy/direction roughly matches across
      the splice frame on both sides, not just that the shot lengths add up.
- [ ] For a dialogue cut, confirm no consonant or breath got guillotined by scrubbing
      ±5 frames around the splice with audio on.
- [ ] For a J/L cut, confirm the unlinked A/V survived any later ripple trim (re-check
      sync after any timeline reorder).

Status: draft — these are standard live-action/animation editorial conventions
(cut-on-action, split edits, lead/lag trims); frame counts above are typical starting
points, not measured against a specific verified in-house cut. Note any project-
specific numbers that worked (or didn't) here rather than opening a competing skill.
