---
id: computing-software.systems-network-administration.backup-and-recovery.encryption-vs-deduplication-tradeoff
name: encryption-vs-deduplication-tradeoff
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [encryption-dedup-tradeoff, deduplication, encryption, convergent-encryption, dedupe-appliance]
level: advanced
status: draft
description: "Place encryption so it does not destroy deduplication: encrypt after dedupe, at-rest on the appliance, per-repository keys, and when to accept lower ratios for security."
sources:
  - https://restic.readthedocs.io/en/stable/100_references.html
  - https://www.usenix.org/conference/usenixsecurity13/technical-sessions/presentation/bellare
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption vs deduplication trade-off

Encrypted data looks random, so two identical blocks encrypted with different keys or IVs never deduplicate.

## Placement rules
1. **Dedupe first, then encrypt**: the backup engine chunks and dedupes, then encrypts unique chunks (restic, Borg, PBS, Veeam job encryption all do this within their own repository).
2. **Do not encrypt before sending to a dedupe appliance**: Veeam job-level encryption to Data Domain or StoreOnce kills the appliance ratio. Use the appliance's at-rest encryption and in-transit encryption instead.
3. **Source data already encrypted** (database TDE, encrypted VMs, BitLocker inside guests read at block level, ransomware): dedupe and compression ratios collapse. Back up at a layer where data is plaintext (TDE databases via native backup with backup encryption, guest file level) or budget raw capacity.
4. **Scope of dedupe = scope of key**: Veeam dedupes only within a job/backup file; jobs with different passwords never share blocks.

## Convergent encryption
Some systems derive keys from content (convergent encryption) so identical data encrypts identically and still dedupes across users. It leaks equality of content (an attacker can confirm a known file is stored). Acceptable for many enterprise cases, avoid for highly sensitive multi-tenant data.

## Decision table
| Need | Choice |
|---|---|
| Max ratio on appliance | Appliance at-rest encryption + TLS in transit |
| Backups readable only by backup team, cloud object store | Encrypt in backup software (dedupe within repo still works) |
| Regulated data on shared multi-tenant storage | Per-tenant keys; accept lower global dedupe |

## Verify
Compare ratios before and after enabling encryption on a pilot job; document the expected capacity change in the capacity plan.
