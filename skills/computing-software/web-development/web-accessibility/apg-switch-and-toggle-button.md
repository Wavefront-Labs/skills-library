---
id: computing-software.web-development.web-accessibility.apg-switch-and-toggle-button
name: apg-switch-and-toggle-button
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-switch, toggle-button, aria-pressed, aria-checked, apg-patterns, wcag-4-1-2]
level: practitioner
status: docs-checked
description: "Building on/off controls: role=switch vs checkbox vs aria-pressed toggle buttons, native switch inputs, labels that do not change, keyboard support and immediate effect."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/switch/
  - https://www.w3.org/WAI/ARIA/apg/patterns/button/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/checkbox
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switch and toggle button patterns

## 1. Choose the control
| Control | Use when | Announced |
|---|---|---|
| Checkbox | option submitted with a form | "checkbox, checked" |
| Switch | setting takes effect immediately (Wi-Fi, dark mode, notifications) | "switch, on" |
| Toggle button (`aria-pressed`) | toolbar actions with a pressed state (Bold, Mute) | "toggle button, pressed" |

## 2. Switch
```html
<button type="button" role="switch" aria-checked="false" id="notif">Email notifications</button>
```
```js
notif.addEventListener("click", () => {
  const on = notif.getAttribute("aria-checked") !== "true";
  notif.setAttribute("aria-checked", String(on));
  savePreference(on);
});
```
- `<button>` gives focus, Enter and Space for free (APG: Space toggles a switch; Enter is optional).
- Or start from a checkbox: `<input type="checkbox" role="switch">` (keeps form semantics; use the `checked` attribute, not `aria-checked`). The `switch` attribute on `<input type="checkbox">` marks it as an on/off switch; check MDN's compatibility table for browser support.
- The label names the setting and never changes ("Email notifications", not "Turn on notifications" -> "Turn off notifications"); the APG calls this critical for both switches and toggle buttons.
- Style from state: `[role="switch"][aria-checked="true"] { ... }` so visuals cannot drift from semantics.

## 3. Toggle button
```html
<button type="button" aria-pressed="false">Mute</button>
```
Same rule: the label stays "Mute"; the pressed state carries the meaning. Changing the label instead (Mute <-> Unmute) is a different pattern and must not be combined with `aria-pressed`.

## 4. Gotchas
- If the change can fail (network), revert the state and announce the error (status message).
- Do not use a switch for actions that need confirmation or a save button.
- Ensure the thumb/track contrast meets 3:1 in both states (1.4.11) and state is not conveyed by colour alone.

## Verify
- [ ] NVDA/VoiceOver announce "switch, off" then "on" after Space; the label text is constant.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG switch and button patterns: role switch with aria-checked true/false (checked attribute for input checkboxes), Space toggles and Enter optional, the label must not change with state, toggle buttons use aria-pressed. MDN confirms the checkbox switch attribute. Removed the unconfirmed Safari version and the aria-hidden On/Off advice. WCAG 1.4.11 non-text contrast is 3:1.

Method: documentation only; no commands were run.
