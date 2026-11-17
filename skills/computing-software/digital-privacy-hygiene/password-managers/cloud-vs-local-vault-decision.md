---
id: computing-software.digital-privacy-hygiene.password-managers.cloud-vs-local-vault-decision
name: cloud-vs-local-vault-decision
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, cloud-vs-local-vault, password-manager-selection, keepassxc, bitwarden, 1password, offline-vault, sync, threat-model]
level: practitioner
status: draft
description: "Decide between a cloud-synced password manager and a local KDBX file by threat model, sync needs, backup discipline and who else must use the vault."
sources:
  - "https://www.privacyguides.org/en/passwords/"
  - "https://ssd.eff.org/module/choosing-password-manager"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud-synced vs local-file vault

**Goal:** pick the storage model you will actually maintain for years, because a
vault you abandon or lose is worse than either choice done well.

## The two models
- **Cloud-synced (Bitwarden, 1Password, Proton Pass):** encrypted vault stored by the
  vendor, synced automatically, sharing and emergency access built in. Risk: the
  encrypted vault sits on someone else's server and can be stolen in bulk; your
  protection then rests on master password strength and KDF cost.
- **Local file (KeePassXC/KeePass `.kdbx`):** one encrypted file you own. No vendor
  server to breach and no account to lock you out. Risk: you are the sync service and
  the backup service; file conflicts and lost copies are on you.

## Decision table
| Situation | Lean |
|---|---|
| Non-technical user, several devices, phone heavy | Cloud |
| Need family sharing or emergency access for a spouse | Cloud (or self-hosted Vaultwarden) |
| Air-gapped or very high-risk, few devices, disciplined backups | Local |
| Distrust of any third-party server, comfortable with Syncthing | Local |
| Need it to work if the vendor goes bankrupt tomorrow | Local, or cloud with regular encrypted exports |

## If you choose cloud
- Use a **diceware master passphrase of 5-6 words** or more; with bulk theft the
  attacker has unlimited offline time.
- Confirm the KDF is at current defaults (old accounts may still have low iterations).
- Schedule an encrypted export (see
  `computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery`).

## If you choose local
- Sync with Syncthing or a cloud folder; never edit the same file on two devices
  while both are offline, or you will get conflict copies. Merge them with
  `computing-software.digital-privacy-hygiene.password-managers.merging-divergent-kdbx-databases`.
- Keep at least two backups on different media, and one off-site.
- Pick mobile clients deliberately (KeePassDX on Android, Strongbox or KeePassium on iOS).

## Gotchas
- "Local" stored in a Dropbox folder is a cloud copy too; that's fine (the file is
  encrypted) but be honest that the threat model now includes Dropbox.
- Hybrid is legitimate: cloud manager for daily logins, a separate KDBX for a small set
  of break-glass secrets (recovery codes, crypto seeds).

## Verify
- [ ] You can name where every copy of your vault lives.
- [ ] You have restored the vault on a second device at least once.
