---
id: computing-software.web-development.web-accessibility.accessibility-annotations-in-design-handoff
name: accessibility-annotations-in-design-handoff
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility-annotations, design-handoff, figma-accessibility, shift-left-accessibility, focus-order]
level: practitioner
status: docs-checked
description: "Annotating designs for accessibility before build: headings, landmarks, focus order, names, states, alt text and errors, with Figma annotation kits."
sources:
  - https://www.w3.org/WAI/planning/
  - https://github.com/cvs-health/annotations
  - https://www.figma.com/community/file/953682768192596304
  - https://design-system.service.gov.uk/accessibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessibility annotations in design handoff

Most accessibility defects are decided in design. Annotations make the invisible parts (semantics, order, names, behaviour) explicit so developers don't guess.

## 1. What to annotate on every screen
| Annotation | Example |
|---|---|
| Headings | H1 "Your basket", H2 per section |
| Landmarks | header, nav "Primary", main, aside "Related", footer |
| Focus order | numbered path through interactive elements, especially for non-linear layouts and modals |
| Accessible names | icon-only buttons: "Close dialog", "Remove item: Blue mug" |
| Images | alt text or "decorative" per image |
| States | expanded/collapsed, selected, disabled, loading, error, empty |
| Live announcements | "3 results found", "Saved" toast, polite vs assertive |
| Focus management | where focus goes on open, close, delete, route change |
| Keyboard behaviour | arrow keys in tabs/menus, Esc closes |
| Reflow | what stacks or collapses at narrow widths and large text sizes |
| Touch targets | size and spacing of small or dense controls |

## 2. Tools
- Annotation kits: CVS Health publishes open-source accessibility annotations (github.com/cvs-health/annotations). Keep annotations on a separate layer/page so visuals stay clean.
- Contrast checkers for colour; check every state (hover, focus, disabled, error).
- Use design-system components that already encode behaviour; annotate only deviations.

## 3. Process
1. Designer annotates at hand-off; accessibility specialist reviews in the same design review as visuals.
2. Annotations become acceptance criteria in the ticket ("Focus returns to 'Add address' after the dialog closes").
3. QA tests against the annotations with keyboard and screen reader before sign-off.
4. Recurring gaps feed back into the design system (e.g. a default error-summary pattern).

## 4. Common misses
Focus indicator design, error messages text and placement, empty and loading states, what screen readers hear for charts, heading levels that skip, text-in-images.

## Verify
- [ ] Each delivered screen has annotations for headings, landmarks, focus order, names, states and announcements; tickets include them as acceptance criteria.

## Checked
2026-10-28 Confirmed: the CVS Health open-source accessibility annotations repository exists (github.com/cvs-health/annotations). Removed: pixel target sizes, reflow figures, named third-party kits and plugins (not confirmed on fetched pages; Figma community page was blocked).
Method: documentation only; no commands were run.
