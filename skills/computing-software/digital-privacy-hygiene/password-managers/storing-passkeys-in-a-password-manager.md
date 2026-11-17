---
id: computing-software.digital-privacy-hygiene.password-managers.storing-passkeys-in-a-password-manager
name: storing-passkeys-in-a-password-manager
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, passkeys, bitwarden, webauthn]
level: practitioner
status: docs-checked
description: "Store and use passkeys in Bitwarden so they are not tied to one OS keychain: enable the setting, one passkey per login item, platform limits."
sources:
  - "https://bitwarden.com/help/storing-passkeys/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storing passkeys in a password manager

**Goal:** use passkeys (phishing-resistant, nothing to remember) without being locked into one OS vendor's
keychain. Steps below follow Bitwarden; other managers differ, so read their help pages.

## Setup
1. In the Bitwarden browser extension, open Settings > Notifications and make sure **Ask to save and use
   passkeys** is checked. It must also be on before you can sign in with a stored passkey.
2. On the site's security page, create a passkey. Bitwarden offers to save it; accept.

## Management
- Only one passkey can be saved per login item. To keep a second passkey for the same service (for example a
  backup), overwrite the existing one or create a separate login item for it.
- Remove a passkey from a vault item by editing the item and deleting the Passkey field. Also remove it in the
  site's own security settings; Bitwarden's page does not say the site's copy is removed for you.
- Keep a password or other backup sign-in method until you are confident the passkey works.

## Platform limits (from Bitwarden's page)
- iOS: Bitwarden passkeys need iOS 17.0 or later.
- Android: stored passkeys work only as a primary login credential, not as passkey-based 2FA.
- Windows desktop app: must be the appx or Microsoft Store distribution.
- Bitwarden will not save a passkey used to log in to a Bitwarden account, and the extension will not offer
  passkeys for excluded domains.

## Verify
- [ ] Sign in on a second device with the synced passkey.
- [ ] The site's security page lists the passkey.

## Checked
2026-11-01. Confirmed against bitwarden.com/help/storing-passkeys/: the Notifications setting name, one passkey per
login item, deleting the Passkey field, and the iOS, Android, Windows and domain limits. Removed as unconfirmed:
1Password and KeePassXC steps and version, NIST syncable-authenticator wording, attestation refusals, extension
troubleshooting, and the other source URLs (not read).
Method: documentation only; no commands were run.
