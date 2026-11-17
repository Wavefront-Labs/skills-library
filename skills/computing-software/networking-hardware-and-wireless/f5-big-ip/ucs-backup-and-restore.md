---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.ucs-backup-and-restore
name: ucs-backup-and-restore
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, ucs, backup, restore, config-archive]
level: practitioner
status: draft
description: "Create, copy and restore UCS archives on BIG-IP including the master-key and platform-match caveats."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://clouddocs.f5.com/training/community/f5cert/html/class4/module1/module1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UCS archives: backup and restore

A UCS contains configuration, certificates/keys, licence and local users, not logs.
```
tmsh save sys ucs /var/local/ucs/pre-change-$(date +%F)
tmsh list sys ucs
scp admin@bigip:/var/local/ucs/pre-change.ucs .
tmsh load sys ucs pre-change.ucs
tmsh load sys ucs pre-change.ucs no-license
tmsh load sys ucs pre-change.ucs no-platform-check
tmsh load sys ucs pre-change.ucs passphrase 'secret'
```
- Add `passphrase` when saving to encrypt; the same is required to load. Without it, private keys are stored recoverably, so protect the file.
- Restoring onto a different platform/hostname may need `no-platform-check`; restoring on different hardware needs a matching licence (use `no-license` and re-activate).
- Restoring a UCS from a unit with a different master key is a trap: encrypted values (e.g. monitor passwords) fail to decrypt. Restore to the same unit, or copy the master key first with `f5mku -K` / `-r` (confirm procedure on your version).
- Software version must match the UCS version (restore to same build or a later one, with caution).
- `tmsh load sys ucs` merges and restarts services; do not run it on the active unit of a pair without notice.

Verify: after load, `tmsh show sys failover`, `tmsh show ltm virtual` (availability) and `tmsh list sys global-settings hostname`. Keep `/var/local/ucs` pruned; archives fill `/var`.
