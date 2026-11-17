---
id: computing-software.digital-privacy-hygiene.password-managers.choosing-which-provider-saves-a-passkey
name: choosing-which-provider-saves-a-passkey
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, passkey-provider-selection, passkey-storage-in-password-manager, passkeys]
level: practitioner
status: draft
description: "Control whether a new passkey lands in your password manager, the OS keychain or a security key when browser, OS and extension all offer to save it."
sources:
  - "https://bitwarden.com/help/storing-passkeys/"
  - "https://support.1password.com/save-use-passkeys/"
  - "https://developers.google.com/identity/passkeys/supported-environments"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Choosing which provider saves a passkey

**Goal:** every passkey ends up where you intended, so you can find, back up and migrate it.

## Who intercepts the request
When a site calls WebAuthn `create()`:
1. A password manager **extension** with passkey support (Bitwarden, 1Password) intercepts first.
2. Otherwise the browser/OS dialog appears: Google Password Manager (Chrome), iCloud Keychain (Safari/macOS),
   Windows Hello, a phone via QR, or a USB security key.

## Steer it
- **Bitwarden:** Settings > Notifications > "Ask to save and use passkeys" on/off. In the save prompt choose
  "Use your device or hardware key" to hand off to the OS dialog (e.g. for a YubiKey).
- **1Password:** the save prompt has "Use a security key or another device" to fall through.
- **OS level:** set your preferred provider (iOS AutoFill & Passwords, Android Credential Manager preferred
  service) so native apps also use it.
- **Security key on purpose:** for high-value accounts register a hardware key **in addition**, via the
  fall-through option.

## Policy that keeps you sane
- One primary synced provider for everyday passkeys.
- Hardware keys only for accounts you deliberately protect that way (email, password manager, registrar).
- Record in the vault item notes where each passkey lives if it isn't in the vault.

## Gotchas
- Sites may store one passkey per provider; creating a second in another provider adds a separate credential.
  Name them in the site's security settings.
- Chrome profile sync can save to Google Password Manager silently when the extension is locked; unlock the
  manager before creating a passkey.
