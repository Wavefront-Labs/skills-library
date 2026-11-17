---
id: computing-software.digital-privacy-hygiene.password-managers.paper-backup-of-critical-credentials
name: paper-backup-of-critical-credentials
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, paper-password-backup, emergency-kit, vault-recovery]
level: practitioner
status: draft
description: "Make a minimal paper backup of the credentials that unlock everything else, decide where to store it, and keep it current without leaking it."
sources:
  - "https://support.1password.com/emergency-kit/"
  - "https://ssd.eff.org/module/creating-strong-passwords"
  - "https://www.cisa.gov/secure-our-world/use-strong-passwords"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Paper backup of critical credentials

**Goal:** if every device is lost (fire, theft, death), the people who need to can rebuild access from one sheet.

## What goes on the sheet (only the roots)
- Password manager: account email, master password, Secret Key/Emergency Kit (1Password) or vault URL.
- Primary email account and its recovery codes.
- Phone carrier account PIN (to recover the number).
- Device unlock passcode for one phone or computer.
- Location of hardware security keys and their PINs.
Everything else stays in the vault.

## Format
- Handwritten or printed from an offline machine; avoid printers that store jobs (network printers often
  cache). Write the passphrase by hand if unsure.
- Date the sheet. Number versions.

## Storage
| Option | Pros | Cons |
|---|---|---|
| Home fireproof safe | Fast access | Lost in a burglary of the safe |
| Safe deposit box | Off-site | Bank hours, access after death may need probate |
| Sealed envelope with attorney/executor | Legacy covered | Update friction |
Many people split: copy in home safe, copy with executor.

## Keep it current
Calendar reminder every 6 months or after any master password/recovery code change. Destroy old versions
(cross-cut shred).

## Gotchas
- Don't photograph it "as a backup".
- Tamper-evident envelopes (sign across the seal) tell you if someone looked.
