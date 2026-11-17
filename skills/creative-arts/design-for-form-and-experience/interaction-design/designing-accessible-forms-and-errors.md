---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-accessible-forms-and-errors
name: designing-accessible-forms-and-errors
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [accessible-forms, accessible-form-errors, form-labels, error-identification, wcag-forms, form-accessibility]
level: practitioner
status: docs-checked
description: "Design accessible forms: persistent labels, instructions, error identification and suggestions, input purpose, redundant entry and accessible authentication."
sources:
  - "https://www.w3.org/TR/WCAG22/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accessible forms and errors

## Requirements (WCAG 2.2)
- **SC 3.3.2 Labels or Instructions (A):** labels or instructions are provided.
- **SC 1.3.5 Identify Input Purpose (AA):** fields about the user (name, email, address) identify their purpose programmatically (for example with `autocomplete`).
- **SC 3.3.1 Error Identification (A):** errors are identified and described to the user in text.
- **SC 3.3.3 Error Suggestion (AA):** when known, suggest a correction, unless it would jeopardise security or purpose.
- **SC 3.3.4 Error Prevention (Legal, Financial, Data) (AA):** for such submissions, make them reversible, checked or confirmed.
- **SC 3.3.7 Redundant Entry (A, new in 2.2):** information entered earlier in the same process is auto-populated or selectable, unless re-entry is essential, needed for security, or the data is no longer valid.
- **SC 3.3.8 Accessible Authentication (Minimum) (AA, new in 2.2):** no cognitive function test at any login step unless there is an alternative, an assisting mechanism (password managers, paste), object recognition or personal content.

## Design
1. **Visible, persistent labels** above fields, programmatically associated with the input; placeholders are not labels (see `...interaction-design.writing-form-labels-placeholders-and-help-text`).
2. Mark required fields in text, not colour alone; group related fields with `fieldset` and `legend`.
3. **Errors:** show an error summary at the top that links to each field, and inline messages beside fields; associate each message with its field programmatically; move focus to the summary or first error on submit (see `...interaction-design.designing-inline-validation` and `...ux-design.writing-helpful-error-messages`).
4. **Do not rely on colour,** icons need text.
5. **Preserve input after errors.**
6. **Test** with keyboard and a screen reader (see `...interaction-design.designing-for-screen-readers-and-aria`).

## Verify
- [ ] Every input has a programmatic label.
- [ ] Errors are announced and reachable from the summary.
- [ ] No redundant entry; password manager works.

## Checked
2026-11-01. Confirmed in WCAG 2.2 (w3.org/TR/WCAG22): the text, level and "new in 2.2" status of SC 1.3.5, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7 and 3.3.8. Removed: the "allow enough time" item, and the specific ARIA attribute names (not in WCAG; see the screen-reader skill).
Method: documentation only; no commands were run.
