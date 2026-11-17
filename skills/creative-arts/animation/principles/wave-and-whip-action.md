---
id: creative-arts.animation.principles.wave-and-whip-action
name: wave-and-whip-action
category: creative-arts
field: animation
product: principles
tags: [animation, follow-through-overlap, wave-principle, whip-action, flexibility, s-curve, figure-eight, overlap, tails, flags]
level: advanced
status: draft
description: "Animate the wave principle (a curve travelling down a flexible form) and the whip (a wave that accelerates to a snap at the tip) for tails, flags, arms and tentacles."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wave and whip action

Goal: animate flexible forms with a travelling wave, and turn that wave into a whip snap
where needed. Williams treats both as extensions of flexibility and overlap.

## The wave principle
A shape bends, and the bend travels from root to tip. At any frame the form is an S or C
curve; frame by frame, the curve's peak moves down the length.
- Root changes direction first, the bend propagates outward, the tip changes direction last.
- The tip draws a figure-of-eight over a full cycle.
- Flags, tails, seaweed, a swimming fish body, a spine in a slinky walk all follow this.

## The whip
A wave that **accelerates** as it travels, because the mass gets smaller toward the tip. The tip
reaches a peak speed and snaps (a crack), then recoils.
- Root does a sharp, short move; the wave travels faster each segment.
- Spacing at the tip goes very wide in 1-2 frames (often a smear frame).
- Used for whips, wet-towel flicks, a character's arm in a hard throw, a tail lash.

## Method (chain or drawn form)
1. Animate the root as a simple back-and-forth (or single snap for a whip).
2. Each segment copies the parent's rotation curve shifted later in time (1-2 frames per segment
   for a wave; decreasing offsets toward the tip for a whip, so the wave speeds up).
3. Increase amplitude toward the tip.
4. For the whip, add one smear or stretch frame at the crack, then a quick recoil and settle.

## Failure modes
- Whole form rotating as one piece (a stick).
- Constant offsets making a whip look like a lazy wave.
- Tip motion jittering because offsets are not smooth along the chain.

## Verify
- [ ] At every frame the form is a smooth C or S, no kinks.
- [ ] Tip traces a figure-of-eight on cycles.
- [ ] On a whip, the tip's spacing is largest at the crack frame.

Related: `creative-arts.animation.principles.successive-breaking-of-joints`,
`creative-arts.animation.principles.appendage-overlap`.
