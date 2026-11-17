---
id: computing-software.digital-privacy-hygiene.password-managers.disabling-browser-password-saving
name: disabling-browser-password-saving
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, disable-browser-password-saving, remove-browser-saved-passwords, chrome, firefox, edge, safari, infostealer, group-policy, migration]
level: intro
status: draft
description: "After moving to a dedicated password manager, stop browsers offering to save passwords and purge what they already stored, so infostealers find nothing."
sources:
  - "https://support.google.com/chrome/answer/95606"
  - "https://support.mozilla.org/en-US/kb/password-manager-remember-delete-edit-logins"
  - "https://support.microsoft.com/en-us/microsoft-edge/manage-passwords-in-microsoft-edge"
  - "https://chromeenterprise.google/policies/#PasswordManagerEnabled"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disabling browser password saving and purging old passwords

**Goal:** one source of truth for credentials. Two competing save prompts confuse
people, and browser stores are the first thing commodity infostealer malware grabs.

## 1. Import first, then purge
Export or import the browser's passwords into the manager (handle CSVs as in
`computing-software.digital-privacy-hygiene.password-managers.migrating-vaults-between-password-managers`),
verify counts, then delete.

## 2. Turn off the offer to save
| Browser | Setting |
|---|---|
| Chrome | `chrome://password-manager/settings` > Offer to save passwords and passkeys **off**; Sign in automatically off |
| Edge | Settings > Profiles > Passwords > Offer to save passwords **off** |
| Firefox | Settings > Privacy & Security > Passwords > Ask to save passwords **off** |
| Safari (macOS) | Settings > AutoFill > uncheck User names and passwords |
| Brave | `brave://settings/autofill` > Password Manager > Offer to save off |

Also turn off address and card autofill if those now live in the manager.

## 3. Delete what's stored
- Chrome/Edge/Brave: Clear browsing data > Advanced > **Passwords and other sign-in
  data**, time range All time. Repeat on every synced device or it may resync.
- Firefox: `about:logins` > ... menu > Remove all passwords.
- Safari: Passwords app / Keychain; only delete if you are leaving iCloud Keychain.

## 4. Managed machines
Policy `PasswordManagerEnabled = false` (Chrome/Edge) or Firefox `PasswordManagerEnabled`
in `policies.json` enforces it for a family PC.

## Gotchas
- Synced profiles restore deleted passwords from the cloud copy if another device
  still has them and syncs first; delete while all devices are online and synced.
- Clearing "passwords" in some browsers also removes passkeys stored in the browser.

## Verify
- [ ] `chrome://password-manager/passwords` (or equivalent) shows zero entries on all devices.
- [ ] Logging into a new site prompts only the dedicated manager.
