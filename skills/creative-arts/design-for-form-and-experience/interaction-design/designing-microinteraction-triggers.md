---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-microinteraction-triggers
name: designing-microinteraction-triggers
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [microinteraction-triggers, triggers, manual-triggers, system-triggers, micro-interactions, saffer-microinteractions]
level: practitioner
status: draft
description: "Design microinteraction triggers: choose manual or system-initiated, make controls discoverable, set clear affordance and state, and avoid unwanted activation."
sources:
  - "Dan Saffer, Microinteractions: Designing with Details (O'Reilly, 2013)"
  - "Interaction Design Foundation literature (interaction-design.org/literature)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microinteraction triggers

In Dan Saffer's model a microinteraction has four parts: trigger, rules, feedback, and loops and modes. The trigger starts it.

## Types
- **Manual triggers:** the user starts it with a control: a button, toggle, swipe, long-press, voice command, gesture, or a keyboard shortcut.
- **System-initiated triggers:** the system starts it when a condition is met: a threshold crossed (battery low), a time (reminder), an event (message arrived), a location or sensor input.

## Design manual triggers
1. **Make them discoverable:** visible affordance and a label or icon the user recognises; a gesture-only trigger needs a visible alternative or a hint.
2. **Place it where the need arises** (near the content it acts on) and use platform conventions.
3. **Show the state** the trigger is in (on or off, available or disabled) before it is used.
4. **Size and reach:** follow touch target guidance (see `...interaction-design.sizing-touch-targets`).
5. **Make it fast to reach** for frequent actions; a rare action can be one level deeper.
6. **Prevent accidental activation:** spacing, confirmation or undo for risky ones (see `...interaction-design.choosing-undo-over-confirmation`).

## Design system-initiated triggers
- Ask whether the system should interrupt at all; the cost of interruption vs benefit.
- Use thresholds with hysteresis so the trigger does not flap.
- Give the user control: dismiss, snooze, settings.

## Verify
- [ ] A new user can find and understand each trigger without instruction.
- [ ] State is visible before and after use.
- [ ] System-initiated triggers can be controlled or turned off.
