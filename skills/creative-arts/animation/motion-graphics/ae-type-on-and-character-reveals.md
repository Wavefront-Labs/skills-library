---
id: creative-arts.animation.motion-graphics.ae-type-on-and-character-reveals
name: ae-type-on-and-character-reveals
category: creative-arts
field: animation
product: motion-graphics
tags: [type-on, typewriter, character-reveal, text-animators, after-effects, kinetic-typography, source-text]
level: practitioner
status: draft
description: "Build type-on and per-character reveals in After Effects: opacity animator with range selector, hard reveal settings, cursor, expression-driven counts and presets."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Type-on and per-character reveals

## Method 1: opacity animator (the standard)
1. Add a text layer. Click **Animate > Opacity** and set the animator's **Opacity to 0%**.
2. In **Range Selector 1 > Advanced**, set **Shape** to **Square** and **Smoothness** to 0% for a hard on/off reveal, keep **Based On** at Characters.
3. Animate the selector **Start** from 0% to 100% (or **Offset** from -100% to 0%) over the time you want the line to type. Linear keyframes give an even speed; use irregular timing or the Wiggly selector for a human feel.
4. Switch **Based On** to Words or Lines for word-by-word or line-by-line reveals.

## Method 2: Source Text expression (counter-driven)
Add a slider and use an expression on Source Text to cut the string at a number:
```javascript
s = "Hello there, world.";
n = Math.round(effect("Slider Control")("Slider"));
s.substr(0, n)
```
This works with proportional fonts and lets you drive the count from other controls (`ae-expression-controls.md`). It does not give per-character easing.

## Typewriter cursor
- Append a cursor character: `s.substr(0, n) + (Math.floor(time*2)%2 ? "|" : " ")` for a blinking cursor (a flicker of two per second).
- Use a **monospaced** font for a convincing terminal look, and avoid kerning shifts as characters appear.

## Presets
After Effects ships text animation presets (Effects & Presets > Animation Presets > Text > Animate In), including a Typewriter preset. Apply one and inspect how it is built before modifying, as names vary by version.

## Typing rhythm
- Keystroke timing is uneven: add small random pauses on punctuation and spaces.
- Sync sound: place a click SFX per character or word (`hard-effects-cutting.md`), or make the reveal in sync with VO (`lip-sync-review-and-offset-correction.md`).

## Pitfalls
- Opacity-based reveal keeps layout stable; Source Text based reveal can reflow centred text. Set paragraph alignment to left to avoid jumping.
- Check **Based On** setting when spaces cause pauses.

## Verify
- [ ] Hard edges at 0% smoothness; no half-visible characters.
- [ ] Reveal completes exactly at the target frame.
