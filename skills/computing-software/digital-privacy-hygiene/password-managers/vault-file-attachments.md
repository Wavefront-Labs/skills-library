---
id: computing-software.digital-privacy-hygiene.password-managers.vault-file-attachments
name: vault-file-attachments
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-attachments, file-attachments, bitwarden-premium, 1password-documents, keepassxc-attachments, export-gaps, ssh-keys, gpg-keys]
level: practitioner
status: docs-checked
description: "Store small sensitive files as vault attachments in Bitwarden, 1Password or KeePassXC, within each product's limits, and include them in exports and backups."
sources:
  - "https://bitwarden.com/help/attachments/"
  - "https://support.1password.com/files/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault file attachments

**Goal:** keep the few small files that are as sensitive as passwords (key backup, 2FA recovery
PDF, scanned passport) encrypted and next to the related login.

## Limits and behaviour
- **Bitwarden**: attachments are for Premium users and members of paid organisations, with 5 GB of
  encrypted storage per user (more in 1 GB increments). Any file type up to 500 MB (100 MB when
  uploading from mobile). Attachments on individual items and all Sends use the individual
  storage; attachments on organisation-owned items use shared organisation storage. Encryption
  and decryption happen locally. Self-hosted storage is limited by volume space, up to 10 TB.
- **1Password**: add a file via New Item > Document, or attach to an existing item with Edit >
  Add More > Attach a File. Individual accounts include 1 GB of storage; Families and Teams 1 GB
  per person; Business 5 GB per person, with files up to 2 GB. Business admins can turn off file
  saving for team members.
- **KeePassXC**: you can attach files to any entry; they are added to the database and stored as
  encrypted binaries. Opening one extracts it to a temporary file and opens it in the default
  application; afterwards you choose to import or discard changes, and KeePassXC securely deletes
  the temporary file by overwriting it. The guide notes that entry history is truncated above a set
  size (it recommends 6 MiB), for example when entries have large attachments.

## Good uses
- 2FA recovery code PDFs downloaded from a site.
- Key backups, or small signed documents needed in an emergency.

## Backup and export
1. Bitwarden: select the `.zip (with attachments)` format in Tools > Export (web), Settings >
   Vault options > Export vault (extension), File > Export vault (desktop), or `bw export
   --format zip`. Attachments can be exported only from your individual vault. The export asks
   for your master password or an email verification code.
2. Bitwarden CLI per file: `bw get attachment <file> --itemid <id> --output <dir>`; add with
   `bw create attachment --file <path> --itemid <id>`.
3. KeePassXC: CSV, XML and HTML exports do not support attachments (per the guide); the database
   file itself holds them.
4. 1Password: the cited page does not describe export behaviour; verify before relying on it.

## Gotchas
- Bitwarden attachments encrypted before December 2018 use an older method and show an alert
  icon; use the Fix button on the item's Edit > Attachments to re-encrypt them.
- Shared vault items give others access to their files (1Password tip: add files to a shared
  vault to give others access).

## Verify
- [ ] Backup routine states how attachments are captured.
- [ ] One attachment restored from backup and opened.

## Checked

Date 2026-11-08. Pages read: Bitwarden File Attachments, 1Password Save important files, KeePassXC User Guide (attachment sections, export notes). Corrected: Bitwarden quota is 5 GB, not 1 GB; per-file limit is 500 MB (100 MB mobile). Removed as not on the pages: the claim that 1Password .1pux includes files, the KDBX sync-bloat claim, Cryptomator/VeraCrypt advice, the temporary-copy-on-some-platforms claim (replaced by the KeePassXC wording), and the item-key claim.

Method: docs-only read of cited pages, 2026-11-08
