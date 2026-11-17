---
id: computing-software.digital-privacy-hygiene.password-managers.vault-portability-check-before-committing
name: vault-portability-check-before-committing
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-portability, lock-in, export-formats, csv-export, json-export, 1pux, kdbx, credential-exchange-protocol, password-manager-selection]
level: practitioner
status: draft
description: "Before committing to a password manager, test that you can export everything (passwords, TOTP, notes, attachments, passkeys) in a format another manager imports."
sources:
  - "https://bitwarden.com/help/export-your-data/"
  - "https://support.1password.com/export/"
  - "https://fidoalliance.org/specifications-credential-exchange-specifications/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vault portability check

**Goal:** prove on day one that you can leave, so the manager never holds your
credentials hostage through a price rise, acquisition or shutdown.

## Test in a trial account before migrating your real data
Create 6 test items: login with TOTP, login with two URLs, secure note, card,
item with a file attachment, and a passkey for a test site (e.g. webauthn.io).
Export, then import into a second manager (KeePassXC is a good neutral target).

## What each format carries (check current docs; these change)
| Export | Carries | Typical losses |
|---|---|---|
| Generic CSV | username, password, URL, notes, often TOTP | attachments, custom field types, multiple URLs, folders, passkeys |
| Bitwarden JSON (plain or password-protected) | all item types, custom fields, folders, TOTP | attachments (download separately), passkeys only in some versions |
| 1Password `.1pux` | full fidelity incl. attachments | only some managers import it |
| KDBX | full fidelity for KeePass family | importers in cloud managers vary on attachments |
| Credential Exchange (CXF/CXP) | designed to include passkeys | rollout still in progress across vendors; uncertain availability |

## Checks to pass
- [ ] Count items before and after: equal.
- [ ] TOTP codes on 2 imported items match the source at the same moment.
- [ ] Attachments: either exported or you have a documented manual step.
- [ ] Passkeys: you know whether they move or must be re-registered per site.
- [ ] Export is available without contacting support or paying.

## Handling the export file
Plaintext exports are your whole life in one file: generate on an encrypted disk,
import immediately, then delete and empty the trash. Prefer the encrypted export
format where offered.

## Gotchas
- Some managers block export for organisation-owned items if policy forbids it; check
  family/business plans.
- Mobile apps often lack export; plan to export from desktop or web.

## Verify
- [ ] Round-trip export/import documented and repeatable in under an hour.
