---
id: creative-arts.animation.blender.character-interaction
name: character-interaction
category: creative-arts
field: animation
product: blender
tags: [blender, character-animation, character-interaction, prop-interaction, contact, two-character, prop-handoff]
level: practitioner
status: docs-checked
description: "Animate character-prop and character-character contact in Blender: lead/follow choice, Child Of and Armature constraint parent switching, contact checks."
sources:
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/child_of.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/armature.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# character-interaction

Goal: hands that stay locked on props and on another character (handshakes, lifts, fights) without sliding or interpenetration.

## Decide who leads

For each contact section, one element *drives* and the other *follows*: the prop is held, so the prop follows the hand; a hand pushes a table, so the hand IK follows the table; a partner leads a dance, so the follower's hand IK is constrained to the leader's hand.

## Techniques

- **Child Of constraint**: transforms an object or bone as though it were a child of another object or bone. Its advantage over normal parenting is an animatable *Influence*, so you can switch parents over time (key influence 0 to 1 on one Child Of while keying the previous parent's down). Setting several Child Of constraints with partial influences gives a weighted average of parents.
- **Set Inverse**: if the child's transform is right with the constraint disabled but wrong with it enabled, press *Set Inverse*. *Clear Inverse* tells the constraint the child's current transform (constraint disabled) is its correct relative transform, applied as an offset to the parent. Set the inverse at the contact frame so the prop or hand does not jump.
- **Location / Rotation / Scale toggles** on the constraint choose which axes of the child are affected.
- **Child Of is a poor fit for bone chains**: it cannot emulate connected bones. When the parents are bones and you want weighted blends, the manual recommends the *Armature* constraint.
- **Armature constraint**: transforms the owner (object or bone) from the weighted pose of one or more target bones; each bone entry has a *Weight*, *Normalize Weights* makes them sum to 1.0, and, unlike the Armature modifier, it can use bones from different armatures (so a prop can blend between two characters' hands) and bones with Deform disabled. *Preserve Volume* stops shrinking when targets rotate relative to each other. It does not auto-detect nearby bones when envelopes are used: add each bone manually.
- **Prop in hand**: prop Child Of the hand bone with keyed influence, or Armature constraint weights, plus a `prop_offset` control under the prop for fine adjustment (see `child-of-dynamic-parenting` and `armature-constraint`).
- **Hand on another character**: the hand IK control gets a Child Of targeting the partner's bone, influence keyed on during contact.
- **Two-handed props**: the prop follows the dominant hand; the other hand's IK is Child Of a socket bone or empty on the prop.

## Checks

- Interpenetration: side views at contact frames.
- Weight transfer: the lifter's centre of gravity lowers and shifts before contact; the lifted character's timing lags.

## Gotchas

- Child Of on bones is not suited to chains of connected bones (see above); use Armature constraint weights when blending bone parents.

## Verify

Scrub through contact frames in camera and side views: zero slide at contact points and no visible penetration.

## Checked

2026-11-09. Confirmed against the Blender manual Child Of and Armature constraint pages (raw RST, both read in full): animatable Influence and weighted parents, Set Inverse / Clear Inverse behaviour, axis toggles, bone-chain limitation, the Armature constraint's weights, Normalize Weights, Preserve Volume, multi-armature targets and non-Deform bones. Removed: Constant-key and motion-path contact locking, X-ray and Mask modifier checks, library override advice and the Bake Action / Visual Keying export step (not on the pages). Also removed the circular-evaluation and engine-export gotchas.
Method: documentation only; no commands were run.
