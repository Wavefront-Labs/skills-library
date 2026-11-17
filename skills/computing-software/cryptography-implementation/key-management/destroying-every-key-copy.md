---
id: computing-software.cryptography-implementation.key-management.destroying-every-key-copy
name: destroying-every-key-copy
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-copy-destruction, key-destruction, crypto-shredding, backups, secret-sprawl, key-inventory, decommissioning]
level: practitioner
status: docs-checked
description: "Locate and destroy every copy of a key: backups, replicas, HSM backups, CI secrets, laptops, images, swap and logs, and use crypto-shredding where copies are unbounded."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroying every key copy

SP 800-57 Part 1 section 8.3.4: all copies of a private or secret key shall be
destroyed as soon as they are no longer required (for example for archival or
reconstruction), in a manner that removes all traces so the key cannot be
recovered by physical or electronic means. Public keys may be retained or
destroyed as desired. When copies are made, plan for their eventual
destruction, for example by recording the identity of sharing parties in the
key's metadata. In practice copies are everywhere.

## Where copies hide
| Location | How to find |
|---|---|
| KMS/HSM replicas, multi-region keys, HSM backups | Provider replica listings, HSM backup inventory |
| Database or file backups containing wrapped or plaintext keys | Backup catalogues; search for key IDs |
| CI/CD variables, secrets managers, container-orchestrator secrets | Secret manager listings |
| Developer machines, downloads, password managers | Ask custodians; managed-device file search |
| Container images, VM templates, machine images | Image secret scanning |
| Source history, wikis, tickets, chat | Secret scanners, data-loss-prevention search |
| Logs, core dumps, crash reports, swap | Log search for key fingerprints; dump retention policies |
| Partner systems you sent the key to | Key exchange records |

## Procedure
1. Use the inventory and key-exchange records to list known copies; run discovery for unknown ones.
2. Destroy primary copies (KMS deletion, HSM delete), then replicas and backups.
3. For copies you cannot reach (old tape backups, partners), rely on the hierarchy: destroy the KEK that wraps them
   so they become useless (crypto-shredding).
4. Record each destruction with evidence and witness.

## Design so this is easy
- Keep plaintext keys inside KMS/HSM; distribute only wrapped keys.
- One KEK per data domain so destroying a KEK removes all copies of the keys it wraps.
- Backups store wrapped keys only; never plaintext key exports.

## Verify
- [ ] Destruction checklist covers every row of the table above.
- [ ] Attempted decryption with the old key ID fails across environments.

## Checked

2026-11-01. Confirmed against SP 800-57 Pt1 Rev 5 section 8.3.4 (all copies
destroyed when no longer required, all traces removed, record sharing parties
in metadata, public keys optional). Removed: the `kubectl` command, named
scanner tools, "unless archived under control" paraphrase, SP 800-88 and OWASP
sources (not read this batch). The remaining table and design rules are
procedural advice, not factual claims.

Method: documentation only; no commands were run.
