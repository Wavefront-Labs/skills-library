---
id: creative-arts.animation.visual-development.character-visdev-exploration
name: character-visdev-exploration
category: creative-arts
field: animation
product: visual-development
tags: [character-design, character-visdev, silhouette, shape-language, proportion, costume-kit, mix-and-match, option-sheet, ensemble-cast, attitude-sheet, expression-sheet, turnaround, art-direction, pre-production, visual-development, design-options, cast-silhouette-variety]
level: advanced
status: draft
description: "Explore a single character's shape/proportion/costume options to a pitchable option sheet, before any turnaround or model is built."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character vis-dev exploration — the option sheet, not the turnaround

This skill is the *character-specific* layer of `creative-arts.animation.visual-development.concept-art`.
That skill covers the whole vis-dev discipline (thumbnails, value, keyframes, props,
environments); this one is only about exploring ONE character to a locked design, and
goes deeper than concept-art's brief section 4 does. If you need thumbnailing
fundamentals or the value/color order, read concept-art first — this file assumes them
and does not repeat them.

## 1. The deliverable is an option SHEET, not a finished drawing
A character exploration pass produces a single page (or 2-3 at most) the art director
can scan in under a minute: 8-16 small variants of the SAME character concept, grouped
by the axis being tested, each labelled A/B/C. Never present one "best" drawing first —
that collapses the director's choice to approve/reject instead of compare. Status:
unconfirmed exact count; 8-16 is the range observed to still fit on one sheet at
thumbnail size without the director needing to scroll/paginate.

## 2. Silhouette-only pass before any line work
Fill the figure flat black, no interior lines, no face. Judge only:
- Does it read as the right **archetype** (hero / villain / comic relief / elder) at a
  glance?
- Is the silhouette **distinct from every other named character in the cast** already
  designed? Overlay or place side by side at the same scale — two round-shouldered
  average-height silhouettes in one cast is the single most common vis-dev failure, and
  it is cheap to catch here and expensive to catch after modeling.
- **Negative-space pockets** (the gaps under an arm, between legs, under a hat brim) are
  part of the shape language — a design with no negative space reads as a blob.

Kill anything that fails the silhouette test before adding a single costume idea; a
good costume on a bad silhouette is wasted effort.

## 3. Proportion exploration — the head-to-body ladder
Explore the same character at 3-5 proportion settings on one strip: e.g. 8-head heroic,
6-head standard, 4-head chibi/cute, 3-head toddler-squash. Proportion alone re-casts the
read — a 4-head version of a "tough mercenary" design usually reads as comic sidekick,
which tells you fast whether the brief wants tough-and-threatening or tough-and-likable.
Lock proportion before costume: costume details drawn at the wrong proportion have to be
redrawn, not adjusted.

## 4. Costume / prop-kit mix-and-match
Once silhouette + proportion are picked, explore the character's *kit* as swappable
parts, not whole redrawn outfits each time:
- Draw one base body (the "paper doll") and 4-8 interchangeable heads, 3-6 hand-held
  props, 2-4 footwear/legwear options, 2-3 headwear options on transparent overlays or a
  simple grid.
- Recombine on paper/digitally to generate option count fast (4 heads x 3 props = 12
  looks) without redrawing the body each time. This is the vis-dev equivalent of a
  blendshape rig: separate the variables so they can be judged independently.
- Flag which combinations are structurally cheap to build later (shared topology,
  reused materials) vs. which require a one-off asset — note this on the sheet margin so
  the director's pick doesn't accidentally triple the build cost. Unconfirmed: exact
  cost deltas are production-specific; flag qualitatively (cheap/moderate/expensive) if
  you don't have real build-time numbers.

## 5. Attitude / expression sheet — acting range, not just a face
A character design isn't locked until it's been drawn doing the character's job, not
just standing neutral:
- Draw the SAME locked silhouette in 4-6 attitude poses pulled from the character's
  likely beats (confident stance, cowering, laughing, mid-run) — this is where a design
  that looked great standing still reveals it can't bend, or the costume silhouette falls
  apart in motion (a long coat reads differently standing vs. running).
- A small expression grid (6-9 faces: neutral, happy, angry, sad, surprised, scared,
  plus 2-3 show-specific ones) checks the face holds appeal and clarity at the design's
  stylization level before it's rigged. This feeds `facial-animation` and
  `blendshape-sculpting` downstream — catching a face that can't read "angry" clearly
  here is a sketch fix; catching it after shape keys are built is a rebuild.

## 6. Ensemble consistency pass (do this LAST, across the whole cast)
Once every named character has an individually-approved sheet, lay all silhouettes
together at true relative scale on one page:
- Check the shape-language **families** are deliberate, not accidental: if the brief
  wants "soft good guys, angular villains," every silhouette should sort correctly by
  shape alone with faces hidden.
- Check relative **scale and proportion read correctly as a group** (the "giant" is
  visibly giant next to the "kid" at the same panel scale) — proportion that looked fine
  solo can fail next to the cast.
- Re-open any character whose silhouette duplicates another's shape family; this is the
  cheapest point in the whole pipeline to fix it.

## Gotchas
- Don't let costume detail compensate for a weak silhouette — directors (and audiences)
  read shape before color before detail; fix order matters.
- Mix-and-match kits tempt over-combination (testing every permutation); cap it at the
  combinations that answer a real open question, not a full matrix.
- An attitude sheet drawn AFTER costume lock sometimes reveals the costume breaks in
  motion — budget a revision pass rather than treating attitude-sheet as a rubber stamp.
- Ensemble pass belongs last: comparing half a finished cast against half-sketched
  characters produces false negatives (the sketchy one looks weaker for being sketchy,
  not for being wrong).

## Verify
- [ ] One option sheet per character, 8-16 labelled variants, scannable in under a
      minute.
- [ ] Passed the silhouette-only test (flat black, no face) before any costume was drawn.
- [ ] Proportion was explored and locked as its own pass, separate from costume.
- [ ] Costume/prop kit explored as swappable parts (paper-doll method), not full
      redraws.
- [ ] At least one attitude/action pose and one expression grid exist for the locked
      silhouette before sign-off.
- [ ] Final silhouette checked against the rest of the named cast at true relative
      scale; no two leads share a shape family.

See `creative-arts.animation.visual-development.concept-art` (the general vis-dev
process this specializes), `creative-arts.animation.blender.facial-animation` and
`creative-arts.animation.blender.blendshape-sculpting` (where the expression sheet
feeds next), and character-design-craft (the refinement pass after this one locks).
