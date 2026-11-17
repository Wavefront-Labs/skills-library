---
id: creative-arts.design-for-form-and-experience.figma.prototype-triggers-actions-and-flows
name: prototype-triggers-actions-and-flows
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [prototype-triggers, prototype-flows, figma-prototyping, prototype-actions, interactions, flow-starting-points, figma]
level: practitioner
status: docs-checked
description: "Wire Figma prototypes: choose triggers (click, drag, hover, key, delay), actions (navigate, change to, open overlay, back, set variable), and define flow starting points."
sources:
  - https://help.figma.com/hc/en-us/articles/360040035834-Prototype-triggers-and-actions
  - https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype triggers, actions and flows

Each interaction pairs a trigger with an action.

## Triggers
- **On click / On tap**, **On drag** (any direction), **While hovering** (returns to the original frame when the cursor leaves), **While pressing** (returns on release).
- **Keyboard/Gamepad:** a key, key combination or controller button.
- **Mouse enter**, **Mouse leave**, **Mouse down (touch down)**, **Mouse up (touch up)**. Older "Mouse move inside/outside" interactions can no longer be created.
- **After delay:** fires after a set time on a frame, in milliseconds.
- **When video hits** a timestamp, **When video ends**.

## Actions
- **Navigate to** a frame, **Back** to the previous screen, **Open link** (new tab, with a warning before leaving Figma), **Scroll to** an object.
- **Change to** switches variants in a component set.
- **Open overlay**, **Close overlay**, **Swap overlay** (swapped frames are not added to history).
- **Set variable**, **Set variable mode**, **Conditional** (if/else) (see `creative-arts.design-for-form-and-experience.figma.conditional-logic-in-prototypes`).
- Video actions: play/pause, mute/unmute, set to a time, jump forward or back.
- Multiple interactions per layer allow combined behaviours (hover and click). For animation between frames see `creative-arts.design-for-form-and-experience.figma.smart-animate-in-figma-prototypes`.

## Flows
Define a named flow starting point for each user journey (for example Onboarding, Checkout) and test each path from its start. Look up the current steps in the Figma Help Center article on flows and starting points.

## Interactive components
Put hover and pressed behaviour in component variants with Change to, so every instance behaves consistently (`creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants`).

## Gotchas
- Dangling connections lead to dead ends in tests.
- Long chains of frames become unmaintainable; reuse overlays and component states.

## Verify
- [ ] Every task path exists from a named flow starting point.
- [ ] Actions and animations chosen deliberately.
- [ ] Prototype tested on the target device.

## Checked
2026-11-01. Confirmed on the Figma Help Center pages Prototype triggers and actions, and Prototype actions: the trigger and action names and behaviours above. Removed: animation type list, durations and easing, flow-start button steps, Present shortcut, Mirror and Maze, link access and password claims, hotspot hint setting, which no page read stated.
Method: documentation only; no commands were run.
