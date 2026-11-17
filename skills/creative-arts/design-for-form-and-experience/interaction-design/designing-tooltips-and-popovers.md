---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-tooltips-and-popovers
name: designing-tooltips-and-popovers
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [tooltip, popover, toggletip, contextual-help, hover-help, overlays, aria-describedby]
level: practitioner
status: draft
description: "Design tooltips and popovers: short supplemental text only, trigger on hover and focus, dismissible and hoverable per WCAG 1.4.13, toggletips for rich content, no essential info."
sources:
  - "W3C WCAG 2.2 SC 1.4.13 Content on Hover or Focus (w3.org/TR/WCAG22/#content-on-hover-or-focus)"
  - "W3C WAI-ARIA Authoring Practices - Tooltip Pattern (w3.org/WAI/ARIA/apg/patterns/tooltip)"
  - "Nielsen Norman Group - Tooltip Guidelines (nngroup.com/articles/tooltip-guidelines)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tooltips and popovers

**Goal:** optional, brief help that never blocks essential tasks.

## Choose the right pattern
- **Tooltip:** a short label or hint (1 line, under about 80 characters) for an icon button or truncated text; plain text only; appears on hover and **keyboard focus**; not on touch (so never the only place for needed information).
- **Toggletip / info button:** an "i" or "?" button that opens a small text bubble on click or tap; for brief explanations (Material 3 "rich tooltip"); accessible on touch.
- **Popover:** richer, interactive content (a preview, a short form, menu); opens on click, can contain links and buttons; behaves like a non-modal dialog.
- For long or critical explanations use inline text, a help panel or a dialog.

## Behaviour (WCAG 1.4.13)
1. **Dismissible:** Esc closes without moving focus or pointer.
2. **Hoverable:** the pointer can move onto the tooltip without it vanishing.
3. **Persistent:** it stays until hover or focus leaves or the user dismisses it.
Delay open by about 300-500 ms; close about 100 ms after leaving; position smartly with collision handling (flip away from edges), arrow pointing to trigger.

## Accessibility
- Tooltip: `role="tooltip"` with the trigger referencing it via `aria-describedby`; icon-only buttons still need an accessible name (`aria-label`) as the tooltip is a description.
- Popover: `aria-expanded` on the trigger, focus moves into the popover if it contains controls and returns on close; the HTML `popover` attribute and CSS anchor positioning help.
- Never hide required form instructions in a tooltip.

## Verify
- [ ] Tooltip content short, text-only, not essential; reachable by keyboard.
- [ ] Meets dismissible, hoverable, persistent rules.
- [ ] Touch alternative exists (toggletip).
