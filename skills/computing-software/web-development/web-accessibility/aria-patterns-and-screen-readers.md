---
id: computing-software.web-development.web-accessibility.aria-patterns-and-screen-readers
name: aria-patterns-and-screen-readers
category: computing-software
field: web-development
product: web-accessibility
tags: [aria, screen-reader, nvda, voiceover, live-region, aria-label, roles, custom-widgets, accessibility, web-development]
level: advanced
status: docs-checked
description: "ARIA for custom widgets: the 'no ARIA is better than bad ARIA' rule, live regions for dynamic content, and testing with an actual screen reader."
sources:
  - https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  - https://www.w3.org/TR/using-aria/
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARIA patterns and screen readers — only when native HTML can't do it

**Goal:** a custom widget (dropdown, tabs, modal) that a screen reader user can
operate with the same confidence as a sighted mouse user — without ARIA attributes
that lie about what the element actually does.

## 1. First rule of ARIA: don't, if you can avoid it
The first rule of ARIA use (W3C Using ARIA note): if a native HTML element or attribute has
the semantics/behaviour you need, use it instead of recreating it with a `div` and
ARIA. `<button>` is focusable, keyboard-activatable (Enter/Space), and announced
as "button" with zero ARIA. A `<div role="button">` gets you the announced role
only — you must manually add `tabindex="0"`, handle `keydown` for Enter and Space,
and manage focus styles yourself. Every one of those is a place to get it wrong;
native elements get it right for free.

## 2. ARIA changes what's announced, never what's visible or functional
`role`, `aria-label`, `aria-describedby` etc. only affect the accessibility tree
(what assistive tech reads) — they don't add keyboard behaviour, don't change
focusability, don't change visual rendering. Setting `role="button"` on a `<div>`
without also adding keyboard handling produces an element a screen reader
announces as a button that a keyboard user still can't activate — this is "bad
ARIA," and the APG states that no ARIA is better than bad ARIA.

## 3. Live regions — announcing dynamic content changes
```html
<div aria-live="polite" aria-atomic="true">3 items added to cart</div>
<div role="alert">Payment failed — check your card number</div>  <!-- assertive, implicit -->
```
- `aria-live="polite"`: announced when the screen reader is next idle — for
  non-urgent updates (search result counts, "saved" confirmations).
- `aria-live="assertive"` / `role="alert"`: interrupts immediately — reserve for
  genuinely urgent things (errors, session timeout warnings); overusing it is
  disorienting, like a sighted user getting a modal for every minor update.
- The region must exist in the DOM *before* the content changes — injecting a
  brand-new `aria-live` element with its final text already in it is often not
  announced, because there's no "live" region yet to observe the mutation. Render
  the empty container first, then update its text content.

## 4. Common custom-widget patterns (follow the APG, don't invent your own)
The WAI-ARIA Authoring Practices Guide (APG) has a reference implementation per
widget type (combobox, tabs, menu, dialog, accordion) with the exact roles,
states, and keyboard interactions expected — copy the pattern rather than
guessing at `aria-expanded`/`aria-controls`/`aria-activedescendant` combinations.
A modal dialog specifically needs: `role="dialog"` + `aria-modal="true"`, focus
moved into it on open, focus trapped inside while open (Tab cycles within, not
out to the page behind), and focus returned to the trigger element on close —
missing any one of these is a frequent audit finding.

## 5. Testing with an actual screen reader, not just an automated scanner
Automated tools (axe, Lighthouse) catch missing labels and contrast — they
cannot tell you whether a custom widget's *interaction* makes sense when heard,
only sighted. Test manually with NVDA (Windows) or VoiceOver (macOS)
navigating by keyboard only: Tab order should match visual order, every
interactive element should announce its role and state ("button, collapsed"),
and nothing should trap focus unexpectedly. If you can't operate your own
feature with the screen reader and no mouse, a screen reader user can't either.

## Verify
- [ ] Every custom interactive `div`/`span` has a native-element alternative ruled out first.
- [ ] Any `role` added to a non-native element is paired with matching keyboard behaviour and focus management.
- [ ] Live regions exist empty in the DOM before their content is first updated.
- [ ] Modal/dialog patterns trap focus while open and return it to the trigger on close.
- [ ] The feature has been operated end-to-end with a real screen reader and keyboard only, not just an automated scan.

## Checked

- Date: 2026-10-26. Documentation: ARIA APG (read-me-first, modal dialog pattern), W3C Using ARIA (a discontinued draft kept for reference), WAI-ARIA 1.2, MDN live regions.
- Confirmed: first rule of ARIA use; "No ARIA is better than Bad ARIA"; `role="alert"` has an implicit `aria-live="assertive"`; the live region should exist (empty) before its content changes; a modal dialog sets `aria-modal="true"`, moves focus in, contains Tab and returns focus to the invoking element on close; Escape closes it.
- Removed (no documentation found): the NVDA "free" label and the VoiceOver key shortcut.
Method: documentation only; no commands were run.