---
id: computing-software.web-development.web-accessibility.concurrent-input-mechanisms
name: concurrent-input-mechanisms
category: computing-software
field: web-development
product: web-accessibility
tags: [concurrent-input-mechanisms, wcag-2-5-6, input-modalities, pointer-events, any-pointer]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.5.6 Concurrent Input Mechanisms: never locking users to touch or mouse, avoiding UA sniffing for input type, pointer events for all modalities and hybrid devices."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/concurrent-input-mechanisms.html
  - https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/any-pointer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrent input mechanisms (2.5.6)

2.5.6 (AAA in 2.1, still AAA in 2.2): content does not restrict use of input modalities available on a platform, except where essential or for security. People switch between input mechanisms such as keyboard, mouse, stylus and touchscreen mid-task (the Understanding page gives phones and tablets paired with an external keyboard or mouse as examples).

## 1. Failures to avoid
- Detecting "touch device" once (`'ontouchstart' in window`, user agent) and then ignoring mouse or keyboard events.
- Listening only to `touchstart`/`touchend`, so mouse and stylus users on the same laptop can't operate a control.
- Calling `preventDefault()` on touch events in ways that block keyboard or switch access.
- Hiding focus outlines once a touch event is seen.
- Showing a "please use a mouse" or "tap only" restriction.

## 2. Do this instead
```js
el.addEventListener("pointerdown", onDown);   // one model for mouse, touch, pen
el.addEventListener("click", activate);       // fires for keyboard Enter/Space on buttons too
// Branch per event, not per device:
function onDown(e) { if (e.pointerType === "touch") { /* larger slop for drag */ } }
```
- Pointer Events unify mouse/touch/pen; `click` covers keyboard and assistive tech activation.
- Use `:focus-visible` to decide when to show focus rings - the browser handles modality switching.
- CSS: `@media (any-pointer: coarse)` asks "is there any coarse pointer available" (better for sizing targets on hybrids) whereas `pointer` reports only the primary.
- Don't remove hover behaviour on touch-capable devices that also have a mouse; use `@media (hover: hover)` per interaction rather than one global flag.

## 3. Security exception
Restricting input is allowed for security (e.g. requiring a hardware key gesture), and where essential (signature capture may require a pointer, but provide an alternative such as typed name).

## 4. Testing
- A touch laptop or a tablet with keyboard and trackpad: complete key flows while switching input mode mid-task.
- DevTools device emulation toggles touch but keeps the mouse - useful for catching "touch only" code.

## Verify
- [ ] No code path disables mouse, keyboard or stylus after detecting touch; flows completable with any input and when switching mid-flow.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.5.6 Concurrent Input Mechanisms (Level AAA): content must not restrict use of the platform's input modalities except where essential, required for security, or required to respect user settings; the Understanding page confirms the paired-keyboard example. MDN confirms the any-pointer and hover media features, :focus-visible, and pointerType values. Removed the unconfirmed Windows/iPad product claims.

Method: documentation only; no commands were run.
