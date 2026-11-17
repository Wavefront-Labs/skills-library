---
id: computing-software.general-digital-literacy.internet-navigation.form-will-not-submit
name: form-will-not-submit
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-forms-accounts, form-errors, web-form, validation-errors]
level: intro
status: draft
description: "Fix an online form that will not submit: hidden errors, field formats, autofill, upload limits, timeouts and browser blocks, without losing your answers."
sources:
  - https://www.w3.org/WAI/tutorials/forms/notifications/
  - https://support.google.com/chrome
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Form will not submit

## Find the error
- Scroll up and down: errors often appear at the top in a summary or as red text beside a field you can't see.
- Required fields marked *; checkboxes like "I agree" are often the missed one.
- Screen readers: the error summary should be announced; Tab through fields to find the one flagged.

## Common causes
- **Format**: phone without spaces or with country code, postcode format, dates DD/MM/YYYY vs MM/DD/YYYY, no dashes in card numbers, name with apostrophes or accents rejected by poor validation.
- **Autofill** put the wrong data in a hidden or similar field; clear and type manually.
- **Password rules** (length, symbol) shown only after failure.
- **Upload**: file too big or wrong type; see the upload-documents skill.
- **Session timeout**: long forms expire (often 20-30 minutes) and silently fail. Save drafts if offered.
- **CAPTCHA** not completed or blocked by a privacy extension.
- **Browser**: ad/tracker blockers, strict tracking prevention or an outdated browser stop scripts. Try a private window with extensions off, or another browser.

## Don't lose your answers
- Write long answers in a text editor first and paste them in.
- Don't press Back after submitting payment forms; check email for confirmation before retrying to avoid double charges.

## Still stuck
- Note the exact error, screenshot it, and contact the organisation; many government forms have phone or paper alternatives.

## Verify
- [ ] Confirmation page or email received with a reference number.
