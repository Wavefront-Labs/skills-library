---
id: computing-software.web-development.web-accessibility.pointer-gestures-single-pointer-alternatives
name: pointer-gestures-single-pointer-alternatives
category: computing-software
field: web-development
product: web-accessibility
tags: [input-modalities, pointer-accessibility, pointer-gestures, wcag-2-5-1, multipoint-gestures, path-based-gestures, swipe-alternatives, pinch-zoom]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.5.1 Pointer Gestures: providing single-tap alternatives for swipes, pinches and multi-finger or path-based gestures in maps, carousels and sliders."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G215
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pointer gestures: single-pointer alternatives

**Goal:** everything done with a multi-finger or path-based gesture can also be done with a single tap/click (users with tremors, head pointers, mouth sticks, switch access).

## 1. What counts
- **Multipoint**: pinch-zoom, two-finger rotate/pan.
- **Path-based**: swipe, drag along a path, drawing a shape (the route matters, not just endpoints).
2.5.1 (A) requires that functionality using multipoint or path-based gestures can be operated with a single pointer without a path-based gesture, unless the gesture is essential (signature capture, drawing app).

## 2. Common fixes
| Gesture | Alternative |
|---|---|
| Swipe carousel | Previous/Next buttons, dot buttons |
| Pinch-zoom on a map/image | +/- zoom buttons |
| Swipe-to-delete in a list | Visible Delete button or a menu |
| Pull-to-refresh | Refresh button |
| Two-finger map pan | Single-finger drag is fine (that's a dragging movement - also see 2.5.7) or arrow buttons |
| Slider drag | Click on track / +/- buttons / keyboard arrows |

## 3. Implementation notes
- Keep the browser's own pinch-zoom working; users rely on it.
- Pointer Events (`pointerdown/move/up`) unify mouse, touch and pen; feature-detect multi-touch only for enhancement.
- Buttons must meet target size (24x24 CSS px minimum, 2.5.8) and be keyboard operable (2.1.1).

## 4. Library check
If a carousel, map or gallery library offers buttons, make sure they are enabled and labelled ("Zoom in", "Next slide").

## Verify
- [ ] Every gesture-driven function reachable with single clicks only (test with a mouse, no drag, no wheel).
- [ ] Same functions work by keyboard.
- [ ] Page still zooms with pinch on mobile.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.5.1 Pointer Gestures (Level A) and 2.5.8 Target Size (Minimum) (24 by 24 CSS px, Level AA). Removed the touch-action, user-scalable and library-name claims.

Method: documentation only; no commands were run.
