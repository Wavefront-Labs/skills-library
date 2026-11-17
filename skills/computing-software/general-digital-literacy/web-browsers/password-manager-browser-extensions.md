---
id: computing-software.general-digital-literacy.web-browsers.password-manager-browser-extensions
name: password-manager-browser-extensions
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-extensions, password-manager-extension, autofill, bitwarden]
level: intro
status: docs-checked
description: "Install and use a password manager's browser extension (Bitwarden example), keep the browser's own manager from clashing, and autofill on click rather than on page load."
sources:
  - https://bitwarden.com/help/getting-started-browserext/
  - https://bitwarden.com/help/auto-fill-browser/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Password manager extensions

## Install
- Bitwarden's help: download the browser extension from your browser's marketplace or app store, or from the Bitwarden Downloads page. The Safari extension is packaged with the desktop app from the Mac App Store.
- Use the vendor's own link to the store page, and check the developer name matches the vendor.

## Avoid two managers fighting
Bitwarden recommends deactivating the browser's built-in password manager so it does not interfere with autofill, and making Bitwarden the default password manager. Import existing browser passwords into the manager first, and delete any exported file afterwards.

## Autofill
- Fill from the inline menu in a field, the toolbar icon, the context menu, or the keyboard shortcut (Bitwarden's default for login items is Ctrl/Cmd + Shift + L).
- **Autofill on page load** is off by default in Bitwarden. Its docs warn that while generally safe, compromised or untrusted sites could exploit it; leave it off unless you need it.
- Bitwarden's extension will not autofill on page load in untrusted iframes and warns before filling on an HTTP site when HTTPS is expected.

## Verify
- [ ] The manager fills your login on the correct site only, and the browser's own save-password prompt is off.

## Checked
Date: 2026-10-27. Documentation: Bitwarden help "Password Manager Browser Extensions" and "Autofill From Browser Extensions", read in October 2026. Confirmed: install sources, default shortcut, page-load default and warning, iframe and HTTP behaviour, advice to deactivate the browser's manager. Other vendors differ; check their own help. Removed as unconfirmed: 1Password and Proton Pass shortcuts, iCloud Passwords for Windows, per-browser menu paths for turning off built-in managers, vault timeout advice, and phishing-detection claims.
Method: documentation only; no commands were run.
