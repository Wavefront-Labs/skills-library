---
id: computing-software.ux-hci-design.wcag-accessibility.text-spacing-and-hover-content
name: text-spacing-and-hover-content
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [text-spacing-wcag, content-on-hover-focus]
level: practitioner
status: docs-checked
description: "Survive user text-spacing overrides (1.4.12) and make hover or focus popups dismissible, hoverable, persistent (1.4.13)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
  - https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1.4.12 Text Spacing (AA)
No loss of content or functionality when the user sets: line height to at least 1.5 times the font size, spacing following paragraphs to at least 2 times, letter spacing to at least 0.12 times, word spacing to at least 0.16 times. The user applies these with a user stylesheet, bookmarklet, extension or application. Clipped or overlapped content when spacing is adjusted is a documented failure.

# 1.4.13 Content on Hover or Focus (AA)
Content that appears on pointer hover or keyboard focus must be **dismissible** (for example the Escape key clears a tooltip without moving the pointer), **hoverable** (the pointer can move onto the new content) and **persistent** (it stays visible until the trigger is removed, the user dismisses it, or its information is no longer valid).

## Verify
- [ ] Apply the spacing values; text is not clipped. Tooltip stays when pointer moves onto it.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.4.12 Text Spacing and Understanding SC 1.4.13 Content on Hover or Focus (both Level AA): the four spacing values, user stylesheet/bookmarklet, the clipped-content failure, the dismissible/hoverable/persistent conditions and the Escape example. Pages were searched for these claims rather than read line by line.
- Removed: the advice on fixed-height containers with `overflow: hidden` (not stated on the pages).

Method: documentation only; no commands were run.
