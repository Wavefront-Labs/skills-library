---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-inline-validation
name: designing-inline-validation
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [inline-validation, form-validation, real-time-validation, validation-timing, form-design, error-messages, accessibility]
level: practitioner
status: draft
description: "Design inline form validation: validate on blur not keystroke, show success sparingly, keep errors next to fields, summarise on submit, and announce to screen readers."
sources:
  - "Baymard Institute - Inline Form Validation (baymard.com/blog/inline-form-validation)"
  - "Luke Wroblewski - Inline Validation in Web Forms, A List Apart (alistapart.com/article/inline-validation-in-web-forms)"
  - "W3C WAI - Forms Tutorial: Validating Input (w3.org/WAI/tutorials/forms/validation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inline validation

**Goal:** catch problems early without nagging, and make fixing them easy.

## Timing (premature validation is the main sin)
- Validate on **blur** (field loses focus) after the first entry, then **live** while correcting an error ("reward early, punish late").
- Do not flag an error while the person is still typing a valid-in-progress value (email before "@" typed).
- For slow checks (username availability) show a small progress state and validate after a short pause or on blur.
- **Password fields:** show rules and strength live, since users need guidance as they type.
- On **submit**, validate everything; place an error summary at the top with links to each field, and move focus to the summary (or first error).

## Messages
- Next to the field, above or below consistently; icon, colour and text; specific and constructive (`creative-arts.design-for-form-and-experience.ux-design.writing-helpful-error-messages`).
- Keep the input value; remove the error as soon as it is valid.
- Success marks (green tick) only where reassurance helps (username availability, card number); not on every field.

## Accessibility
- Associate messages with `aria-describedby`; set `aria-invalid="true"`; announce with `role="alert"` or an `aria-live="polite"` region.
- Do not rely on colour; keep focus order logical.
- Prefer `novalidate` plus custom messages, with the Constraint Validation API for logic and server-side validation as the source of truth.

## Verify
- [ ] No errors appear before the user leaves the field (except password guidance).
- [ ] Errors are linked, announced and specific; summary on submit.
- [ ] Server validates everything the client does.
