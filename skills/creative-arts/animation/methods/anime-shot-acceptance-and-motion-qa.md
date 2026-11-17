---
id: creative-arts.animation.methods.anime-shot-acceptance-and-motion-qa
name: anime-shot-acceptance-and-motion-qa
category: creative-arts
field: animation
product: methods
tags: [method, recipe, qa, review, motion, continuity, acceptance-criteria, independent-review, contact-sheet, pop-in, contact, agents]
level: advanced
status: draft
description: "Recipe: QA that catches what stills miss: per-shot acceptance lists from the script, 6 fps motion strips, an independent reviewer and automatic object checks gating assembly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Method: shot acceptance and motion QA

A **method** is a recipe. This one replaces "the maker looks at a few stills" with a loop that catches
broken motion, missing actions and objects that pop in or out.

**Why:** on one episode, the maker's own still-frame checks passed every cut. The owner then found hands that
weren't real, an orange that never went down the drain, and papers appearing from nowhere. An independent
reviewer using this method then failed 67 of 87 shots, and almost every pass was a talking-head close-up.

## Steps

1. **Acceptance list per shot, written from the script before anyone looks at frames.** For each shot:
   `must_see` (concrete visible events), `contacts` (who touches or holds what), `objects` (where each one
   comes from and goes: frame edge, container or hand), and `continuity` (what must match the previous shot).
   Write it from the shot list alone, so the picture can't bias it.
2. **Motion strips.** Every shot of the cut as frames at 6 fps, tiled 6 per row, with the action and line in
   a header. Use real shot starts from the assembly, not summed durations.
3. **Independent review.** A reviewer that didn't make the shot (a fresh agent with only the strips, the shot
   list and the acceptance lists) gives each shot PASS or FAIL. Each failure names what is wrong, the row and
   column, and what should happen. The summary ranks the most damaging problems and groups failures into
   categories.
4. **Automatic object checks.** The renderer logs every object's box per frame, with kind (prop, container,
   hand) and holder. Then flag:
   - **pop-in:** first seen away from the frame edge and not overlapping a container or hand;
   - **pop-out:** gone before the shot ends, away from the edge and not inside a container;
   - **contact:** a held object more than 0.6 hand-sizes from the nearest hand.
   On first use this caught all 9 papers spawning mid-air in one shot.
5. **Gate.** Assembly builds the strips and runs the object checks on every cut. A cut isn't done while any
   object check is red, or while the review has a failure the owner hasn't waived.

## Limits

- Strips at 6 fps can miss one-frame events, like a single bad frame. Hold such events for 2 to 3 frames, or
  review that shot at 24 fps.
- Boxes can't show layering, such as an object that should pass behind grate bars. That stays with the
  reviewer.
- The reviewer judges picture only. Check sound against picture separately: effects for events not on screen
  read as noise.

## Acceptance

Every shot has an acceptance list, a strip, a review verdict and clean object checks before the cut goes to
the owner.

See `editorial.script-to-picture-audit` (the one-off audit this automates),
`sound-design.tts-dialogue-intelligibility-gate`, and `methods.anime-episode-2d-tier` (phase 8).
