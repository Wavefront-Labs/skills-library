---
id: computing-software.web-development.web-accessibility.wcag-audit-and-fixes
name: wcag-audit-and-fixes
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility, a11y, wcag, wcag-2-2, wcag-aa, colour-contrast, color-contrast, target-size, focus-visible, focus-not-obscured, keyboard-navigation, semantic-html, aria, accessible-name, labels, alt-text, landmarks, headings, screen-reader, nvda, voiceover, jaws, talkback, axe, axe-core, lighthouse, wave, accessibility-audit, eaa, section-508, en-301-549, web-development, axe-devtools]
level: practitioner
status: docs-checked
description: "Auditing and fixing a site against WCAG 2.2 AA: contrast, target size, focus, semantic HTML, ARIA rules, labels, keyboard and screen-reader testing, limits of axe/Lighthouse."
sources:
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/WCAG22/quickref/
  - https://www.w3.org/WAI/ARIA/apg/
  - https://github.com/dequelabs/axe-core
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WCAG audit and fixes — automated scan, then keyboard, then screen reader

**Goal:** find and fix the barriers that block real users, documented against WCAG 2.2
Level AA (the level most laws and contracts reference; check which standard and level
your jurisdiction or contract names).

## 1. Audit in this order
1. **Automated scan** — axe DevTools browser extension or `@axe-core/playwright` in CI; Lighthouse's accessibility score uses a subset of axe. Treat these as a floor: automated tools catch only a part of WCAG issues, so a score of 100 does not mean accessible.
2. **Keyboard pass** — unplug the mouse (section 4).
3. **Screen reader pass** — at least one desktop and one mobile pairing (section 5).
4. **Zoom and reflow** — 200% text zoom and a 320 CSS px wide viewport.
5. Log each issue: URL, element, WCAG criterion, impact, fix.

## 2. Key AA criteria with numbers
| Criterion | Requirement |
|---|---|
| 1.4.3 Contrast (Minimum) | Text 4.5:1; large text (≥ 24px, or ≥ 18.66px bold) 3:1 |
| 1.4.11 Non-text Contrast | UI component boundaries, focus indicators, meaningful icons 3:1 against adjacent colours |
| 2.5.8 Target Size (Minimum) — new in 2.2 | Pointer targets ≥ 24×24 CSS px, or enough spacing that a 24px circle on each doesn't overlap another (inline text links exempt) |
| 2.4.7 Focus Visible | Keyboard focus indicator always visible |
| 2.4.11 Focus Not Obscured (Minimum) — new | Focused element not entirely hidden by sticky headers, cookie banners, chat widgets |
| 1.4.10 Reflow | Usable at 320 CSS px wide without 2-D scrolling |
| 1.4.4 Resize Text | Readable and functional at 200% |
| 2.1.1 / 2.1.2 | Everything works by keyboard; no keyboard traps |
| 1.1.1 Non-text Content | Informative images have alt text; decorative ones `alt=""` |
| 1.3.1 / 4.1.2 | Structure and name/role/value exposed programmatically |
| 3.3.1 / 3.3.2 | Errors identified in text; inputs have labels/instructions |
| 2.5.7 Dragging Movements — new | Any drag action has a single-pointer alternative |
| 3.3.8 Accessible Authentication (Minimum) — new | No cognitive test to log in; allow paste and password managers |

2.2 also removed 4.1.1 Parsing. The 44×44 px target size is 2.5.5 at AAA.

## 3. Fix with semantic HTML first
The first rule of ARIA: if a native element does the job, use it. A `<button>` gives focus,
Enter/Space activation and the button role for free; a `<div onclick>` gives none.
```html
<button type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email" aria-describedby="email-err" aria-invalid="true">
<p id="email-err">Enter an email like name@example.com</p>
<button aria-label="Close dialog"><svg aria-hidden="true">…</svg></button>
```
- One `<h1>`, headings in order; landmarks `<header> <nav> <main> <footer>`; a skip link to `<main>`.
- Placeholder is not a label. Icon-only buttons need an accessible name.
- ARIA rules: don't change native semantics (`<h2 role="button">`); every ARIA widget must implement the keyboard pattern from the APG; never `aria-hidden="true"` on focusable elements. Bad ARIA is worse than none.
- Use native `<dialog>` with `showModal()` for modals — it traps focus and handles Esc. Return focus to the trigger on close.
- Status messages ("Saved", "3 results") go in a live region present in the DOM before the update: `<div role="status">`.

## 4. Keyboard test script
`Tab`/`Shift+Tab` through the whole page: order follows visual order, every interactive
element is reachable, the focus ring is clearly visible (never `outline: none` without a
replacement — use `:focus-visible { outline: 2px solid; outline-offset: 2px; }`). `Enter`
activates links and buttons, `Space` buttons and checkboxes, arrows within menus/tabs/radios,
`Esc` closes overlays. Nothing focusable hides off-screen or behind a sticky header. Positive
`tabindex` values are a defect; use `0` or `-1` only.

## 5. Screen reader test
| Platform | Pairing |
|---|---|
| Windows | NVDA (free) + Firefox or Chrome; JAWS if users/contracts require it |
| macOS / iOS | VoiceOver + Safari |
| Android | TalkBack + Chrome |

Check: page title and `lang` announced; headings list (the screen reader's elements list or rotor)
makes sense alone; every control announces name, role and state; form errors are announced;
images convey the right information; dynamic updates are spoken.

## Verify
- [ ] axe reports zero violations on key templates, and the keyboard and screen-reader passes were also done.
- [ ] Text contrast ≥ 4.5:1 (3:1 large), UI and focus indicators ≥ 3:1, in every theme.
- [ ] All targets ≥ 24×24 CSS px or adequately spaced.
- [ ] Full task completed keyboard-only with visible, unobscured focus.
- [ ] Task completed with NVDA and VoiceOver; every control has a sensible name.
- [ ] Page works at 320px width and 200% zoom.

## Checked
2026-11-01. Confirmed against the WCAG 2.2 Recommendation (w3.org/TR/WCAG22): the criteria names and numbers, the 4.5:1, 3:1, 24 px target size and 320 CSS px reflow figures, 200% resize, and 4.1.1 Parsing removal. Removed: the automated-coverage percentage, specific screen reader shortcuts and the named laws, which were not confirmed. The Quick Reference page returned no text.
Method: documentation only; no commands were run.
