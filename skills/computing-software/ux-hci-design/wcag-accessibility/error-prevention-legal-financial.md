---
id: computing-software.ux-hci-design.wcag-accessibility.error-prevention-legal-financial
name: error-prevention-legal-financial
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [error-prevention-legal, review-confirm-step]
level: practitioner
status: docs-checked
description: "Make legal, financial and data-deleting submissions reversible, checked or confirmed (SC 3.3.4)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 3.3.4 Error Prevention (Legal, Financial, Data) (AA)
Applies to pages that cause legal commitments or financial transactions, that modify or delete user-controllable data, or that submit test responses. At least one of:
- Reversible: submissions are reversible (technique G164: a stated time within which a request can be amended or cancelled).
- Checked: data is checked for input errors and the user can correct them.
- Confirmed: a mechanism to review, confirm and correct information before finalizing (G98 review and correct answers; G168 request confirmation; G155 a checkbox in addition to a submit button).
- For deletion, recovering deleted information (G99) is also a sufficient technique.
- "User-controllable" data means data the user can view and change or delete, such as account details or past invoices, not logs. The intent is to prevent mass loss such as deleting a file or record; a confirmation for each save is not required.
- Example from the page: an order confirmation page showing items, quantities, shipping address and payment method that the user can confirm or change.

## Verify
- [ ] The final step offers at least one of reverse, check or review-and-confirm.

## Checked

2026-11-09. Confirmed on the Understanding SC 3.3.4 page: the criterion text and Level AA, the three options, the scope (legal, financial, user-controllable data, test responses), techniques G164, G98, G168, G155, G99, the user-controllable definition and the order confirmation example. Removed: nothing substantive; the "cancel window" and "validated" wording was replaced with the page's text.

Method: documentation only; no commands were run.
