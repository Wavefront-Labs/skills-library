---
id: computing-software.cryptography-implementation.key-management.stateful-signature-state-management
name: stateful-signature-state-management
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, hash-based-signatures, signature-state-management, lms, xmss, hss, index-reuse, hsm, backup, sp-800-208]
level: sme
status: draft
description: "Keep LMS/XMSS private key state safe: reserve-then-sign ordering, index range partitioning for HA, backup without cloning, and incident response for suspected reuse."
sources: ["https://csrc.nist.gov/pubs/sp/800/208/final", "https://eprint.iacr.org/2016/357", "https://datatracker.ietf.org/doc/html/rfc8554#section-9"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateful signature state management

With LMS/XMSS, signing two different messages with the same one-time key
index lets an attacker forge signatures. The engineering problem is state:
the index must move forward exactly once per signature, across crashes,
failover, backups and humans.

## Ordering: reserve, persist, sign

1. Read current index i.
2. Write i+1 (or i+k for a batch) to durable storage and fsync / commit.
3. Only then compute signatures with indices i .. i+k-1.
4. If the process dies after step 2, indices are wasted, never reused.

HSMs that support LMS do this internally; verify the vendor documents
crash-consistent counter handling.

## High availability without cloning

- **Partition index ranges**: HSM A owns leaves 0..2^19-1, HSM B owns
  2^19..2^20-1. RFC 8554 supports this by splitting at the HSS level: each
  device gets its own lower-level tree signed by the top tree.
- **No active-active on one range.** Two signers sharing one counter through a
  database is fragile; prefer separate subtrees.
- VM snapshots, container images and filesystem restores must never contain
  live private state. Restoring a snapshot rolls the counter back.

## Backup

SP 800-208 discourages exporting private keys. Instead of backing up the key:
- Generate several independent top-level keys (or subtrees) on different HSMs
  and publish all their public keys (or sign them under one root), so loss of
  one device does not stop signing.
- If an HSM supports backup of stateful keys, it must do so in a way that
  invalidates the remaining range on the source (some vendors "split" the
  remaining range between original and backup).

## Monitoring and response

- Track remaining signatures per key; alert at 20% and 5%.
- Log every index used with the message hash; a duplicate index in the log
  means reuse. Treat that as key compromise: stop signing, revoke or rotate
  the affected tree, and check for signatures in the wild that do not match
  logged hashes.

## Verify

- [ ] Code or HSM persists the counter before releasing a signature (test with a crash injected after sign).
- [ ] Each signer instance has a disjoint index range or subtree.
- [ ] Backups/snapshots verified to contain no private stateful key material.
- [ ] Index log exists and a duplicate-index check runs.
