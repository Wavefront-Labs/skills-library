---
id: computing-software.web-development.web-accessibility.on-focus-on-input-change-of-context
name: on-focus-on-input-change-of-context
category: computing-software
field: web-development
product: web-accessibility
tags: [readable, predictable, on-input, change-of-context, on-focus, wcag-3-2-1, wcag-3-2-2, auto-submit, select-navigation]
level: practitioner
status: docs-checked
description: "Meeting WCAG 3.2.1 and 3.2.2: no context changes on focus or input - auto-submitting selects, auto-advancing fields, popups and focus jumps - and acceptable alternatives."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/on-focus.html
  - https://www.w3.org/WAI/WCAG22/Understanding/on-input.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On focus / on input: no unexpected change of context

**Goal:** moving focus or changing a value never navigates, submits, opens windows or moves focus somewhere unexpected.

## 1. What is a "change of context"
New page/window, focus moved, content that changes the meaning of the page (major re-layout), form submitted. Not: showing an inline hint, expanding a section the user requested, filtering results in place (content change, not context change - but announce it).

## 2. Failures and fixes
| Failure | Fix |
|---|---|
| `<select onchange="location = this.value">` (language/country jump menu) | Add a "Go" button, or make it a list of links / disclosure menu |
| Auto-advance to next field after N characters (OTP, card number, phone parts) | Single field accepting the whole value, or warn users beforehand; never auto-advance on focus |
| Form submits when the last field changes | Explicit submit button |
| Popup/modal opens on focus | Open on activation (click/Enter) |
| Focusing a field moves focus elsewhere or triggers navigation | Remove |
| Radio button change reloads the page | Update in place without moving focus, or require a button |

3.2.1 On Focus (A): focus alone never changes context. 3.2.2 On Input (A): changing a setting doesn't, unless the user was warned before (e.g. text above: "Selecting a country reloads the page").

## 3. Live filtering is OK if done right
Checkbox filters that update results in place are fine: keep focus on the control, announce the new count with a polite live region ("24 results"), and don't scroll the page.

## 4. Keyboard specifics
The Understanding page for 3.2.2 treats changing the selected option in a list control as changing a setting, so `onchange` handlers that navigate or submit are the classic failure; test by arrowing through the options with the keyboard.

## Verify
- [ ] Tab through every control: nothing navigates, submits or pops up.
- [ ] Arrow through select options: no navigation.
- [ ] Any control that changes context has prior warning or requires explicit submission.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text: 3.2.1 On Focus and 3.2.2 On Input are Level A; 3.2.2 allows a change of context only if the user was advised of the behaviour before using the component; the Understanding page counts changing the selected option in a list control as changing a setting. Removed the unconfirmed Windows arrow-key behaviour claim.

Method: documentation only; no commands were run.
