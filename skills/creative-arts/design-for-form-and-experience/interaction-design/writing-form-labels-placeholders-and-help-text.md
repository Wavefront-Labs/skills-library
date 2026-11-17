---
id: creative-arts.design-for-form-and-experience.interaction-design.writing-form-labels-placeholders-and-help-text
name: writing-form-labels-placeholders-and-help-text
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [form-labels, placeholders, help-text, hint-text, form-design, accessibility, microcopy]
level: practitioner
status: draft
description: "Write form labels, placeholders and help text: persistent visible labels, no placeholder-as-label, concise hints with format examples, and accessible associations."
sources:
  - "Nielsen Norman Group - Placeholders in Form Fields Are Harmful (nngroup.com/articles/form-design-placeholders)"
  - "W3C WAI - Forms Tutorial: Labels (w3.org/WAI/tutorials/forms/labels)"
  - "GOV.UK Design System - Text input and hint text (design-system.service.gov.uk/components/text-input)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Labels, placeholders and help text

**Goal:** every field is understandable before, during and after typing, for sighted and assistive-tech users.

## Labels
- Always a **visible, persistent label** (not only a placeholder or floating label alone). Programmatically tied: `<label for="email">` or wrapping.
- Short noun phrases in sentence case: "Email address". Questions only when needed.
- Required vs optional: mark the minority; for required fields use `required` and `aria-required` consistently.

## Placeholders
- Vanish on typing, have low contrast, are mistaken for filled values, and are not reliably announced. Do **not** use them for labels or essential instructions.
- Use only for a short example of format ("name@example.com") if at all, and ensure 4.5:1 contrast, or move the example into hint text.

## Help text (hints)
- Placed between label and input, always visible, linked with `aria-describedby`.
- Say what to enter and why: "Use the name on your passport" or "We only use this for delivery updates".
- Format examples: "For example, 12 11 2007". Password rules shown before typing, not only after failing.
- Avoid tooltips-only help; collapsible "Why we ask" for longer explanations.

## Floating labels
Acceptable only if the label stays visible and legible after focus (small label at top) and has adequate contrast; risk: truncation of long labels and cramped height.

## Verify
- [ ] Every field has a visible label bound with for/id.
- [ ] Placeholders carry no required information.
- [ ] Hints linked with aria-describedby; examples in hint text.
