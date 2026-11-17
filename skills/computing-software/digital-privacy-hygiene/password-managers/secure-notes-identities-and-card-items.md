---
id: computing-software.digital-privacy-hygiene.password-managers.secure-notes-identities-and-card-items
name: secure-notes-identities-and-card-items
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, secure-notes, vault-items, identity-items, card-items, wifi-passwords, software-licenses, document-numbers, crypto-seed]
level: intro
status: draft
description: "Use secure notes, identity and card items for the non-login secrets (Wi-Fi keys, licences, passport numbers, door codes) and know what should stay out of an online vault."
sources:
  - "https://bitwarden.com/help/managing-items/"
  - "https://support.1password.com/item-categories/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure notes, identities and card items

**Goal:** stop sensitive non-password information living in phone notes, email
drafts and photos, and move it into the encrypted vault in a findable form.

## What goes where
| Secret | Item type | Tips |
|---|---|---|
| Wi-Fi network password | Secure note / 1Password "Wireless Router" | Include SSID, admin URL; share with household |
| Software licence keys | Secure note / "Software License" | Include purchase email, order number |
| Passport, driving licence, national ID numbers | Identity (or document category) | Expiry dates trigger renewal reminders in some apps |
| Bank card for online shopping | Card | Store only cards you use online; CVV storage is a trade-off |
| Alarm, safe, gate codes | Secure note | Tag `home` |
| Server / router admin creds | Login with custom fields | Port, IP, notes |
| Medical / insurance numbers | Identity custom fields or secure note | Needed by family in emergencies; share via emergency access |

## Structure for findability
- Titles that read in search: `Wi-Fi - Home`, `Licence - Office 2021`, `ID - Passport (Alex)`.
- Use folders/tags consistently (see
  `computing-software.digital-privacy-hygiene.password-managers.organizing-a-large-vault`).
- Mark card/identity items to **not** autofill everywhere, or restrict to known shops.

## What not to put in an online vault
- **Cryptocurrency seed phrases** for meaningful sums: a vault theft becomes an instant,
  irreversible loss. Keep on paper or metal, offline.
- The vault's own master password and its 2FA recovery code.
- Large files; use an encrypted container instead (see the file encryption skills).

## Gotchas
- Secure notes are full-text searchable only after unlock; that's fine, but avoid
  putting secrets in item **titles**, which some managers show in more places
  (and older providers stored them less protected).
- Photographs of IDs as attachments are convenient and also a full identity-theft kit;
  keep them only if you really need them.

## Verify
- [ ] Phone notes app and email drafts searched for "password", "PIN", "code"; anything
      found moved and deleted.
