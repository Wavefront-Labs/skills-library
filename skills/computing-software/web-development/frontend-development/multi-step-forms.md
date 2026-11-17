---
id: computing-software.web-development.frontend-development.multi-step-forms
name: multi-step-forms
category: computing-software
field: web-development
product: frontend-development
tags: [multi-step-form, form-wizard, form-state, progressive-enhancement, html-forms]
level: practitioner
status: docs-checked
description: "Building multi-step forms: step structure, per-step validation with reportValidity, preserving progress, history integration, focus on step change and server checks."
sources:
  - https://design-system.service.gov.uk/patterns/question-pages/
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/reportValidity
  - https://www.w3.org/WAI/tutorials/forms/multi-page/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-step forms

## 1. Structure options
- **One page per step, server-held state** (the GOV.UK question-pages pattern): works without JS, survives refresh, every step POSTs and the server stores a draft keyed to the session. Most robust.
- **Single form, fieldsets shown one at a time**: one final submit; hidden steps must not block validation of the current one.

## 2. Per-step validation (single form)
```js
function validateStep(fieldset) {
  for (const el of fieldset.elements) if (!el.checkValidity()) { el.reportValidity(); return false; }
  return true;
}
next.addEventListener("click", () => {
  if (!validateStep(steps[i])) return;
  steps[i].hidden = true; steps[++i].hidden = false;
  steps[i].querySelector("h2").focus();          // h2 has tabindex="-1"
  history.pushState({ step: i }, "", `?step=${i + 1}`);
});
addEventListener("popstate", e => showStep(e.state?.step ?? 0));
```
Hidden fieldsets with `required` inputs can block the final `submit` because the browser cannot focus them to show the error; set `disabled` on hidden fieldsets or validate per step and use `novalidate` on final submit after your own checks.

## 3. Preserve progress
- Save to `sessionStorage` on `input` (debounced); restore on load. Never store passwords or card numbers.
- For long forms (applications), save server drafts and email a resume link.

## 4. Accessibility
- Progress: `<ol>` of steps with `aria-current="step"`, plus "Step 2 of 5" in the heading or title.
- Move focus to the new step heading; update `document.title`.
- Check-your-answers summary page before submit, with "Change" links back to each step.

## 5. Server
Re-validate everything on final submit; a client can skip steps by editing the URL or POSTing directly.

## Verify
- [ ] Browser Back goes to the previous step, not off the form.
- [ ] Refresh mid-form keeps entered data.
- [ ] Screen reader announces the new step heading after Next.

## Checked
2026-10-28. Confirmed on MDN: `HTMLFormElement.reportValidity()` exists (the skill applies it per element via the same validity API). Removed: the browser error string and the WCAG criterion number (not located on the fetched pages). Other guidance is design advice without figures.
Method: documentation only; no commands were run.
