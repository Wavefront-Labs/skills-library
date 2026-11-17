---
id: computing-software.digital-privacy-hygiene.password-managers.autofill-keyboard-shortcuts
name: autofill-keyboard-shortcuts
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, autofill-keyboard-shortcut, autofill, keepassxc-auto-type]
level: practitioner
status: draft
description: "Use password manager keyboard shortcuts to fill, generate and open the vault, rebind them in the browser, and fill manually when autofill is off."
sources:
  - "https://bitwarden.com/help/keyboard-shortcuts/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_auto_type"
  - "https://support.mozilla.org/kb/manage-extension-shortcuts-firefox"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Autofill keyboard shortcuts

**Goal:** fill deliberately with a keystroke instead of auto-filling on page load, which is both faster and
safer.

## Bitwarden browser extension defaults
| Action | Windows/Linux | macOS |
|---|---|---|
| Autofill last-used login for this site | Ctrl+Shift+L (repeat to cycle) | Cmd+Shift+L |
| Generate and copy password | Ctrl+Shift+9 | Cmd+Shift+9 |
| Open the popup | Ctrl+Shift+Y | Cmd+Shift+Y |

## KeePassXC
- Global Auto-Type: set in Settings > Auto-Type (commonly Ctrl+Alt+A); it matches the active window title to
  entry Window associations or titles.
- KeePassXC-Browser: fill username+password with Ctrl+Shift+U, password only Ctrl+Shift+P (browser-configurable).

## Rebinding
- Chromium browsers: `chrome://extensions/shortcuts` (Edge: `edge://extensions/shortcuts`).
- Firefox: about:addons > gear icon > Manage Extension Shortcuts.
- Resolve clashes: Ctrl+Shift+L is used by some apps; pick an unused chord.

## Manual-fill workflow (autofill off or failing)
1. Click into the username field.
2. Press the fill shortcut, or open the popup and click the item.
3. If the popup offers **no** matching item, stop: check the URL before searching the vault manually.

## Gotchas
- Shortcuts fill the item matched by URI; a "no match" is a phishing signal, not a nuisance.
- macOS may need Accessibility permission for KeePassXC global auto-type (System Settings > Privacy &
  Security > Accessibility).
