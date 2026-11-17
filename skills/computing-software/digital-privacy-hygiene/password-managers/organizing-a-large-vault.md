---
id: computing-software.digital-privacy-hygiene.password-managers.organizing-a-large-vault
name: organizing-a-large-vault
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-organization, folders, tags, favorites, naming-convention, vault-health, archive]
level: practitioner
status: docs-checked
description: "Organise a vault of hundreds of items with a naming convention, a small folder set, favourites and an archive, so search works and stale items get cleaned."
sources:
  - "https://bitwarden.com/help/folders/"
  - "https://support.1password.com/favorites-tags/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organising a large vault

**Goal:** a ten-year vault can reach hundreds of items. Without structure people stop trusting
search, create duplicates, and keep dead accounts that still hold valid passwords.

## Naming convention
`<Service> - <account qualifier>`: `Google - personal`, `Google - work`,
`Bank of X - joint`. Put the service first so alphabetical sort groups them (Bitwarden lists folders alphabetically).
KeePassXC search matches Title, Username, URL, Tags and Notes by default, so fill the URL field correctly.

## What each manager gives you
- **Bitwarden folders** organise your own vault only. Any item can go in a folder, including items shared with you
  from an organization, and other members can set up different layouts. Deleting a folder is permanent but does not
  delete its items. Nest by naming a folder `Parent/Child`; searching in a parent folder does not include nested
  folders' items. **Collections** are what organisation members share.
- **1Password** has Favorites and tags: multiple tags per item, nested with `/`, and the app search finds tags.
- **KeePassXC** has groups, custom tags (any number per entry, shown in a Searches and Tags panel) and saved searches
  such as expired and weak passwords.
- **Bitwarden Archive** (paid plans) hides items from search results and autofill but keeps them in exports and
  reports; one user's archiving does not archive for others.

## Suggested minimal set
- Folders or groups: `Finance`, `Email & identity`, `Shopping`, `Social`, `Work`, `Home & devices`, `Archive`.
- Tags where available: `critical` (email, bank, vault, phone carrier), `shared`, `has-2fa`, `no-2fa-available`.
- **Favourites**: the 10-20 items you use daily.

## The Archive pattern
When you delete an online account, do not delete its item immediately: move it to `Archive` (a folder, or Bitwarden's
Archive) with a note "account deleted <date>". After a year, delete. If you keep using the item, it was not dead.
Remember that Bitwarden's trash empties after 30 days.

## Quarterly tidy (20 minutes)
1. Review your manager's password health or security reports, or the KeePassXC saved searches for expired and weak.
2. Review the oldest items.
3. Merge duplicates (see
   `computing-software.digital-privacy-hygiene.password-managers.deduplicating-an-imported-vault`).
4. Check `critical` items all have MFA and recovery details.

## Gotchas
- Moving an item into a folder never shares it; sharing in Bitwarden happens by assigning to a collection.
- Over-tagging stops being maintained; five tags used consistently beat thirty.

## Verify
- [ ] Every `critical` item found in under 5 seconds by search.
- [ ] Archive folder exists and has dated notes.

## Checked
Confirmed 2026-11-08 against Bitwarden's Folders page (personal scope, nesting with `/`, deletion behaviour), the
Vault Items page (Archive and trash behaviour), 1Password's favorites and tags article (nested tags, multiple tags),
and the KeePassXC User Guide (tags panel, saved searches, default search fields). Removed: the one-folder-per-item
claim, the health report field list, and the "sort by last modified" step, which the pages do not state.
Method: docs-only read of cited pages, 2026-11-08
