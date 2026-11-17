---
id: creative-arts.animation.principles.appendage-overlap
name: appendage-overlap
category: creative-arts
field: animation
product: principles
tags: [animation, follow-through-overlap, appendage-overlap, tails, hair, ears, cloth, capes, drag, follow-through, secondary-motion]
level: practitioner
status: draft
description: "Animate tails, ears, hair, capes and loose clothing so they drag, overshoot and settle believably after the body moves, by hand or on top of a simulation."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Appendage overlap

Goal: loose parts attached to a character move after the body, continue past where it stops,
and settle - the classic "follow through" of Thomas and Johnston's principle 5.

## Rules of thumb
1. **Delay** - the appendage starts moving later than its attachment point; longer and lighter
   parts delay more (a long tail more than a short ear).
2. **Drag shape** - while the body accelerates, the appendage curves backward, tip last.
3. **Overshoot** - when the body stops, the appendage keeps going past its rest position.
4. **Settle** - decaying oscillation back to rest; 2-3 diminishing swings for light material,
   1 for heavy material, none for stiff.
5. **Weight scale** - heavy fabric (leather coat) moves less, settles fast; silk and hair move
   more and settle slower.

## Method (chain: tail, ponytail, cape corner)
1. Animate the base/attachment.
2. Rotate the first segment opposite to the base's acceleration, offset 1-2 frames.
3. Copy the curve to each next segment with increasing offset (1-2 frames per segment).
4. Reduce amplitude near the root, increase toward the tip.
5. Check that the tip traces a smooth figure-of-eight or wave path, not a jitter.

## With simulations
Many productions simulate hair/cloth then art-direct: pin regions, adjust stiffness, or
replace the sim on hero shots with keyed animation for timing control. Always animate the
base performance assuming the sim will lag; do not "help" the sim with exaggerated body moves.

## Failure modes
- Appendages moving in lockstep with the body: stiff and plastic.
- Equal offsets on each segment with equal amplitude: a rigid rod swinging.
- Endless oscillation: settles must decay and stop.
- Appendages passing through the body: check collisions on overshoots.

## Verify
- [ ] Tip motion lags and overshoots the base.
- [ ] Settle decays to a full stop within the shot.
- [ ] Heavier materials visibly settle faster than light ones.

Related: `creative-arts.animation.principles.offset-keys-in-the-graph-editor`,
`creative-arts.animation.principles.settles-and-recoil`.
