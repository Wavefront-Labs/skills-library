---
id: creative-arts.design-for-form-and-experience.design-systems.setting-fluid-typography-with-clamp
name: setting-fluid-typography-with-clamp
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [fluid-typography, css-clamp, clamp-typography, responsive-type, utopia-type-scale, fluid-type-scale]
level: practitioner
status: docs-checked
description: "Set fluid typography with CSS clamp: choose minimum and maximum sizes and viewports, compute the preferred value, keep rem in the formula for zoom, and test."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
  - https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fluid typography with clamp

Fluid type scales between a minimum size and a maximum with no breakpoints.

## Syntax
`font-size: clamp(MIN, PREFERRED, MAX);` clamp resolves as `max(MIN, min(PREFERRED, MAX))`. Each argument may use different units (`rem`, `px`, `vw`, `em`, `%`) and may be a math expression; put spaces around `+` and `-`. MDN's example: `font-size: clamp(1.8rem, 2.5vw, 2.8rem);`.

## Compute the preferred value
To scale linearly from size `s1` at viewport `v1` to `s2` at `v2` (all in px):
- slope = (s2 - s1) / (v2 - v1)
- intercept = s1 - slope x v1
- preferred = intercept (in rem) + (slope x 100)vw

Example, assuming a 16 px root size: 16 px at 320 px and 20 px at 1280 px gives slope 4 / 960 = 0.004167, so 0.417vw; intercept 16 - 0.004167 x 320 = 14.67 px = 0.917rem. Result: `clamp(1rem, 0.917rem + 0.417vw, 1.25rem)`.

## Rules
1. **Bound with relative units and keep the maximum at least twice the minimum.** MDN recommends this so text can still reach 200 percent when the page is zoomed, which supports WCAG 1.4.4 Resize Text (Level AA: text must resize to 200 percent without loss of content or functionality). The example above has a ratio of 1.25 and would not meet that guidance for large steps; check zoom behaviour.
2. **Beware viewport units.** WCAG failure F94 is incorrect use of viewport units to resize text; do not rely on vw alone.
3. Convention: apply fluid scales to headings first, limit line length (see `...interaction-design.setting-line-length-for-readable-ui-text`), choose the ratio with `...design-systems.choosing-a-modular-scale-ratio`, and output sizes as tokens.
4. Test at the narrowest and widest supported viewports and at 200 percent zoom.

## Verify
- [ ] Text enlarges when the user zooms.
- [ ] Sizes at the endpoints match the design.
- [ ] No heading overflows at the narrowest width.

## Checked
2026-11-01. Confirmed on MDN clamp() (semantics, units, equivalent max/min form, the twice-the-minimum zoom recommendation; first 100000 characters read) and the WCAG 2.2 Understanding Resize Text page (1.4.4, Level AA, 200 percent, F94). Corrected the worked example: the slope gives 0.417vw, not 4.17vw. Removed: Utopia generator claim, "rem in the formula" as a WCAG requirement, test viewport list, the "fluid ratio" advice.
Method: documentation only; no commands were run.
