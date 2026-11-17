---
id: computing-software.web-development.web-accessibility.error-summary-and-submit-focus
name: error-summary-and-submit-focus
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, error-summary, focus-management, form-submission-errors, error-list, aria-describedby]
level: practitioner
status: docs-checked
description: "Building an accessible error summary: focusing it on failed submit, linking each error to its field, titles prefixed with Error, and SPA vs server-rendered behaviour."
sources:
  - https://design-system.service.gov.uk/components/error-summary/
  - https://design-system.service.gov.uk/patterns/validation/
  - https://www.w3.org/WAI/tutorials/forms/notifications/
  - https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error summary and focus management on submit

**Goal:** after a failed submission, users immediately learn how many problems there are and can jump to each field.

## 1. Markup (GOV.UK pattern)
```html
<div class="error-summary" tabindex="-1" aria-labelledby="error-summary-title">
  <h2 id="error-summary-title">There is a problem</h2>
  <ul>
    <li><a href="#email">Enter an email address in the correct format, like name@example.com</a></li>
    <li><a href="#dob-day">Date of birth must be in the past</a></li>
  </ul>
</div>
```
- Same message text as the inline error next to each field.
- Link target is the input's id (for groups, the first input) so activating the link moves focus to the field. With a sticky header, links can scroll the field under it - use `scroll-margin-top` on inputs.

## 2. Focus it
```js
form.addEventListener('submit', (e) => {
  const errors = validate(form);
  if (!errors.length) return;
  e.preventDefault();
  renderSummary(errors); renderInlineErrors(errors);
  summary.focus();               // announces heading + list
});
```
- Server-rendered: render the summary at the top of `<main>` and focus it on load (GOV.UK Frontend's JavaScript moves focus to the summary for you; otherwise use a small script), and prefix `<title>` with "Error: ".

## 3. When to choose live announcement instead
For inline async validation (username taken) use a polite live region near the field rather than moving focus.

## 4. Keep it in sync
Remove summary entries as the user fixes fields on resubmit; never leave a stale summary.

## Verify
- [ ] Failed submit: screen reader announces "There is a problem" and the list; focus is on the summary.
- [ ] Each link moves focus to its field, visible below any sticky header.
- [ ] Page title starts with "Error:" on server-rendered error pages.

## Checked

- Date: 2026-10-26. Documentation: GOV.UK Design System error summary component, WAI Forms tutorial (notifications), WCAG 2.2 3.3.1, MDN `scroll-margin-top`.
- Confirmed: move keyboard focus to the summary, heading "There is a problem", messages worded the same as the inline errors, link to the first field (first radio or checkbox, first date field), prefix the page title with "Error: ".
- Removed (no documentation found): the `role="alert"` double-announcement claim, the `autofocus` claim and the single-field exception.
Method: documentation only; no commands were run.