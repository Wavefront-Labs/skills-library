---
id: creative-arts.animation.motion-graphics.range-and-wiggly-selectors
name: range-and-wiggly-selectors
category: creative-arts
field: animation
product: motion-graphics
tags: [range-selector, wiggly-selector, text-animators, after-effects, selectors, expression-selector, kinetic-typography]
level: practitioner
status: draft
description: "Drive text animators with range and wiggly selectors in After Effects: Start, End, Offset, shapes, smoothness, randomness controls and when to use which."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Range and wiggly selectors (After Effects)

Selectors decide **how much** each character is affected by a text animator (`ae-text-animators.md`).

## Range selector
- **Start** and **End** (0-100% by default) define the selected range; the **Offset** slides the range along the text.
- Animate **Offset** from -100% to 100% to sweep the effect across the line. Animate **Start** from 0 to 100% for a progressive reveal.
- **Units** can be Percentage or Index (character number), and **Based On** chooses characters, words or lines.
- **Shape** controls the falloff: Square (hard edges), Ramp Up, Ramp Down, Triangle, Round, Smooth. **Ease High/Low** reshapes the curve; **Smoothness** blends neighbouring characters for Square.
- **Randomize Order** with a **Random Seed** shuffles which characters change first.

## Wiggly selector
- Add from the animator's Add button: **Selector > Wiggly**.
- It adds randomised variation to the selection amount over time: **Max Amount** and **Min Amount**, **Wiggles/Second**, **Correlation** (0 = each character independent, 100% = all together), **Temporal Phase** and **Spatial Phase**, **Lock Dimensions**, **Random Seed**.
- Use with Position, Rotation or Scale for jittery, alive text; with Opacity for flicker.
- A **Mode** of Add, Intersect or others decides how it combines with the range selector.

## Choosing
- **Range**: controlled, sweeping reveals and wave effects.
- **Wiggly**: organic noise and jitter.
- **Expression selector**: use an expression for per-character logic (`textIndex`, `textTotal`, `selectorValue`) when ranges are not enough.

## Practice
1. Set the animator's property to the "full effect" value, then use selectors to control where it applies.
2. Offset keyframes with Easy Ease for smooth sweeps.
3. Randomise sparingly: seeds change the result, so lock a seed that looks good.

## Verify
- [ ] Sweep reaches 0% and 100% at the intended times.
- [ ] Wiggly randomness is stable on re-render (seed locked).
