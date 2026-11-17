---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-loops-and-modes
name: designing-loops-and-modes
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [loops-and-modes, microinteraction-loops, modes-in-ui, long-loops, micro-interactions, saffer-microinteractions]
level: practitioner
status: draft
description: "Design microinteraction loops and modes: repeat or adapt over time, handle first-run versus experienced use, and avoid mode errors with clear mode indication."
sources:
  - "Dan Saffer, Microinteractions: Designing with Details (O'Reilly, 2013)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Loops and modes

The fourth part of a microinteraction in Saffer's model deals with what happens over time (loops) and with alternative states of operation (modes).

## Loops
- A **loop** repeats or changes the microinteraction over time: a progress indicator that repeats, a reminder that returns weekly, a tip that disappears after use.
- **Ask:** how long does it last, how often does it recur, and should it change with use (fade out hints, shorten confirmations for experienced users)?
- **Long loops** (days or weeks) need a way to stop and a limit on frequency so that they do not become nagging.
- **Adapt to the user:** first-run guidance, then less; remember settings.

## Modes
- A **mode** makes the same input do something different (caps lock, edit vs view, silent mode). Modes can cause errors when users forget the current mode.
- **Avoid modes** if possible; if needed, make the mode visible (label, colour, cursor), keep it short-lived (a spring-loaded mode that ends when released), and make the switch easy.
- Provide an escape route (Cancel, Esc) and avoid modal blocking when a non-modal alternative works.

## Verify
- [ ] Repeating events have limits and can be turned off.
- [ ] Every mode is visible and easy to leave.
- [ ] First-time and experienced paths have been tested separately.
