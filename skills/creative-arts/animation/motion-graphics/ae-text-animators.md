---
id: creative-arts.animation.motion-graphics.ae-text-animators
name: ae-text-animators
category: creative-arts
field: animation
product: motion-graphics
tags: [text-animator, text-animators, animator-groups, after-effects, kinetic-typography, per-character, text-layers]
level: practitioner
status: draft
description: "Animate text per character, word or line with After Effects text animators: animator properties, selector basics, multiple animators and common pitfalls."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Text animators (After Effects)

A **text animator** lets you change properties of selected characters, words or lines, and animate which text is selected. It is the standard route to kinetic typography.

## Adding one
1. Select the text layer, open it in the Timeline, and click **Animate** next to the layer's Text group.
2. Pick a property: Position, Scale, Rotation, Skew, Anchor Point, Opacity, Fill Color, Stroke Color and Width, Tracking, Line Anchor, Line Spacing, Character Offset, Character Value, Blur, and 3D equivalents.
3. The new **Animator 1** contains the property you chose plus a **Range Selector 1**. Set the property value to the change you want applied to selected text, for example Position Y = 50 px.
4. Animate the selector (`range-and-wiggly-selectors.md`) so the change sweeps across the text.

## Key settings (Range Selector > Advanced)
- **Based On**: Characters, Characters Excluding Spaces, Words, Lines.
- **Mode**: Add, Subtract, Intersect, Min, Max, Difference (how multiple selectors combine).
- **Amount**: how strongly the animator applies (0-100%).
- **Shape**, **Smoothness**, **Ease High/Low**: how the effect fades across the selection.
- **Randomize Order** and **Random Seed**.

## Combining
- One text layer can have several animators, each with its own selectors and properties; animate them independently.
- Set Anchor Point Grouping (More Options) to **Word** or **Line** so scaling and rotation pivot around each word or line rather than each character.
- Use **Tracking** with **Tracking Amount** for expanding or collapsing letter-spacing.

## Tips
- Animator properties are relative offsets; the base Source Text, font and size stay in the Text group.
- Use presets (Effects & Presets > Animation Presets > Text) to learn how professional animators are built, then inspect and modify.
- For performance, avoid animating Blur and 3D properties on very long text.

## Verify
- [ ] Animator and selector names are clear in the timeline.
- [ ] Selected range produces the intended per-character timing.
