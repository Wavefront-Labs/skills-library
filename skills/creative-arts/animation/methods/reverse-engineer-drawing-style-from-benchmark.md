---
id: creative-arts.animation.methods.reverse-engineer-drawing-style-from-benchmark
name: reverse-engineer-drawing-style-from-benchmark
category: creative-arts
field: animation
product: methods
tags: [method, recipe, drawing, style-matching, reference, benchmark, hands, anatomy, line-weight, cel-shading, anime, side-by-side]
level: advanced
status: draft
description: "Recipe: reach a benchmark show's drawing quality one body part at a time: reference crops, written rules, draw, side-by-side, correct, record the skill."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Method: reverse-engineer a drawing style from a benchmark

A **method** is a recipe. This one turns "make it look like Dragon Ball" into rules a drawing process can
follow, one body part at a time, and turns each verified rule into a skill.

**Origin:** a show owner, looking at hands that "didn't look real", proposed: put a Dragon Ball hand side by
side, reverse-engineer the skills and recipes needed to make that body part, then expand to the rest of the
body.

## Order of parts

Work in the order the audience notices failure: hands, then face and eyes, hair, arms and sleeves, torso and
clothing folds, legs and trousers, feet and shoes, then props held in hands. Hands go first because they
carry most interaction and break most visibly.

## Loop for each part

1. **Collect 6 to 10 benchmark crops** of the part in different states: open, closed, holding, foreshortened,
   at close-up and at wide size. Use full-resolution frames, not thumbnails. Keep them in a reference folder
   with source and timestamp.
2. **Write the rules down** under five headings: line (weight, colour, open or closed strokes), shadow
   (number of tones, edge, placement), construction (the simple volumes underneath), grouping and overlap,
   and detail by screen size. Each rule cites the crop it came from.
3. **Draw ours** applying only those rules.
4. **Side by side:** our drawing beside two or three benchmark crops at the same scale. Mark which rules
   transferred and which didn't, with the evidence.
5. **Correct once,** then go back to step 4. Stop when two passes show no improvement on a rule. That rule
   needs a different tool, not more passes.
6. **Record:** add the rules that held to the part's skill (version bump), and note the ones that didn't
   transfer, with what's needed instead.

## What the first part taught

On hands, line and shadow rules transferred in one pass. Construction (3D form, foreshortening, fingers
wrapping an object) didn't transfer when curves were placed from imagination. Expect this split for every
part: **style rules** (line, shadow, colour, detail level) are recipes a drawing process can follow directly,
while **construction rules** need a 3D form under the drawing, such as a posed 3D model, a pose skeleton or
a pose-guided generation. Plan each part's tooling around that split.

## Acceptance

- Every part has a reference folder, a written rule set and a filled side-by-side.
- An independent reviewer, shown our part and the benchmark crops without labels, can't reliably say which
  rules ours breaks.

See `character-design.cartoon-hands-and-hand-sheets` for the hand rules, `character-design.anime-face-construction`
and `character-design.anime-hair-as-one-mass` for the next parts, and `editorial.script-to-picture-audit` for
finding which parts fail first.
