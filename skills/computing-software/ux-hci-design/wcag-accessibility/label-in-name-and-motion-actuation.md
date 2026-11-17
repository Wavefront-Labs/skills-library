---
id: computing-software.ux-hci-design.wcag-accessibility.label-in-name-and-motion-actuation
name: label-in-name-and-motion-actuation
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [label-in-name, motion-actuation]
level: practitioner
status: docs-checked
description: "Ensure accessible names contain the visible label text (2.5.3) and motion-triggered functions have alternatives (2.5.4)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
  - https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 2.5.3 Label in Name (A) and 2.5.4 Motion Actuation (A)
- Voice-control users say the visible label. Accessible name must contain that text, ideally at the start.
  Bad: visible "Search", `aria-label="Find products"`. Good: `aria-label="Search products"`.
- Functions triggered by device motion (shaking, tilting) need an equivalent user interface control and a way to disable the motion response.

## Verify
- [ ] Voice control ("click Search") activates the control.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 2.5.3 Label in Name (Level A) and Understanding SC 2.5.4 Motion Actuation (Level A): voice users, label text contained in the name, start of the name preferred, motion with UI equivalent and a way to disable. Pages were searched for these claims rather than read line by line.
- Removed: the "shake-to-undo" example as a requirement.

Method: documentation only; no commands were run.
