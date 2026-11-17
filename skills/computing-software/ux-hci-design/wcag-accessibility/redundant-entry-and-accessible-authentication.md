---
id: computing-software.ux-hci-design.wcag-accessibility.redundant-entry-and-accessible-authentication
name: redundant-entry-and-accessible-authentication
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [redundant-entry, accessible-authentication]
level: practitioner
status: docs-checked
description: "Prefill previously entered data (3.3.7) and avoid cognitive function tests at login (3.3.8)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html
  - https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 3.3.7 Redundant Entry (A) and 3.3.8 Accessible Authentication (Minimum) (AA)
- 3.3.7: information previously entered by or provided to the user that is required to be entered again in the same process is auto-populated or available for the user to select.
- 3.3.8: a cognitive function test (such as remembering a password or solving a puzzle) must not be required for any step of authentication unless there is another authentication method that is not a cognitive function test, or a mechanism to assist the user (for example password managers or copy and paste), or the test is to recognize objects, or to identify non-text content the user provided to the site.
- Do not actively block user agents or password managers from filling the fields or pasting.

## Verify
- [ ] A password manager can fill and submit the login form.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 3.3.7 Redundant Entry (Level A) and Understanding SC 3.3.8 Accessible Authentication (Minimum) (Level AA): criterion wording, the alternative method, assistance mechanism, object recognition and user-provided content exceptions, password manager and copy-paste support. The pages were searched for these claims rather than read line by line.
- Removed: the "billing same as shipping" example, passkeys and email links, the `autocomplete` instruction, and "new in WCAG 2.2" wording.

Method: documentation only; no commands were run.
