---
id: computing-software.digital-privacy-hygiene.password-managers.password-history-and-item-versions
name: password-history-and-item-versions
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, password-history, vault-items, vault-recovery]
level: practitioner
status: docs-checked
description: "Recover a previous password from a vault item's history or the generator history after a failed password change, and set history retention."
sources:
  - "https://bitwarden.com/help/managing-items/"
  - "https://support.1password.com/item-history/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Password history and item versions

**Goal:** get back the old password when a site's change-password flow fails half way, or when you overwrote the
wrong item.

## Classic failure
You generate a new password, the site errors out, but the vault already saved the new one. The site still has
the old password. Item history saves you where the manager keeps it.

## Bitwarden
- The Vault Items page documents a trash: deleted items stay there for 30 days, then are permanently deleted. In the
  trash you can **Restore** an item or **Permanently delete** it early.
- It does not describe a per-item password history, so do not rely on one: save the new password to the item before
  submitting the site's form (routine below).

## 1Password
- Password history is available for Login and Password items only. Select an item, hover over the password, choose the
  down arrow > **View password history**, then **Reveal** or **Copy** an earlier password. On 1Password.com the same
  menu offers Reveal or Show in Large Type.
- Whole-item versions: select the item's **Last edited** date at the bottom of its details > **View previous versions**
  > choose a version > **Restore Item**. Other versions stay in the history after a restore.
- 1Password saves previous versions every time you change an item. In a family account only members with the Allow
  Editing permission can restore items in that vault.

## KeePassXC
- Each time you change an entry, KeePassXC keeps a copy of the unmodified entry in its **History** tab. Choose Show
  (read-only), **Restore**, Delete or Delete All. Restoring stores the current settings as a new history item.
- Retention: Database > Database settings > General. **Max history items** is the per-entry limit (0 saves no
  history; the guide recommends no more than 10). **Max. history size** truncates a large history, such as one with
  big attachments (recommended 6 MiB).

## Safe change-password routine
1. Generate in the vault's generator, save to the item **before** submitting the site's form.
2. Submit. If the site rejects it, restore the previous value from history (or the item's earlier version) and log in.
3. Log out and back in on the site to confirm the new password works.

## Gotchas
- History is part of the vault, so anyone who can open a shared item can see its earlier versions. Rotate passwords
  when removing people.
- Large KeePassXC histories grow the database file, attachments especially.

## Checked
Confirmed 2026-11-08 against Bitwarden's Vault Items page (trash, 30 days), 1Password's item history article
(password history, previous versions, permissions) and the KeePassXC User Guide (History tab, Database settings
General). Removed: Bitwarden item password history and Generator history, 1Password Recently Deleted retention, and
the claim that KeePassXC defaults to 10 versions (the guide only recommends no more than 10).
Method: docs-only read of cited pages, 2026-11-08
