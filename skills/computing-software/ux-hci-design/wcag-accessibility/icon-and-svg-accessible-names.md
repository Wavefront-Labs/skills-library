---
id: computing-software.ux-hci-design.wcag-accessibility.icon-and-svg-accessible-names
name: icon-and-svg-accessible-names
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [icon-accessible-name, svg-accessibility]
level: practitioner
status: draft
description: "Give icon-only controls a programmatic name via text, aria-label or visually hidden text, and hide decorative icons."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Icon names
```html
<button type="button" aria-label="Close dialog"><svg aria-hidden="true" focusable="false">...</svg></button>
<button type="button"><svg aria-hidden="true"></svg><span class="visually-hidden">Delete</span></button>
```
- Icon font glyphs: hide from AT (`aria-hidden="true"`) and provide a text name.
- The name must include the visible label text if there is one (SC 2.5.3 Label in Name).
- Do not use `title` as the only name.

## Verify
- [ ] Accessibility tree (browser DevTools) shows a name for each icon button.
