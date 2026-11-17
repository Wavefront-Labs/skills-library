---
id: computing-software.cryptography-implementation.key-management.stateful-hbs-keys-in-hsms-and-backup
name: stateful-hbs-keys-in-hsms-and-backup
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, stateful-key-backup, lms, xmss, sp-800-208, hsm, stateful-signatures]
level: sme
status: draft
description: "Keep LMS and XMSS stateful keys safe per SP 800-208 sections 7-8: generate and sign only inside HSMs, forbid naive backup and cloning, and split key ranges."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-208.pdf", "https://www.rfc-editor.org/rfc/rfc8554"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateful HBS keys in HSMs and backup

## Why backup is dangerous
Restoring a backup of an LMS/XMSS private key rewinds its state: one-time keys already used get used again,
which breaks security (two signatures from the same OTS leaf allow forgery).

## SP 800-208 requirements
- Key generation and signing must happen in a hardware module validated at FIPS 140 Level 3 or above; private
  keys must not be exportable.
- The module must update state in non-volatile memory before releasing the signature.
- Exporting or cloning a private key is prohibited; backup is allowed only via approaches that never let two
  copies sign with the same leaves.

## Patterns that work
- **Distributed multi-tree (HSS)**: generate several subtrees in separate HSMs under one top-level tree;
  each HSM owns a disjoint range. Losing one HSM loses only its range.
- **Reserve range splitting**: partition the leaf index space; a standby device holds an unused range.
- Monitor remaining signatures and plan replacement keys before exhaustion.

## Anti-patterns
- VM snapshots or filesystem backups of a software signer's state file.
- Active-active HSM clusters that replicate the key without coordinated state.

## Verify
- [ ] HSM vendor documents LMS/XMSS state handling and non-export.
- [ ] Runbook covers HSM loss, range reassignment and exhaustion alerts.
