---
id: computing-software.ux-hci-design.interaction-design.inline-validation-timing
name: inline-validation-timing
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [inline-validation, validation-timing]
level: practitioner
status: draft
description: "Validate on blur (not while typing) and show success or errors adjacent, keeping submit enabled."
sources:
  - https://www.nngroup.com/articles/errors-forms-design-guidelines/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inline validation
- Validate after the user leaves the field (blur), not on first keystroke; exception: password strength meters and character counters, which update live.
- Show errors next to the field in text (not colour alone) and in an error summary after submit.
- Keep submit enabled; disabled buttons give no explanation of what is wrong.
- Accept variations: spaces and hyphens in phone/card numbers; normalise server-side.
- HTML: `required`, `type=email`, `pattern`, `inputmode`, constraint validation API (`setCustomValidity`).

## Verify
- [ ] Type a bad value then tab away: error appears once, clears when fixed.
