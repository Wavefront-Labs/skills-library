---
id: computing-software.cryptography-implementation.key-management.key-recovery-drills
name: key-recovery-drills
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-recovery, key-recovery-drill, disaster-recovery, tabletop-exercise, key-rotation, quorum, restore-testing]
level: advanced
status: draft
description: "Run key recovery and emergency rotation drills: scenarios, success criteria, timing, quorum availability, and turning the findings into runbook fixes."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final", "https://csrc.nist.gov/pubs/sp/800/84/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key recovery drills

Key recovery procedures fail in boring ways: the smart card PIN is with
someone on leave, the backup HSM firmware is too old, the runbook refers to a
deleted script. The only way to know is to exercise them (SP 800-84 test,
training and exercise programs; SP 800-57 Pt2 key recovery practices).

## Scenarios to rotate through

1. **Restore a KEK from backup** into a clean HSM/partition and decrypt a
   sample of production-format ciphertexts.
2. **Emergency rotation** of a signing key (JWT, webhook, code signing):
   generate, publish, switch, revoke old - measure wall-clock time.
3. **Quorum recovery**: reconstruct a Shamir-split root with M of N
   custodians, including at least one backup custodian.
4. **Region/account loss**: decrypt data using the DR region's multi-region
   key or escrowed key material.
5. **TLS certificate key compromise**: reissue and deploy across all
   endpoints (including forgotten ones found by CT log search).

## Running a drill

- Use non-production keys created for the drill, or production backups
  restored into an isolated environment. Never test by disabling live keys
  without a planned change window.
- Follow the runbook literally; a participant who "knows a faster way" hides
  runbook defects. Record each deviation.
- Time each step; set targets (e.g. signing key rotated in < 4 hours).
- Destroy restored test copies afterwards with a destruction record.

## Success criteria

- Data decrypts correctly (compare hash of recovered plaintext with known value).
- Every custodian credential (card, PIN, passphrase) worked.
- Elapsed time within target; no undocumented step needed.

## After the drill

File every gap as a ticket with an owner: missing permissions, stale contacts,
tooling changes, hardware end-of-life. Re-run failed scenarios within the
quarter.

## Verify

- [ ] Each critical key class has had a drill in the last 12 months.
- [ ] Drill reports record timings, deviations and follow-up tickets.
- [ ] Custodian lists include backups and were confirmed present in the drill.
