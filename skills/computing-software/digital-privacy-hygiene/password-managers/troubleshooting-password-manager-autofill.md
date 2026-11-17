---
id: computing-software.digital-privacy-hygiene.password-managers.troubleshooting-password-manager-autofill
name: troubleshooting-password-manager-autofill
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, autofill-troubleshooting, autofill, mobile-autofill-service]
level: practitioner
status: draft
description: "Diagnose password manager autofill that doesn't trigger: URI mismatch, unusual forms, extension conflicts, mobile autofill service and app blocks."
sources:
  - "https://bitwarden.com/help/auto-fill-browser/"
  - "https://bitwarden.com/help/auto-fill-android-troubleshooting/"
  - "https://support.1password.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Troubleshooting autofill

**Goal:** get fill working without loosening security settings blindly.

## Desktop browser checklist
1. **Is the item matched?** Open the popup: if the item isn't listed under "Autofill suggestions", the saved
   URI doesn't match. Compare the item URI with the address bar (http vs https, subdomain, port).
2. **Two-step login pages:** username on page 1, password on page 2. Fill twice, or fill username then use the
   shortcut again.
3. **Shadow DOM / custom fields:** some sites build fields the extension can't see. Use the popup's "Copy
   password" with clipboard clearing, or add a custom field named after the input's `name`/`id`.
4. **Competing managers:** the browser's own manager or another extension may grab the field. Disable built-in
   password saving and other managers.
5. **Extension permissions:** Firefox/Safari may need "Always allow on all websites" for the extension.
6. Update the extension and browser; reload the page after unlocking.

## Android
- Settings > Passwords & accounts (or System > Autofill service): your manager selected.
- Inline suggestions need a supporting keyboard (Gboard, Samsung).
- Some browsers (Firefox, older Chrome) need accessibility-based fill or "Autofill using another service" in
  the browser's settings (Chrome: Settings > Autofill services).

## iOS
Settings > General > AutoFill & Passwords: enable the manager; tap the key icon/QuickType bar.

## Apps that refuse
Banking apps often set fields as non-autofillable. Copy/paste with clipboard timeout is the fallback; don't
switch off clipboard clearing.

## When not to "fix" it
If a familiar site suddenly stops matching, read the URL: a domain change can be a phishing page.
