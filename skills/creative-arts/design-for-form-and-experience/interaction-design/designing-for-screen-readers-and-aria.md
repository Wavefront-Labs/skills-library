---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-for-screen-readers-and-aria
name: designing-for-screen-readers-and-aria
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [screen-reader, aria, wai-aria, accessible-name, semantic-html, aria-live]
level: practitioner
status: docs-checked
description: "Design for screen readers: semantic structure, accessible names, roles, states and live regions, with the rule of using native HTML before ARIA."
sources:
  - https://www.w3.org/TR/using-aria/
  - https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  - https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
  - https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Screen reader semantics and ARIA

Screen readers use the accessibility tree, built from the DOM, to announce what things are and how they behave.

## Principles
- **First rule of ARIA** (Using ARIA): if a native HTML element or attribute already has the semantics and behaviour you need, use it instead of repurposing an element and adding ARIA. The APG adds: no ARIA is better than bad ARIA.
- **Structure:** a logical heading hierarchy, landmarks (`header`, `nav`, `main`, `footer`, `aside`), lists for lists, tables for data (SC 1.3.1 Info and Relationships). Landmarks give screen reader users keyboard navigation to page sections and serve as skip-link targets (APG).
- **Name, role, value (SC 4.1.2):** every control has a programmatically determined name and role, and its user-settable states and values can be set programmatically and changes are notified to assistive technology. Typical state attributes: `aria-expanded`, `aria-pressed`, `aria-selected`, `aria-checked`, `aria-disabled`, `aria-current`; names come from visible label text, `aria-labelledby` or `aria-label`.
- **Labels match visible text** so voice-control users can say what they see (SC 2.5.3 Label in Name).
- **Live regions** (`aria-live="polite"` or `role="status"`) announce updates such as search results or toasts without moving focus (SC 4.1.3 Status Messages); reserve `role="alert"` and `aria-live="assertive"` for important, time-sensitive content.
- **Hidden content:** an element hidden with `display:none` or `visibility:hidden` is not focusable and is removed from the accessibility tree. Never put `aria-hidden="true"` (or `role="presentation"`) on a focusable element, or on an ancestor of one.

## Design deliverables
In handoff annotate heading levels, landmarks, accessible names, reading order and live-region content (see `...interaction-design.annotating-designs-for-accessibility`).

## Test
Navigate with a screen reader: headings list, landmark list, form fields, a full task.

## Verify
- [ ] Each interactive element has a name, role and state announced correctly.
- [ ] Headings and landmarks give a usable outline.
- [ ] Dynamic updates are announced.

## Checked
2026-11-01. Confirmed against Using ARIA (first rule, aria-hidden and display:none guidance), the APG read-me-first and landmark pages, and the W3C Understanding pages for SC 4.1.2, 4.1.3, 1.3.1 and 2.5.3. Removed: the list of named screen readers, the single-h1 rule, the decorative-alt-text rule and the hidden-attribute claim (no fetched page states them).
Method: documentation only; no commands were run.
