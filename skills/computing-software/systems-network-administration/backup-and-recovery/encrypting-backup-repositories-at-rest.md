---
id: computing-software.systems-network-administration.backup-and-recovery.encrypting-backup-repositories-at-rest
name: encrypting-backup-repositories-at-rest
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [repository-encryption, backup-encryption, encryption-at-rest, aes-256, restic, bacula, kms]
level: practitioner
status: docs-checked
description: "Encrypt backups at rest: job-level encryption (Bacula PKI, restic), S3 server-side encryption with KMS keys, and the key-loss risk."
sources:
  - https://restic.readthedocs.io/en/stable/100_references.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Data_Encryption.html
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Encrypting backup repositories at rest

**Goal:** stolen backup media, disks or bucket contents are useless without keys you control.

## Encryption layers
| Layer | Examples | Protects against |
|---|---|---|
| Backup application (source/job) | restic (always on), Bacula PKI data encryption | Theft of files anywhere downstream, rogue storage admins |
| Repository storage | Disk, volume or drive encryption chosen per platform (check that platform's docs) | Theft of disks/tapes |
| Cloud object storage | S3 server-side encryption: SSE-S3 or SSE-KMS | Provider-side media exposure; with KMS you get key-level access control |

## Examples
- **restic**: all data in the repository is encrypted and authenticated with master keys: AES-256 in Counter mode for encryption, Poly1305-AES for authentication. The repository password unlocks a key that unlocks the master key.
- **Bacula**: in the File Daemon configuration, `PKI Signatures = Yes`, `PKI Encryption = Yes`, `PKI Keypair = "<path to fd keypair .pem>"` and `PKI Master Key = "<path to master public cert>"`. Each File Daemon should have its own key pair; master keys are extra key pairs that can decrypt any backup if the FD key is lost. Only the master public certificate belongs on the client; never keep the master private key on the client, Storage Daemon or Director machines.
- **Amazon S3**: new object uploads get SSE-S3 automatically; buckets can instead be configured for SSE-KMS. With SSE-KMS the KMS key must be in the same Region as the bucket. Objects encrypted with AWS managed keys cannot be shared cross-account; use a customer managed key for that.

## Trade-offs
- Lost keys mean lost backups. Bacula's manual says: if you lose your encryption keys, backups will be unrecoverable, so always store a copy of the master keys in a secure off-site location. Test restores with escrowed copies.
- Encryption before a deduplicating target can reduce deduplication; check your product's documentation for how it behaves.

## Gotchas
- Backup configuration often contains credentials; protect it too.

## Verify
Copy a backup file to an unprivileged machine and try to read it without the key: it must fail. Then restore it with the escrowed key.

## Checked

2026-11-09. Confirmed against restic "References" (AES-256 Counter mode, Poly1305-AES, master key behaviour), Bacula 15.0.x "Data Encryption" (PKI directives, per-FD key pairs, master keys, key-loss warning) and the Amazon S3 SSE-KMS page (SSE-S3 default, SSE-KMS option, same-Region rule, AWS managed key cross-account limit). Removed: Veeam job encryption and Enterprise Manager password recovery, Borg repokey, LUKS/BitLocker/SED/LTO and Azure rows, definite dedupe-ratio claim, and the chain-format/new-full claim (not on cited pages).

Method: documentation only; no commands were run.
