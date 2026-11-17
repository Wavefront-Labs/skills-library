---
id: computing-software.web-development.web-accessibility.info-and-relationships-programmatic-structure
name: info-and-relationships-programmatic-structure
category: computing-software
field: web-development
product: web-accessibility
tags: [info-and-relationships, programmatic-structure, wcag-1-3-1, wcag-1-3-2, semantic-html, list-semantics]
level: practitioner
status: docs-checked
description: "Meeting WCAG 1.3.1 and 1.3.2: making visual structure programmatic with real headings, lists, tables, labels and groups, and keeping DOM reading order meaningful."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
  - https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F2
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F46
  - https://github.com/dequelabs/axe-core/blob/HEAD/doc/rule-descriptions.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Programmatic structure matches visual structure

**1.3.1 (A):** information, structure and relationships conveyed visually are available in markup (or text). **1.3.2 (A):** DOM order preserves meaning.

## 1. Map visual cue to markup
| Looks like | Must be |
|---|---|
| Big bold section title | `<h2>`-`<h6>` at the right level (not a styled `<div>`/`<p><b>`) |
| Bulleted/numbered items, nav link groups | `<ul>`/`<ol>`/`<li>`; description pairs `<dl>` |
| Grid of data with headers | `<table>` with `<th>`/scope/caption |
| Text next to a field | `<label for>` |
| Group of radios/checkboxes with a question | `<fieldset><legend>` |
| Required marked with * | `required` / `aria-required` plus text explanation |
| Emphasised warning text | `<strong>` and words ("Warning:"), not only colour |
| Quotes, code, abbreviations | `<blockquote>`, `<code>`, `<abbr title>` where helpful |
| Visual regions | landmarks |

## 2. Common failures
- F2: using CSS styling alone to convey structure (fake headings).
- F33/F34: using whitespace/tabs to create columns or tables in plain text.
- F46: `th`, `caption` or non-empty `summary` in layout tables.
- F68 (a 4.1.2 failure): form controls without a programmatically determined name.
- Data in `<div>` grids that look like tables.
- Card components where the heading isn't a heading.
- ARIA roles used instead of native elements, but without the required owned elements (e.g. `role="list"` with children lacking `role="listitem"`).

## 3. Reading order (1.3.2)
- CSS `order`, `flex-direction: *-reverse`, grid placement, `position: absolute` can make visual order differ from DOM. If the meaning depends on order (steps, price then "per month"), DOM order must match.
- Modals/popovers appended at the end of `body` are fine (focus management handles context); inline content that's visually first but last in DOM is not.

## 4. Safari and list semantics
Safari with VoiceOver has been reported to drop list semantics when CSS removes list markers, apparently deliberately (Scott O'Hara's write-up, https://www.scottohara.me/blog/2019/01/12/lists-and-safari.html; secondary source, re-test in current Safari). Where the list count matters, test and, if needed, add `role="list"` on the `<ul>`.

## Verify
- Disable CSS (for example with a developer toolbar or a bookmarklet): content still reads in a sensible order with visible structure.
- Screen reader headings/lists/tables navigation lists what sighted users perceive.
- axe: `list`, `listitem`, `definition-list`, `th-has-data-cells`, `label`, `p-as-heading`.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria and techniques F2, F33, F34, F46, F68; axe-core 4.14 rule descriptions.
- Confirmed: 1.3.1 and 1.3.2 are Level A; F2 (text presentation without markup), F33 and F34 (white space for columns and tables), F46 (`th`, `caption`, `summary` in layout tables); axe rules `list`, `listitem`, `definition-list`, `th-has-data-cells`, `label` and `p-as-heading` exist.
- Corrected: F68 is a 4.1.2 failure, not a 1.3.1 one. The Safari list-semantics behaviour is documented only in a secondary source and is stated as reported; the Firefox menu path was removed.
Method: documentation only; no commands were run.