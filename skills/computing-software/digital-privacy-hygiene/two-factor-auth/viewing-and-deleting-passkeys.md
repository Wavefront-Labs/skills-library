---
id: computing-software.digital-privacy-hygiene.two-factor-auth.viewing-and-deleting-passkeys
name: viewing-and-deleting-passkeys
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, passkey-management, platform-passkeys, passkey-inventory]
level: practitioner
status: draft
description: "Find, view and delete passkeys in iCloud Passwords, Google Password Manager, Windows, password managers and on the website side as well."
sources:
  - "https://support.apple.com/guide/iphone/use-passkeys-iphf538ea8d0/ios"
  - "https://support.google.com/accounts/answer/13548313"
  - "https://support.microsoft.com/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Viewing and deleting passkeys

**Goal:** remove stale or duplicate passkeys cleanly, on both the provider and the site.

## Where passkeys live
| Provider | Path |
|---|---|
| Apple | Passwords app (iOS 18 / macOS 15) > Passkeys; older: Settings > Passwords |
| Google Password Manager | passwords.google.com or Chrome > Password Manager; passkeys show on the site's entry |
| Windows Hello | Settings > Accounts > Passkeys (search, delete) |
| Bitwarden / 1Password | Login item shows the passkey field; delete the passkey from the item |
| Security key | `ykman fido credentials list` / `ykman fido credentials delete <id>` |

## Delete on both sides
1. Site: Security settings > Passkeys > remove the one you're retiring (names often show provider/device).
2. Provider: delete the passkey entry.
Deleting only at the provider leaves the site listing a credential nobody holds; deleting only at the site leaves
a dead entry that will be offered and fail.

## When to delete
- Old phone or departed provider.
- Duplicates created by accident (same site in two providers).
- Account closure.

## Gotchas
- Don't delete your last passkey on an account without another sign-in method.
- Apple and Google sync deletions to all devices in the account; a delete on one is a delete everywhere.
