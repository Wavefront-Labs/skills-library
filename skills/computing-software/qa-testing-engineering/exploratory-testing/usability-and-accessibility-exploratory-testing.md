---
id: computing-software.qa-testing-engineering.exploratory-testing.usability-and-accessibility-exploratory-testing
name: usability-and-accessibility-exploratory-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [accessibility, a11y, usability-testing, wcag, screen-reader, nvda, voiceover, jaws, keyboard-navigation, focus-order, keyboard-trap, color-contrast, manual-a11y-testing, assistive-technology, cognitive-load, heuristic-evaluation, nielsen-heuristics, usability-heuristic-review, focus-management]
level: practitioner
status: draft
description: "Manually test usability and accessibility by hand: keyboard-only navigation, a screen reader pass, focus order and traps, and a heuristic evaluation — the issues automated axe scans miss."
sources: ["https://www.nngroup.com/articles/ten-usability-heuristics/", "https://www.w3.org/WAI/WCAG21/quickref/", "https://webaim.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual usability and accessibility exploratory testing

**Goal:** find the usability and accessibility problems a real user with a
keyboard, a screen reader, or just low patience would hit — the ones automated
scanners (axe, Lighthouse) structurally cannot see because they check markup, not
experience.

## 1. Why automated a11y scans aren't enough
Tools like axe-core catch ~30-50% of WCAG failures: missing labels, bad contrast,
invalid ARIA. They cannot tell you whether the *reading order* makes sense, whether
alt text is actually descriptive versus just present, whether a custom widget
announces its state change, or whether the tab order matches the visual layout.
Those need a human pass. Run both — automated as a floor, manual as the real check.

## 2. Keyboard-only pass (do this first — it's the fastest to run)
Unplug the mouse mentally: `Tab`/`Shift+Tab` through every interactive element,
`Enter`/`Space` to activate, arrow keys inside composite widgets (menus, tabs,
sliders), `Esc` to dismiss. Check for:
- **Focus order** matches visual/logical order, not DOM order if they diverge.
- **Visible focus indicator** on every focusable element (a removed `outline: none`
  with no replacement is the single most common finding).
- **Keyboard traps**: a modal, date picker, or embedded widget you can tab into
  but not out of — a hard blocker, not a nice-to-have.
- Every mouse-only interaction (hover menu, drag-drop, click-outside-to-close) has
  a keyboard equivalent.

## 3. Screen reader pass
Use the OS-native reader that matches real users: NVDA (Windows, free) or VoiceOver
(macOS/iOS, built in) are the two to cover first; JAWS if the user base is known to
use it. Navigate by heading (`H` in NVDA) and by landmark, not just linearly — this
surfaces missing heading structure fast. Listen for: buttons announced as "button,
unlabeled"; images read as filenames; form fields with no associated label read as
just a type ("edit text"); live regions (toast notifications, error banners) that
update visually but say nothing. Do this with eyes closed or monitor off for at
least one pass — reading the accessibility tree while looking at the screen hides
exactly the problems a blind user would hit.

## 4. Heuristic usability evaluation
Walk the flow against Nielsen's 10 heuristics, writing one note per violation
(heuristic name + what you saw + why it costs the user): visibility of system
status (does a long action show progress?), error prevention and recovery
(confirmation before a destructive action, clear recovery path after), consistency
with platform conventions, recognition over recall (does the user have to remember
something from 3 screens ago?). This is a structured version of the general
heuristics in the session-based exploratory testing skill, scoped specifically to
usability.

## 5. Reporting these findings
File like any exploratory bug (see bug-report-triage-and-severity-priority): state
the WCAG success criterion violated where applicable (e.g., "2.1.2 No Keyboard
Trap"), the assistive tech/browser combo used, and the user-facing cost, not just
"inaccessible." Severity for a11y issues should reflect blocking vs. degraded
experience, not just visual prominence — a keyboard trap on checkout is Sev-1 even
though it looks like "nothing is visually wrong."

## Unconfirmed / notes
Screen reader behavior differs by browser pairing (NVDA+Firefox vs NVDA+Chrome) —
verify findings in at least the pairing your users actually use before filing as
confirmed. Not benchmarked against a specific WCAG conformance audit here.

## Verify
- [ ] Every interactive element reachable and operable by keyboard alone.
- [ ] No keyboard trap in any modal, widget, or embedded iframe.
- [ ] A full screen-reader pass done with the screen off or eyes closed.
- [ ] Each finding cites the WCAG criterion (where applicable) and AT/browser combo.
- [ ] Heuristic findings tie to user cost, not just "looks off."
