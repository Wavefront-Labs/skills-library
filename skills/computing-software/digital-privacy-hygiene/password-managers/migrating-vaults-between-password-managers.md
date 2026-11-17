---
id: computing-software.digital-privacy-hygiene.password-managers.migrating-vaults-between-password-managers
name: migrating-vaults-between-password-managers
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, migration, csv-export, 1pux, json-export, bitwarden-import, keepassxc-import, totp-migration, passkey-migration, secure-deletion, data-loss-prevention, vault-switch]
level: practitioner
status: draft
description: "Move a full vault from one password manager to another with nothing lost, nothing left behind in plaintext, and TOTP/passkeys verified working on the new tool before deleting the old one."
sources:
  - "https://bitwarden.com/help/condition-bitwarden-import/"
  - "https://support.1password.com/export/"
  - "https://keepassxc.org/docs/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating vaults between password managers

**Goal:** switch from one password manager to another (or consolidate several
into one) with every item accounted for, every TOTP seed and passkey actually
working in the new tool before the old vault is deleted, and no plaintext export
file left sitting on disk afterward.

## 1. The window of maximum risk is the export file itself
Every manager's bulk export (CSV, JSON, 1PUX) is **plaintext** — the whole vault,
unencrypted, in a file that now exists outside any vault at all. This is the
single biggest exposure in a migration, not the two apps themselves.
- Export directly to local disk, never to a cloud-synced folder (Desktop under
  OneDrive/Dropbox/iCloud sync counts as cloud-synced).
- Import immediately — don't let the export sit for "later."
- **Securely delete** the export file afterward: moving it to the recycle bin and
  emptying it is enough on an SSD with full-disk encryption already on (the
  encrypted-at-rest data makes the deleted blocks unreadable without the
  key), but if the disk isn't encrypted, treat it like any other sensitive file
  needing a real wipe pass (see
  `computing-software.digital-privacy-hygiene.device-hardening.secure-data-wiping-and-disposal`
  for why plain overwrite tools don't reliably work on SSDs either — on an
  unencrypted SSD, deleting the one file securely is actually hard; this is
  itself an argument for having full-disk encryption on *before* you ever
  export anything sensitive).

## 2. What commonly does NOT survive a straight export/import
- **TOTP/2FA secrets** stored inside the old manager: some tools include them in
  export (Bitwarden does, in the `login.totp` field of a JSON export), others
  omit them from CSV exports by default. Check the specific export format's
  documentation for the old tool — don't assume.
- **Passkeys**: cross-manager passkey portability is still immature (the FIDO
  Alliance's credential exchange format is rolling out gradually); a passkey
  created in one manager often cannot be exported and re-imported into another at
  all. Plan to **re-register** passkeys on the new manager per site rather than
  expecting a transfer, and don't delete the old manager/account until each
  passkey-protected site has a working credential in the new one.
- **Attachments** (files attached to vault items, e.g. a scanned ID): often
  excluded from bulk export entirely — check item by item before assuming
  they moved.
- **Folder/collection structure, custom fields, and item history**: format
  support varies widely between tools; expect to manually recreate organisation
  even when the core items import cleanly.

## 3. The verification pass — don't delete the old vault until this is done
1. Import into the new manager, then **compare item counts** old vs. new as a
   first-pass sanity check (not sufficient alone, but catches gross failures).
2. Spot-check a sample across categories: a login with TOTP, a password-protected
   note, an item with an attachment, and anything with a passkey.
3. For TOTP items specifically: open the new manager's generated code and confirm
   it matches a code from the old manager at the same moment (or, if the old
   manager is already gone, confirm the new code successfully logs in) — a TOTP
   secret that imported as plain text instead of parsing the `otpauth://` URI
   correctly will generate codes that look plausible but are wrong.
4. For passkey-protected accounts, actually complete a sign-in using the new
   manager's passkey before considering that account migrated.
5. Only after step 2–4 pass: delete the old manager's account/vault, revoke its
   browser extension, and destroy the export file (section 1).

## 4. Consolidating multiple vaults (e.g. a browser's saved logins plus a
dedicated manager)
Merging two live sources risks duplicate or conflicting entries overwriting a
more recent password with a stale one. Import into a **new, empty vault/
organisation** first if the tool supports it, de-duplicate there, then merge into
the live vault — safer than importing directly on top of existing items.

## Gotchas
- A successful "import complete" message from the new tool does not mean every
  field, especially TOTP and attachments, actually carried over — verify per
  section 3, don't trust the summary count alone.
- Browser-saved-password exports are unencrypted CSV with no exceptions across
  Chrome, Edge, Firefox and Safari — treat the export step itself as the
  highest-risk moment of the whole migration.
- Uncertain: specific manager-to-manager import/export field support changes
  across versions — re-check the destination tool's current import
  documentation for the source format before relying on this for anything
  high-value.

## Verify
- [ ] Export file was created on local, non-synced storage and destroyed
      immediately after import.
- [ ] Item counts compared old vs. new as a first-pass check.
- [ ] At least one TOTP item verified to generate matching/working codes in the
      new manager, not just "imported."
- [ ] Every passkey-protected account re-registered and sign-in tested in the new
      manager before the old vault was deleted.
- [ ] Old manager's account closed and its browser extension removed only after
      all of the above passed.
