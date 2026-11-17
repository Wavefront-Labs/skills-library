---
id: computing-software.digital-privacy-hygiene.password-managers.1password-shared-vaults-and-guests
name: 1password-shared-vaults-and-guests
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, 1password-shared-vaults, password-sharing, collections]
level: practitioner
status: draft
description: "Set up 1Password shared vaults with per-person permissions, keep private vaults private, and give guests access to a single vault only."
sources:
  - "https://support.1password.com/create-share-vaults/"
  - "https://support.1password.com/guests/"
  - "https://support.1password.com/family-organizer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# 1Password shared vaults and guests

**Goal:** share exactly the logins that need sharing, with the right edit rights, and nothing more.

## Structure
- **Private vault:** per person, cannot be shared, organisers can't see it.
- **Shared vault (Families):** created by default; visible to all family members.
- Create purpose vaults: `Household`, `Kids`, `Parents' care`, `Business`. Each vault has its own member list.

## Create and share
1. 1Password app or 1Password.com > New Vault, name it.
2. Vault > Manage Access (People): add members.
3. Permissions (business plans offer granular: view, edit, manage; Families: view/edit and "manage vault").
4. Move items in: drag, or item > ... > Move/Copy to vault.

## Guests
On Teams/Business (and some Family configurations), guests are limited accounts with access to a **single**
shared vault. Use for a babysitter, accountant or contractor. Remove when done.

## Revoking
- Remove person from vault (Manage Access). Items they already viewed may be copied: rotate passwords for
  anything sensitive.
- Removing a family member deletes their access to shared vaults; their private vault goes with them.

## Gotchas
- Moving an item out of a shared vault doesn't erase history others saw.
- Don't put your own email or bank in the default Shared vault by accident; check the vault selector when
  saving new items.
