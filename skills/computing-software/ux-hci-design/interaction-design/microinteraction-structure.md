---
id: computing-software.ux-hci-design.interaction-design.microinteraction-structure
name: microinteraction-structure
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [microinteractions, trigger-rules-feedback, id-feedback-microinteractions]
level: practitioner
status: draft
description: "Structure small interactions with trigger, rules, feedback and loops and modes, in line with Dan Saffer's model."
sources:
  - https://www.nngroup.com/articles/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Saffer's four parts
1. **Trigger**: user (tap, toggle) or system (a threshold).
2. **Rules**: what happens, in what order.
3. **Feedback**: visual, audio, haptic confirmation of the rules.
4. **Loops and modes**: how long it lasts, whether it repeats, what changes over time.
Examples: pull to refresh, like button, toggle switch, typing indicator.

## Practice
Keep durations short (commonly 100-300 ms for UI transitions; Material specifies ranges in its motion docs), keep it purposeful, respect reduced-motion preferences.

## Verify
- [ ] Microinteraction can be removed without losing needed information.
