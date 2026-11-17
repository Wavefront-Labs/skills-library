---
id: creative-arts.animation.storyboarding.thumbnail-to-storyboard-workflow
name: thumbnail-to-storyboard-workflow
category: creative-arts
field: animation
product: storyboarding
tags: [animation, storyboarding, thumbnails, thumbnail-pass, pacing, previs, sequence-finding, boarding-process, throughput, production-workflow, story-artist]
level: practitioner
status: draft
description: "Thumbnail small, fast, and in batches before cleaning a single panel, to find staging and pacing cheaply."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SKILL: Thumbnail-to-storyboard workflow

This is the **production process** of getting from a script page to a clean sequence of
panels — the order of operations, batch sizing, and time budget that keeps a board
artist fast. `creative-arts.animation.storyboarding.storyboarding` covers what makes a
panel *good* (composition, staging, acting); this skill covers the *pipeline* that
gets you there without wasting hours cleaning panels that die in revision. The
distinction matters because the single biggest time-sink in boarding is skipping this
workflow and jumping straight to clean art.

## Why thumbnail first
A thumbnail is a 1-2 inch box, drawn in under a minute, that answers one question:
does this staging work? At that size you cannot render detail, so you are forced to
solve composition, staging, and shot size — exactly the decisions that are expensive to
change later. Cleaning a panel before the sequence works at thumbnail scale means every
revision throws away finished art. In practice a 22-minute episode script page (roughly
1-3 shots) should produce 3-8 thumbnails per shot as alternates before one is picked —
if you're drawing one "final" thumbnail per shot, you're not thumbnailing, you're
pre-cleaning.

## The pass structure
Work in three distinct passes, never mixed within a sequence:
1. **Beat pass (no drawing).** Read the scene, list the beats (moments where staging,
   composition, or acting changes — see the parent skill). Write one line per beat.
   This is a text list, not art, and it's where shot count gets decided before any
   panel exists. Skipping this and thumbnailing straight from the script is how
   sequences end up over-boarded (padding beats that didn't change) or under-boarded
   (missing a beat that needed its own panel).
2. **Thumbnail pass (batch, whole sequence).** Thumbnail every beat in the sequence
   before cleaning any of them. Work small (postage-stamp, pencil or a stylus at low
   zoom) and fast — minutes, not an hour, per panel. Batching the whole sequence at
   thumbnail scale lets you see pacing and shot-size variety across the *sequence*,
   which you cannot judge one clean panel at a time. Flag 2-3 alternates on any beat
   that's acting-heavy or geography-tricky (crossing the line, a reveal) rather than
   committing to the first idea.
3. **Clean pass (only survivors).** Clean only the thumbnails that survived a read
   (ideally a read with the director or lead, even an informal one). Cleaning is where
   time actually gets spent, so gate it behind approval, not behind "I already drew it."

## Batch sizing and cadence
- Thumbnail a whole sequence (typically 1 scene, 3-15 shots) in one sitting before
  switching to clean art. Context-switching per-panel between thumbnail and clean mode
  is slower than batching, because staging decisions made on panel 3 often change
  panel 1 and 2 — you want all of them loose at once.
- Keep a rough shots-per-hour budget for the thumbnail pass (on a known show this is a
  measured number from past sequences; if you don't have one yet, track your own first
  few sequences and use that — this skill can't give you a universal number it hasn't
  verified). The budget exists so a thumbnail pass that's running long gets flagged as
  a script/scene problem, not quietly absorbed by working later.
- Don't thumbnail ahead of locked dialogue/VO if the show records scratch VO before
  boarding — timing assumptions baked into thumbnails at that stage get invalidated
  by the real read. Where the show board-then-records, thumbnail against the script
  timing and expect the boardomatic pass to retime.

## Tools and setup
- Low-res, low-color canvas (even a 2-bit pencil brush) on a thumbnail-sized canvas
  (roughly 400-600px wide) forces you to stay loose; a full-res canvas invites
  premature detail.
- Keep thumbnails for a sequence on one sheet or one timeline track so size/pacing
  variety is visible at a glance (see the parent skill's "vary the sizes" rule) —
  scrolling through separate files hides repetition.
- Grease Pencil or any raster app works; the tool doesn't matter as much as the canvas
  size discipline. **Unconfirmed**: specific thumbnail-grid templates or keyboard-driven
  batch tools vary by studio/software and aren't verified here — note your own setup if
  you adopt this.

## Gotchas
- **The "nice thumbnail" trap.** A thumbnail that took 10 minutes because you kept
  refining it isn't a thumbnail anymore — it's a slow clean panel with no clean line
  quality. If a thumbnail is taking longer than the beat next to it, you're solving a
  staging problem; stop drawing and write the problem down instead.
- **Thumbnailing in isolation from the sequence.** A single thumbnail can look fine and
  still be the fourth medium shot in a row. Always re-scan the whole batch before
  moving to clean.
- **Letting approval lag the clean pass.** If clean art starts before a read/approval
  on the thumbnails, you lose the entire point of the pass — you're back to expensive
  revisions on finished panels.

## Verify
- [ ] A beat list exists for the sequence before any thumbnail was drawn.
- [ ] Every beat has a thumbnail, and acting-heavy/tricky beats have 2-3 alternates.
- [ ] The full thumbnail batch was reviewed together (pacing, shot-size variety) before
      any panel entered the clean pass.
- [ ] Clean art exists only for thumbnails that passed that review.
- [ ] Elapsed time on the thumbnail pass was tracked, so the next sequence's budget is
      based on a real number, not a guess.

If a sequence is in revision trouble (a note undoes several clean panels at once), the
fix is almost always upstream: re-run the beat pass or thumbnail pass rather than
patching clean art directly.
