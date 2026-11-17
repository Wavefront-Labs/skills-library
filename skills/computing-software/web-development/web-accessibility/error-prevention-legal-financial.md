---
id: computing-software.web-development.web-accessibility.error-prevention-legal-financial
name: error-prevention-legal-financial
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, error-prevention, wcag-3-3-4, review-step, confirmation-step, undo, reversible-submissions]
level: practitioner
status: docs-checked
description: "Meeting WCAG 3.3.4 Error Prevention for legal, financial and data submissions: reversible actions, input checking, review-and-confirm steps and undo windows."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G98
  - https://design-system.service.gov.uk/patterns/check-answers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error prevention for legal, financial and data submissions

**Goal:** a mistyped amount, wrong account or accidental delete can be caught or undone before it costs the user.

## 1. When it applies (3.3.4, AA)
Pages that create legal commitments or financial transactions, modify/delete user-controllable data in storage, or submit test responses. At least one of:
1. **Reversible** - submissions can be undone (cancel an order within a set period, restore from trash).
2. **Checked** - input is checked for errors and the user can correct them.
3. **Confirmed** - a review step lets the user check and correct before final submission.

## 2. Patterns
- **Check your answers page**: summary of everything with "Change" links back to each question (GOV.UK pattern); the final button names the action it performs (for example "Send your claim form").
- **Destructive actions**: soft delete + undo toast ("Project deleted. Undo") beats confirm dialogs (people click through confirms). For irreversible, high-impact deletes, require typing the name.
- **Payments**: show amount, payee and date on a confirm step; validate account/IBAN formats; warn on unusual amounts.
- **Exams/tests**: review screen listing unanswered questions before submit.

## 3. Implementation notes
- Undo windows need server support (pending state, delayed execution job, or reversible operations) - not just UI.
- Prevent double submission (disable button while submitting, idempotency keys).
- "Change" links must return to the summary after editing, preserving other answers.
- The undo toast must be reachable by keyboard and stay long enough to be used; if it times out, 2.2.1 Timing Adjustable applies.

## Verify
- [ ] Every legal/financial/data-deletion flow has at least one of reversible/checked/confirmed.
- [ ] Review page shows all entered data and every item can be changed.
- [ ] Undo works by keyboard and screen reader.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 3.3.4 text and Understanding page, technique G98, GOV.UK Design System check answers pattern.
- Confirmed: 3.3.4 is Level AA and applies to legal commitments, financial transactions, modifying or deleting user-controllable data, and test submissions, needing one of reversible, checked or confirmed; "Change" links on a check answers page that return the user to it afterwards; the submit button names the action; the Understanding page says confirmation is not needed for every save.
- Removed (no documentation found): the "30 min" and "3 s" example figures.
Method: documentation only; no commands were run.