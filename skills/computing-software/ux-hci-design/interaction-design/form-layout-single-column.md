---
id: computing-software.ux-hci-design.interaction-design.form-layout-single-column
name: form-layout-single-column
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [form-layout, top-aligned-labels, id-forms]
level: practitioner
status: draft
description: "Lay out forms in one column with top-aligned persistent labels, grouped fields and a clear primary action."
sources:
  - https://www.nngroup.com/articles/web-form-design/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Form layout
- Single column completes faster and reduces misreading order; side-by-side only for short related fields (city/postcode, day/month/year).
- Labels above fields, persistent (not placeholder-only); inline hints below the label.
- Field width signals expected input length.
- Group with `fieldset`/`legend`; one primary submit button, secondary actions visually lighter.
- Ask only what you need; each field lowers completion.

## Verify
- [ ] Remove one unnecessary field and compare completion in A/B or testing.
