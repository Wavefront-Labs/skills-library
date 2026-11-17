---
id: computing-software.systems-network-administration.pki-tls-administration.key-backup-split-knowledge
name: key-backup-split-knowledge
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [key-backup-split-knowledge, pki-hsm, hsm, key-backup, shamir, m-of-n, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Back up CA keys with M-of-N shares or wrapped HSM backups, store shares separately and test recovery without exposing the key."
sources:
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key backup and M-of-N split knowledge
Goal: survive loss of a custodian or an HSM without a single person holding the key.
- Not every key needs a backup. NIST SP 800-57 says private signature keys are in general not backed up (non-repudiation would be in question), but backup may be warranted in some cases, such as a CA's private signing key. Any backed-up key must stay under the owner's control.
- Split knowledge, as NIST defines it: the key is split into n shares, each providing no knowledge of the key. If k shares are needed to rebuild it, any k-1 shares reveal nothing about the key beyond possibly its length. That is the M-of-N model (k-of-n) for CA key backup.
- Keep one or more copies of key information in physically separate locations (backup or archive storage) and check the integrity of each copy periodically.
- Backed-up keying material should stay in backup storage as long as the key is used operationally; when it is no longer needed it should be removed and every trace destroyed.
- Document who can authorise recovery and how custody changes when a person leaves.
Gotcha: untested backups are assumptions; custodians change roles and shares go missing silently, so reconfirm possession on a schedule you set.
Verify:
- [ ] A recovery drill signs a test CSR from restored material.
- [ ] Share inventory matches the physical count.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-57 Part 1 Rev 5 PDF (nvlpubs.nist.gov), read the split-knowledge glossary entry, section 6.2.2 integrity text, section 8.2.2.1 backup storage and Table 7.
Removed: HSM clone-domain claim, the ssss-split command, annual drill cadence and share rotation dates (not in source).
