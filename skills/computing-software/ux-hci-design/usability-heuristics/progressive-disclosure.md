---
id: computing-software.ux-hci-design.usability-heuristics.progressive-disclosure
name: progressive-disclosure
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [progressive-disclosure, staged-disclosure]
level: practitioner
status: draft
description: "Show core options first and reveal advanced ones on demand without hiding the path to them."
sources:
  - https://www.nngroup.com/articles/progressive-disclosure/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Progressive disclosure
- Split features into primary (most users, frequent) and secondary (advanced).
- Reveal via "Advanced" sections, accordions, modals, or step-by-step.
- Keep disclosure to about two levels deep; more hurts findability.
- Clear signifiers (chevron, "Show more") with `aria-expanded` for assistive tech.

## Gotchas
- Do not hide critical info (price, terms) behind disclosure.
- Usage data decides what is primary, not stakeholder opinion.

## Verify
- [ ] Task success for advanced features remains acceptable in testing.
