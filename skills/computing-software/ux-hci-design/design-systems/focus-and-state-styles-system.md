---
id: computing-software.ux-hci-design.design-systems.focus-and-state-styles-system
name: focus-and-state-styles-system
category: computing-software
field: ux-hci-design
product: design-systems
tags: [focus-ring-token, interactive-states]
level: practitioner
status: docs-checked
description: "Define system-wide focus ring tokens and consistent hover, active, disabled and error state styling."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactive states
- Every item that receives keyboard focus needs a visible focus indicator (WCAG 2.2 SC 2.4.7 Focus Visible, Level AA).
- Visual information required to identify user interface components and states needs a contrast ratio of at least 3:1 against adjacent colours (WCAG 2.2 SC 1.4.11 Non-text Contrast); check the focus ring in each theme.
- Make hover, active and focus states distinct from each other.
- Do not rely on colour alone for error states; add an icon or text.

## Verify
- [ ] Keyboard through every component in each theme; focus ring always visible.
## Checked
2026-11-02. Confirmed against WCAG 2.2 Understanding pages "Focus Visible" and "Non-text Contrast". Removed: the `:focus-visible`, `aria-disabled` and disabled-contrast exemption claims (not compared) and the colour-alone rule's WCAG attribution.
Method: documentation only; no commands were run.
