---
id: computing-software.digital-privacy-hygiene.password-managers.importing-from-another-password-manager
name: importing-from-another-password-manager
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, password-manager-import, migration, csv-export]
level: practitioner
status: draft
description: "Import a vault from 1Password, LastPass, Chrome, KeePass or Bitwarden using the right export format so folders, TOTP, notes and attachments survive."
sources:
  - "https://bitwarden.com/help/import-data/"
  - "https://support.1password.com/import/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_importing_databases"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Importing from another password manager

**Goal:** move everything with the richest format available, so you don't lose fields that CSV drops.

## Prefer native formats over CSV
| From | Best export | Notes |
|---|---|---|
| 1Password | `.1pux` | Keeps vaults, custom fields, TOTP; not attachments |
| Bitwarden | JSON (or encrypted JSON) | Folders, custom fields, TOTP, passkeys only in some flows |
| LastPass | Direct import (Bitwarden/1Password support) or CSV | Attachments separate |
| Chrome/Edge | CSV from password settings | Logins only |
| Firefox | CSV (about:logins > ... > Export) | Logins only |
| KeePass/KeePassXC | KeePass 2 XML or KDBX | Groups map to folders |

## Bitwarden import
Web vault > Tools > Import data > choose format > file. CLI: `bw import --formats` then
`bw import lastpasscsv export.csv`.

## 1Password import
1Password.com > (account) > Import, choose source; desktop app supports direct import from some managers.

## KeePassXC import
Database > Import > CSV/1Password/Bitwarden JSON/KeePass1 into a new database.

## After import
1. Spot-check 10 items including one with TOTP and one secure note.
2. Count items: source vs destination.
3. Move attachments manually.
4. Securely delete the export file (it's plaintext), empty trash.

## Gotchas
- Passkeys generally don't export via these formats yet; re-create them or use Credential Exchange where supported.
- Imports of shared folders may land in your personal vault; re-share deliberately.
