---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-microinteraction-feedback
name: designing-microinteraction-feedback
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [microinteraction-feedback, interaction-feedback, feedback-design, micro-interactions, visual-audio-haptic-feedback, saffer-microinteractions]
level: practitioner
status: draft
description: "Design microinteraction feedback: show state change and result with visual, audio and haptic cues sized to importance, timed to the action and accessible."
sources:
  - "Dan Saffer, Microinteractions: Designing with Details (O'Reilly, 2013)"
  - "Don Norman, The Design of Everyday Things (revised 2013)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microinteraction feedback

Feedback makes the rules visible: it tells people that something happened and what state they are in. Norman lists feedback among the fundamental principles of interaction.

## Principles
- **Respond immediately** to every action; slow responses need a progress cue (see `...interaction-design.designing-to-response-time-limits`).
- **Match the size of feedback to the importance** of the event: a subtle colour shift for a hover, a stronger animation for a completed purchase.
- **Show state change, not decoration:** the feedback should answer "did it work?" and "what is the state now?"
- **Use more than one channel** where appropriate: visual, audio, and haptic; never rely on colour or sound alone (see `...interaction-design.designing-for-colour-vision-deficiency`).
- **Keep it consistent** so users learn the vocabulary (same success animation across the product).
- **Be brief and non-blocking;** do not make users wait for animations.
- **Respect preferences:** offer sound off and reduced motion (see `...interaction-design.designing-reduced-motion-alternatives`).

## Examples
Button press: pressed state within a frame or two; toggle: thumb slides and label updates; send: item appears in the list and a quiet confirmation; error: field highlight, message and focus.

## Verify
- [ ] Every trigger has visible feedback within the response-time limit.
- [ ] Feedback does not depend on one sense.
- [ ] Animations can be disabled or reduced.
