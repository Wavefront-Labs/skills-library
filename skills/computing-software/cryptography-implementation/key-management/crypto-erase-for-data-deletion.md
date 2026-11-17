---
id: computing-software.cryptography-implementation.key-management.crypto-erase-for-data-deletion
name: crypto-erase-for-data-deletion
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-destruction, crypto-erase, cryptographic-erasure, gdpr-erasure, per-user-keys, nvme-sanitize, sp-800-88]
level: advanced
status: draft
description: "Delete data by destroying its key: per-subject key design, purging caches and backups of keys, what crypto-erase cannot remove, and drive-level crypto erase."
sources: ["https://csrc.nist.gov/pubs/sp/800/88/r1/final", "https://gdpr-info.eu/art-17-gdpr/", "https://nvmexpress.org/specifications/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crypto-erase for data deletion requests

Deleting every copy of a record (replicas, backups, data lakes, logs) is
often impossible. If each subject's data is encrypted under its own key,
destroying that key makes all copies unreadable: cryptographic erasure.
SP 800-88 recognises it as a sanitisation method.

## Design for it

- One data key per subject (user, tenant, case) or per object, wrapped by a
  KEK in KMS. Store wrapped keys in a dedicated key table.
- Encrypt every place the data lands with that key: primary DB fields,
  exports, analytics copies, event streams.
- Backups contain only wrapped keys; the key table itself must be excluded
  from long-retention backups or its backups must also be purged, or the
  erasure is undone by a restore.
- Derived keys must not be re-derivable: if a subject key is
  `HKDF(root, user_id)`, you cannot erase it without rotating the root.
  Use random per-subject keys.

## Erase procedure

1. Delete the wrapped subject key from the key table and its replicas.
2. Purge data-key caches (AWS Encryption SDK caches, app memory) or wait
   their TTL.
3. Purge or let expire the key table backups per a documented schedule
   (state the window in the privacy notice).
4. Record the erasure (key id, time, request id) without storing personal
   data.

## Limits

- Plaintext copies outside the scheme (search indexes, logs, caches, ML
  training sets) are not erased; find and delete them separately.
- Metadata (row existence, timestamps) remains.

## Media-level crypto erase

Self-encrypting drives change their internal media key:
`nvme sanitize /dev/nvme0 --sanact=4` (crypto erase) or
`nvme format /dev/nvme0n1 --ses=2`; ATA `SANITIZE CRYPTO SCRAMBLE`.
Verify by reading back sectors and record per SP 800-88.

## Verify

- [ ] After erasure, every copy (including restored backups past the window) fails to decrypt.
- [ ] No plaintext copies outside the scheme.
