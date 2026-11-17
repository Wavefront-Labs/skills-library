---
id: computing-software.digital-privacy-hygiene.password-managers.forgotten-master-password-options
name: forgotten-master-password-options
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, forgotten-master-password, vault-recovery, master-password]
level: practitioner
status: draft
description: "What you can still do after forgetting a master password in Bitwarden, 1Password or KeePassXC: unlocked sessions, emergency access, recovery, deletion."
sources:
  - "https://bitwarden.com/help/forgot-master-password/"
  - "https://support.1password.com/forgot-account-password/"
  - "https://keepassxc.org/docs/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Forgotten master password: options

**Goal:** salvage as much as possible before giving up. Zero-knowledge means the provider cannot reset it.

## First: stop and check for a live session
Do **not** log out of anything. Any device where the vault is still unlocked, or unlocks with PIN/biometrics,
is your lifeline.
- Bitwarden: if an app unlocks with PIN/biometrics, open each critical item and copy the data out, or export
  (export asks for the master password on most clients; copy items manually if so).
- 1Password: an app unlocked with Touch ID/Windows Hello lets you view items; it may also let you see the
  password if you saved it in the vault (some people do, unintentionally).

## Recovery paths that exist only if set up beforehand
| Manager | Path |
|---|---|
| Bitwarden | Emergency access takeover by a trusted contact (after the wait period); organisation **account recovery** if your org enrolled you |
| 1Password | Family organiser / team admin starts recovery; you get a new Secret Key and set a new password |
| KeePassXC | None. Try remembered variants with your own script against a copy of the file; there is no back door |

## Memory-jogging that works
- Type candidates on the device where you normally type it; muscle memory beats recall.
- Check paper backups, safe deposit box, sealed envelopes, your will.

## Last resort: start over
- Bitwarden: "Delete account" via the recover-delete page sends a confirmation email; then re-register and
  rebuild from browser-saved passwords and password resets.
- Prioritise: primary email first (reset via recovery phone), then bank, then everything else via "forgot
  password" emails.

## Prevent next time
Emergency kit on paper, a second organiser/emergency contact, and a recurring reminder to type the passphrase.
