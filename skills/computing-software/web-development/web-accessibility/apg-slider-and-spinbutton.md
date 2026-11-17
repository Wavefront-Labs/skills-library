---
id: computing-software.web-development.web-accessibility.apg-slider-and-spinbutton
name: apg-slider-and-spinbutton
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-slider, aria-spinbutton, range-input, aria-valuetext, keyboard-navigation]
level: practitioner
status: docs-checked
description: "Accessible sliders and spinbuttons: native range and number inputs first, then role=slider/spinbutton with aria-valuenow/valuetext, keyboard steps, multi-thumb ranges and touch."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/slider/
  - https://www.w3.org/WAI/ARIA/apg/patterns/slider-multithumb/
  - https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/range
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slider and spinbutton patterns

## 1. Prefer native
```html
<label for="vol">Volume</label>
<input id="vol" type="range" min="0" max="100" step="5" value="40" aria-valuetext="40 percent">
```
Native range inputs get keyboard and screen-reader support for free. A spinbutton is just `<input type="number">` (or `inputmode="numeric"` text with +/- buttons for better UX).

## 2. Custom slider
```html
<div class="track"><div role="slider" tabindex="0" aria-labelledby="price-label"
     aria-valuemin="0" aria-valuemax="500" aria-valuenow="120" aria-valuetext="$120"
     aria-orientation="horizontal"></div></div>
```
Keyboard:
| Key | Change |
|---|---|
| Right/Up | +1 step |
| Left/Down | -1 step |
| Page Up/Down (optional) | larger step than the arrow keys |
| Home/End | first / last allowed value |

- Update `aria-valuenow` and `aria-valuetext` (human-readable: "$120", "Tuesday", "Medium") on every change.
- Pointer: `pointerdown` on the track jumps and starts a drag with `setPointerCapture`; WCAG 2.5.8 (Target Size Minimum, AA) asks for targets of at least 24x24 CSS px unless an exception applies; dragging needs a single-pointer alternative (2.5.7, AA), such as tapping the track or +/- buttons.
- Vertical sliders: `aria-orientation="vertical"` (default is horizontal); Up Arrow still increases unless reversing the direction is clearly more intuitive.

## 3. Multi-thumb (range) slider
Two `role="slider"` elements, each labelled ("Minimum price", "Maximum price"); each thumb's `aria-valuemin/max` constrained by the other's value; Tab moves between thumbs (see the APG multi-thumb slider). Often better UX: two number inputs plus a visual slider.

## 4. Spinbutton
`role="spinbutton"` with `aria-valuenow/min/max/text`; Up/Down Arrow step, optional Page Up/Down larger step, Home/End to minimum/maximum when defined, typing a value allowed. Increment/decrement buttons are typically excluded from the Tab sequence (`tabindex="-1"`) and labelled, since the keys already work on the field.

## 5. Mobile screen readers
Test custom sliders with the mobile screen readers you support; prefer the native range input.

## Verify
- [ ] Keyboard table works; value announced in meaningful units; usable by touch without precise drag; native input used unless a design requirement truly needs custom.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG slider and spinbutton patterns: Right/Up and Left/Down by one step, Home/End, optional Page Up/Down, aria-orientation default horizontal, aria-valuetext for non-friendly values, spinbutton Home/End only when min/max exist. WCAG 2.5.7 and 2.5.8 are Level AA in WCAG 2.2. Removed unconfirmed vendor pseudo-element styling and VoiceOver adjustable behaviour claims.

Method: documentation only; no commands were run.
