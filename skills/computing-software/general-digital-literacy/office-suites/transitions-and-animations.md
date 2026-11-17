---
id: computing-software.general-digital-literacy.office-suites.transitions-and-animations
name: transitions-and-animations
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slideshow, transitions-and-animations, morph, animation-pane, appear-on-click, build-bullets]
level: intro
status: docs-checked
description: "Add slide transitions and object animations (including build-in bullets and Morph), control order and timing in the Animation Pane, and keep motion restrained."
sources:
  - https://support.microsoft.com/en-us/powerpoint/training/add-change-or-remove-transitions-between-slides
  - https://support.microsoft.com/en-us/powerpoint/training/animate-text-or-objects
  - https://support.microsoft.com/en-us/powerpoint/training/use-the-morph-transition-in-powerpoint
  - https://support.microsoft.com/en-us/powerpoint/save-a-slide-as-an-image-or-as-a-separate-presentation-file
  - https://support.google.com/docs/answer/1689475
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/00/00000407.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/animated_objects.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transitions and animations

**Goal:** motion that helps the audience follow, not distracts.

## Transitions (between slides)
- PowerPoint: select the slide › **Transitions** tab › pick a transition (it plays as this slide arrives),
  Effect Options, Timing group for duration and advance, *Apply To All*. **Morph** animates objects that appear
  on consecutive slides (duplicate a slide, move/resize things on the copy, apply Morph to the second).
- Google Slides: Slide › **Transition** › choose from the drop-down; drag the slider for speed.
- Impress: Slide Show › **Slide Transition** (opens the Slide Transition deck).

## Animations (objects within a slide)
- PowerPoint: select an object › **Animations** tab › an entrance, emphasis, exit or motion-path effect;
  Effect Options to change how it runs (for example bullets one at a time).
- **Animation Pane** lists the order; drag to reorder; set Start *On Click* / *With Previous* /
  *After Previous*, plus Duration and Delay. **Add Animation** stacks more effects on one object.
- Google Slides: Insert › **Animation** (or View › Motion); new animations default to Appear (On click); tick
  "By paragraph" to reveal list lines one at a time.
- Impress: View › **Animation** (Custom Animation pane in the sidebar) › Add (+).

## Good practice
- One or two styles for the whole deck; simple fades and appears are usually enough.
- Reveal points as you talk about them; avoid flying, spinning, bouncing text.
- Morph or appear-to-highlight works well for building a diagram step by step.

## Gotchas
- Slides saved as images lose transitions and animations, so all objects appear at once.
- Too many clicks per slide makes it easy to lose your place; check the count in the pane.
- Some animations may not work when a Google Slides deck is viewed in some browsers.
- Avoid flashing effects.

## Verify
- [ ] Run the slideshow from the start: each click reveals what you expect, in order.

## Checked
2026-10-27, against Microsoft Support (Add, change or remove transitions; Animate text or objects; Morph; save slides as images; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (Add or change animations and transitions) and the LibreOffice help master branch (Impress Slide Show menu; animating objects). Confirmed: Transitions tab, Effect Options, Timing and Apply To All, Morph setup, animation categories, Start/Duration/Delay, Animation Pane reordering and Add Animation, Google Slide › Transition, Insert › Animation, default Appear (On click) and By paragraph, and Impress Slide Transition and Animation paths. Corrected the Impress transition path (Slide Show menu, not Slide menu) and removed an unconfirmed flash-rate figure.
Method: documentation only; no commands were run.
