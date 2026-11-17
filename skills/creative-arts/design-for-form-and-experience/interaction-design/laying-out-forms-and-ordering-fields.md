---
id: creative-arts.design-for-form-and-experience.interaction-design.laying-out-forms-and-ordering-fields
name: laying-out-forms-and-ordering-fields
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [form-layout, form-design, web-forms, field-order, single-column-forms, form-usability]
level: practitioner
status: draft
description: "Lay out web forms for completion: single column, logical field order, grouped sections, labels above fields, field length hints, and fewer fields with clear primary action."
sources:
  - "Luke Wroblewski, Web Form Design: Filling in the Blanks (Rosenfeld, 2008)"
  - "Baymard Institute - Checkout usability and form field guidelines (baymard.com/blog)"
  - "Nielsen Norman Group - Website Forms Usability: Top 10 Recommendations (nngroup.com/articles/web-form-design)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Form layout and field order

**Goal:** people finish the form quickly and correctly.

## Rules
1. **Ask for less:** every field must justify itself; drop or defer optional fields. Each removed field typically lifts completion.
2. **Single column:** faster and fewer errors than multi-column (CXL and Baymard research); pair related short fields (city / state / postcode, expiry / CVC) only when they form a natural unit.
3. **Logical order,** matching the user's mental model and data dependencies (name, email, then address); group in labelled sections with headings; keep related questions together.
4. **Labels above fields,** left-aligned: fastest to scan and works on mobile and for long labels; right-aligned labels beside fields are a compact option for experts.
5. **Field width signals expected length** (postcode short, street long).
6. **Mark optional fields** ("optional") rather than asterisking most fields; when most are required, say so once at the top.
7. **One primary action**; secondary actions visually quieter and separated; a clear label ("Create account"); do not put a reset button next to submit.
8. **Preserve data** on error and back navigation; support autofill with correct `autocomplete` attributes.
9. **Mobile:** 16 px minimum font to avoid iOS zoom; correct input types (see `creative-arts.design-for-form-and-experience.interaction-design.choosing-input-types-masks-and-formatting`).

## Test
Usability-test with 5 users filling in a real task; watch hesitations and corrections; measure field-level drop-off (analytics for "form field abandonment").

## Verify
- [ ] Each field has a documented reason; optional fields marked.
- [ ] Single column, labels above, grouped sections, one primary action.
- [ ] Tested with users on mobile and desktop.
