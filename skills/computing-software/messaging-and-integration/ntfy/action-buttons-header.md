---
id: computing-software.messaging-and-integration.ntfy.action-buttons-header
name: action-buttons-header
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, actions, action-buttons, x-actions, view]
level: practitioner
status: docs-checked
description: "Add up to three action buttons to an ntfy notification using the X-Actions header format, with view and copy actions."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Action buttons: header format

Up to three actions per notification. Header `X-Actions` (aliases `Actions`, `Action`). Separate actions with `;` and key/value pairs with `,`. Quote values with `"` or `'` if they contain commas or semicolons.

Action types: `view`, `broadcast` (Android only), `http`, `copy`.

## Short formats

```
view, <label>, <url>[, clear=true]
copy, <label>, <value>[, clear=true]
```

- `view` opens a website or app; `clear` defaults to `false`.
- `copy` puts a value on the clipboard. The button shows only in the web app and Android app, not in desktop browser notifications.

## Example

```
curl -d "You left the house. Turn down the A/C?" \
  -H "Actions: view, Open portal, https://home.nest.com/, clear=true" \
  ntfy.sh/myhome
```

## Gotchas

- `clear=true` dismisses the notification after the button is tapped.
- In the web app, view and HTTP actions and images display only in Chrome, Edge and Opera.
- For `http` and `broadcast` actions see the action-http-broadcast skill.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Action buttons) and the web app page: three-action limit, header aliases, separators and quoting, short formats, `clear` default false, copy-button visibility, Chrome/Edge/Opera restriction. Removed: the Verify step.
Method: documentation only; no commands were run.
