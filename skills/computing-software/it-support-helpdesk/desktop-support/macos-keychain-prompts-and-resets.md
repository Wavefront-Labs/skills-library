---
id: computing-software.it-support-helpdesk.desktop-support.macos-keychain-prompts-and-resets
name: macos-keychain-prompts-and-resets
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, keychain, macos, login-keychain, password-sync, platform-sso]
level: practitioner
status: draft
description: "Stop repeated macOS keychain prompts: why the login keychain falls out of sync after admin password resets, how to update or reset it, and how to avoid it with password sync."
sources:
  - "https://support.apple.com/guide/keychain-access/if-you-need-to-update-your-keychain-password-kyca2429/mac"
  - "https://support.apple.com/guide/keychain-access/reset-your-default-keychain-kyca1136/mac"
  - "https://ss64.com/mac/security.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-keychain-prompts-and-resets

## Why it happens
The login keychain is encrypted with the user's macOS password. When a user changes the
password themselves, the keychain follows. When an admin resets it (or a directory/IdP
password changes without sync), the keychain keeps the old password and macOS keeps
asking "...wants to use the login keychain".

## Fix with the old password
Keychain Access > select **login** > Edit > Change Password for Keychain "login" (or enter
the old password when the prompt offers "Update Keychain Password"). Nothing is lost.

## Fix without the old password
1. Keychain Access > Settings (or Preferences) > **Reset Default Keychains**.
2. macOS creates a new login keychain; the old one is renamed (kept in
   `~/Library/Keychains`), so items can be recovered later if the old password turns up.
3. The user re-enters Wi-Fi, mail and app passwords as prompted. iCloud Keychain items
   sync back if they use it.

## Command line
```bash
security list-keychains
security unlock-keychain ~/Library/Keychains/login.keychain-db
security show-keychain-info ~/Library/Keychains/login.keychain-db
```

## App-specific prompts
"<App> wants to access key ... in your keychain" after an app update: enter the password
and choose Always Allow. Repeated prompts for the same app suggest a corrupt item; delete
that item in Keychain Access and let the app recreate it.

## Prevent it
- With Entra ID Platform SSO or Jamf Connect password sync, the local password follows
  the IdP password and the keychain stays in step.
- Teach users to change their password on the Mac, not only on the web portal, when no
  sync tool exists.

## Gotchas
- Local Items / iCloud keychain is separate from the login keychain and has its own
  recovery path.
- Resetting removes saved certificates/private keys in the login keychain; MDM-issued
  identities may need the profile re-pushed.

## Verify
After a restart and login, no keychain prompts appear and Wi-Fi/mail reconnect without
asking.
