---
id: computing-software.cryptography-implementation.applied-cryptography.encrypting-backups-and-exports
name: encrypting-backups-and-exports
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, data-at-rest-encryption, backup-encryption, age, restic, streaming-encryption, key-escrow, restore-testing]
level: practitioner
status: docs-checked
description: "Encrypt backups and exports so they stay restorable: public-key encryption to offline recipients, age and restic, key escrow, restore drills."
sources: ["https://age-encryption.org/v1", "https://restic.readthedocs.io/en/stable/100_references.html#design", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypting backups and exports

Backups and exports are a common way encrypted production data leaks in plaintext: a database dump in a bucket, a
CSV emailed to finance. Encrypt them at creation, to keys that are not on the machine that makes the backup.

## Use public-key encryption for the writer

The backup host only needs a **public** key. The private key lives offline or in a restricted vault, so a
compromised backup host cannot read past backups.

The age format (age-encryption.org/v1) fits this: a file has one or more recipient stanzas, each wrapping the
same random file key independently, so a second recipient (a break-glass key held by another team) can decrypt
too. An X25519 recipient is a public key; the payload is split into 64 KiB chunks, each encrypted with
ChaCha20-Poly1305, and the header ends with a MAC. Tampering therefore fails decryption.

Compress before encrypting, because ciphertext does not compress.

Alternative: restic encrypts everything in its repository with AES-256 in counter mode and authenticates it with
Poly1305-AES. The master key is stored in a key file protected by a key derived from the repository password
using scrypt, so protect that password like a private key.

## Avoid
- Encryption keys stored in the same location as the encrypted backups. OWASP: keep keys in a separate location
  from encrypted data, ideally on separate systems, so one compromise does not expose both.
- Unauthenticated encryption of backup files; use an authenticated format such as the two above.
- Passphrases shared alongside the file, or baked into scripts on the backup host.

## Key escrow and retention
- Backup decryption keys must outlive the backups (retention period plus margin); document who holds them and
  how to retrieve them.
- OWASP recommends storing keys themselves in encrypted form, with a separate key-encrypting key protecting the
  data encryption key.

## Restore drills
An encrypted backup you cannot decrypt is a deleted backup. Periodically restore a random backup on a clean
machine using only the documented key-retrieval procedure.

## Verify
- [ ] Backup host holds only public keys or write-only credentials.
- [ ] A tampered backup file fails decryption.
- [ ] A break-glass recipient exists and its holders are documented.
- [ ] Last restore drill date and result recorded.

## Checked
Method: docs-checked 2026-11-09 against the age v1 specification page (recipient stanzas, X25519, 64 KiB ChaCha20-Poly1305 chunks, header MAC), the restic design reference (AES-256 CTR, Poly1305-AES, scrypt-protected master key) and the OWASP Cryptographic Storage Cheat Sheet (Separation of Keys and Data, Encrypting Stored Keys sections). Dropped as unconfirmed: the age/pg_dump command lines, borg and GPG mentions, KMS cross-account advice, crypto-shredding, and the quarterly drill cadence.
