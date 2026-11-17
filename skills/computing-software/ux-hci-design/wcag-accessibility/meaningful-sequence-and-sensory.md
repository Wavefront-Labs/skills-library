---
id: computing-software.ux-hci-design.wcag-accessibility.meaningful-sequence-and-sensory
name: meaningful-sequence-and-sensory
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [meaningful-sequence, sensory-characteristics]
level: practitioner
status: docs-checked
description: "Keep a meaningful programmatic reading sequence and avoid instructions relying solely on shape, colour or position."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
  - https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1.3.2 Meaningful Sequence and 1.3.3 Sensory Characteristics (both Level A)
- When the order of content affects its meaning, the correct reading sequence must be programmatically determinable. Positioning information with CSS so that it changes the meaning is a documented failure.
- Instructions must not rely solely on sensory characteristics such as shape, color, size, visual location, orientation or sound.
- Describe controls by name, not just by appearance or location: not "select the green arrow icon in the lower right corner" but name the control and add another cue. Failure F14 is identifying content only by shape or location.

## Verify
- [ ] Disable CSS: content still reads in a sensible order.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.3.2 Meaningful Sequence and Understanding SC 1.3.3 Sensory Characteristics (both Level A): programmatic sequence, CSS positioning failure, the sensory characteristics list, name-not-appearance, F14. Pages were searched for these claims rather than read line by line.
- Removed: the grid/flex/`order` specifics and the tab order link to SC 2.4.3 (not on the cited pages).

Method: documentation only; no commands were run.
