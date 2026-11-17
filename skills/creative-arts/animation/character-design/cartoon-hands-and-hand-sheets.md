---
id: creative-arts.animation.character-design.cartoon-hands-and-hand-sheets
name: cartoon-hands-and-hand-sheets
category: creative-arts
field: animation
product: character-design
tags: [character-design, model-sheet, cartoon-hands, hand-sheet, hands, gesture]
level: practitioner
status: draft
description: "Design cartoon hands and a hand sheet: finger count, palm-finger proportions, simplified knuckles and a set of standard gestures drawn on model."
sources:
  - https://books.google.com/books?vid=ISBN9780823023493
  - https://books.google.com/books?vid=ISBN9781560100843
  - https://en.wikipedia.org/wiki/Rubber_hose_animation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cartoon hands and hand sheets

Goal: hands consistent with the character's style and a sheet of the gestures the
character uses most.

## Design decisions
- **Finger count**: four (three plus thumb) is standard for cartoon; it reads cleaner and
  is cheaper to draw. Five for realistic or lead characters in some styles.
- **Palm vs finger length**: palm about equal to finger length in realistic anatomy;
  cartoon often shortens fingers and enlarges the palm (mitten feel) or the reverse for
  elegant characters.
- **Shape language**: round sausage fingers (friendly), tapered pointed fingers (villain),
  square blocky hands (strong).
- **Knuckle and nail detail**: decide once; usually none or minimal.
- **Gloves**: classic rubber-hose style; state cuff shape and inner lines.

## The hand sheet
- Relaxed, fist, open palm, pointing, grasping a cylinder, holding a small object,
  thumbs up, waving, hand on hip, character-specific gesture.
- Front, back and side of the relaxed hand.
- Size reference against the face (hand roughly chin-to-brow length in most styles).

## Method
1. Construct the hand as a palm box plus a thumb wedge plus finger cylinders.
2. Curve the knuckle line in an arc, not a straight row.
3. Draw the standard gestures from that construction.
4. Check the hand size in the full figure and in a close-up.

## Anime (Dragon Ball) hand rules, reverse-engineered from frames

Read off full-resolution Dragon Ball Daima and 1990s Dragon Ball Z frames of an open raised hand, a clenched
fist, hands on hips and a grab. Use them when the show's target is that look.

1. **Line:** thin and near-uniform, about 0.25 % of frame height. Use a dark warm brown on skin and a darker
   tint of the fill on gloves and cloth, not thick black. Interior strokes (palm creases, finger gaps, fist
   folds) are open: they stop short of the contour and never form closed shapes.
2. **Shadow:** one hard-edged shadow tone per material, a darker and slightly desaturated fill, laid as thin
   slivers that follow the form on the side away from the light. No gradients and no extra highlight tones.
3. **Grouping:** fingers grouped and overlapping, each a different length and curve. The index partly hides
   the middle finger, and so on. Evenly fanned, equal fingers read as a rubber glove.
4. **Construction:** the palm is a wedge or box. Each finger has three segments that bend at the joints. The
   thumb comes from a heavy base low on the palm. A fist is a box with front, top and side planes, with the
   shadow on the underside plane.
5. **Detail by size:** at medium shot a hand gets 3 to 5 interior strokes, and nails disappear. A close-up
   adds fold strokes; nails appear only in an insert.

**Tested limit (25 Oct 2026):** applying rules 1, 2 and 5 to a vector hand gripping a can brought its line and
shading close to the reference in one pass. Rules 3 and 4 did not transfer by placing curves from
imagination: the fingers still lay on the can like tubes instead of wrapping, foreshortening and hiding their
tips. Construction needs a 3D form underneath, either a posed 3D hand projected and inked, or a pose-guided
drawing, before these style rules are applied.

## Failure modes
- Fingers all the same length and parallel (bunch of bananas).
- Hands shrinking or growing between shots.
- Mixing four- and five-finger hands in the same cast without reason.

## Verify
- [ ] Finger count and detail rules written.
- [ ] Sheet has 10+ gestures on model.
- [ ] Size relationship to face stated.

Related: `creative-arts.animation.character-design.construction-sheet`,
`creative-arts.animation.principles.prop-handling-animation`.
