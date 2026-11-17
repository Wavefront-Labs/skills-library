---
id: creative-arts.animation.methods.anime-character-design-sheet-tier
name: anime-character-design-sheet-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, character-design, model-sheet, turnaround, expression-sheet, hand-sheet, model-pack, consistency, draw-once, 2d, quality-tier]
level: advanced
status: draft
description: "Recipe: skills, order and gates to produce a modern-anime character model pack (master, turnaround, expression and mouth sheets, hands) that a 2D puppet and animators can draw from without drift."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Method: anime character design sheet (model pack) tier

A **method** is a recipe, not a technique. Every "how" is a link to a skill.

**Outcome:** a model pack per character — one approved master, a turnaround (front,
3/4, profile, back), an expression sheet, a mouth chart, a hand sheet and a size
comparison — such that every later drawing (puppet layer, key pose, in-between) is
checked against it and nothing drifts. This is what a 2D studio hands to animators;
without it, "consistency" is a wish.

**Status: draft.** Phases 1–2 were executed end to end for four characters (three
traced masters + one pure-vector mascot; parametric front and 3/4 faces; variant sheets). Phases 3–5 (profile/back, hands, size chart)
are the industry-standard order and bundle verified skills, but the full pack has not
yet been produced for one character in this pipeline. Gates there are targets.

---

## Ingredients

| Phase | Skill |
|---|---|
| Master | `creative-arts.animation.comfyui.anime-character-master-on-amd-directml` |
| Master | `creative-arts.animation.character-design.lead-character-design` |
| Master | `creative-arts.animation.character-design.iconic-and-simple-characters` |
| Master | `creative-arts.animation.character-design.silhouette-breakers` |
| Master | `creative-arts.animation.comfyui.dbz-line-and-flat-character-master` |
| Face | `creative-arts.animation.pipeline.cel-character-from-generated-master` |
| Face | `creative-arts.animation.character-design.anime-face-construction` |
| Face | `creative-arts.animation.character-design.anime-hair-as-one-mass` |
| Face | `creative-arts.animation.character-design.expression-range-per-character` |
| Face | `creative-arts.animation.character-design.expression-design` |
| Face | `creative-arts.animation.principles.mouth-shapes-and-chart` |
| Turnaround | `creative-arts.animation.character-design.model-sheet-turnaround` |
| Turnaround | `creative-arts.animation.character-design.construction-sheet` |
| Turnaround | `creative-arts.animation.character-design.head-tilt-and-angle-in-expression` |
| Turnaround | `creative-arts.animation.vector-graphics.parametric-features-over-traced-master` |
| Hands | `creative-arts.animation.character-design.cartoon-hands-and-hand-sheets` |
| Cast | `creative-arts.animation.character-design.character-size-comparison-sheet` |
| Cast | `creative-arts.animation.character-design.cast-contrast-in-a-lineup` |
| Cast | `creative-arts.animation.character-design.one-style-rule-set-across-the-cast` |
| Cast | `creative-arts.animation.art-direction.master-palette-specification` |
| Cast | `creative-arts.animation.art-direction.skin-tone-palettes` |
| Check | `creative-arts.animation.character-design.model-sheet-do-and-dont-callouts` |
| Check | `creative-arts.animation.art-direction.on-model-checks-across-departments` |

## Ordering law
The master fixes silhouette, palette and proportions; the face is built to the
master; the turnaround is derived from the master (traced or drawn to its
construction lines), never from a second generation; hands and the size chart come
last because they depend on the final proportions. Do-and-don't callouts are written
only after the pack exists, from the errors found while making it.

## Phases and gates
1. **Master.** One prompt, ≥ 4 seeds, choose one. For a cel (Dragon Ball) tier
   generate it as line+flat and keep its pixels (bust + body masters); for a painted
   tier trace it. *Gate:* owner signs the
   still; silhouette reads at 64 px; palette sampled by region medians and written
   into the master palette.
2. **Face and mouths.** Parametric front and 3/4 face; 4 mouth shapes; ≥ 3 brow
   states; 3 eye states. *Gate:* 12-variant sheet reads as one person; mouth chart
   covers the lip-sync map.
3. **Turnaround.** Profile and back drawn on the master's construction lines
   (head heights, eye line, shoulder and hip widths carried across with guide
   lines). *Gate:* heights and widths match the front within 2 %; hair mass volume
   matches in every view.
4. **Hands.** ≥ 8 hand poses in the character's line style (open, fist, point, grip,
   hold-small-object, hold-large-object, relaxed, splayed). *Gate:* each reads at
   80 px; finger count obvious.
5. **Cast sheet.** All characters at true relative height on one sheet, with
   palette swatches. *Gate:* every pair of characters is distinguishable by
   silhouette alone.
6. **Callouts.** Do/don't sheet from the mistakes made in 1–5.

## Acceptance criteria
- Any new drawing of the character can be overlaid on the matching view of the pack
  with features within 2 % of position and size.
- A cold viewer identifies each cast member from a 64 px silhouette.
- The pack is the only reference given to the puppet and to any animator.

## Failure modes this prevents
- Regenerating the character per view or per shot.
- Hair and outfit that change volume between views.
- Hands invented per shot (claws, wrong finger counts).
- A cast that reads as one person in different clothes.

## Verify
Produce the pack for one character in one sitting; log every gate; mark this method
`verified` when phases 3–5 have been executed and the gates held.

## Run log
- 22 Oct 2026: traced painted masters judged "not real anime" by the owner against a Dragon Ball
  frame. Rebuilt the cast as line+flat cel masters with blink/mouth replacement cels only; first
  all-2D cut (73 shots, close/medium/wide) reads at 1990s Dragon Ball level beside Daima.
  Still open: head turns (no generated 3/4), hard-edged cel shadow pass, hands, turnarounds.
