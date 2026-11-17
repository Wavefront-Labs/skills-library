---
id: computing-software.digital-privacy-hygiene.two-factor-auth.sharing-passkeys-with-family-groups
name: sharing-passkeys-with-family-groups
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, shared-passkeys, passkeys, family-sharing, shared-passwords]
level: practitioner
status: draft
description: "Share passkeys and passwords for household accounts through Apple shared groups or password manager shared vaults, and remove access cleanly when needed."
sources:
  - "https://support.apple.com/guide/passwords/welcome/mac"
  - "https://bitwarden.com/help/storing-passkeys/"
  - "https://support.1password.com/save-use-passkeys/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sharing passkeys with family groups

**Goal:** a shared household login (streaming, utilities, school portal) that several people can use with a passkey,
without texting a password around.

## Options
| Tool | How | Notes |
|---|---|---|
| Apple Passwords (iOS 17+/macOS 14+) | Passwords > New Shared Group, add contacts, move the passkey/password in | Members need Apple devices and to be in your contacts |
| 1Password | Save the passkey in a shared vault (family plan) | Works on any OS with 1Password installed |
| Bitwarden | Passkey stored on a login item in an organisation collection | Family organisation; members need collection access |
| Google Password Manager | Share passwords with your Google family group | Check current passkey sharing support before relying on it |

## Steps (Apple)
1. Settings > Passwords (or the Passwords app) > **New Shared Group**, name it, add people.
2. Choose which saved items to move into it; edit one entry to confirm it lists the group.
3. Each member sees the group in their Passwords app; anyone in the group can edit or delete items, so share only
   with people you trust to edit.

## Good practice
- Share one item per account, not your whole vault; keep personal accounts (email, bank) out of shared groups.
- Prefer accounts that support multiple user profiles or family plans instead of a shared login where they exist.
- Note the shared group in your digital legacy plan.

## Removing someone
Remove them from the group (or shared vault). Items they already used are no longer synced to them, but they may
have saved a copy or been signed in: sign out all sessions on the account and rotate the password or create a new
passkey and delete the old one at the site.

## Verify
Have a member sign in with the shared passkey on their own device. After removal, confirm the item disappears from
their app and that site sessions were revoked.
