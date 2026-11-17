---
id: computing-software.cybersecurity-defensive.security-architecture.encryption-at-rest-design
name: encryption-at-rest-design
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, encryption-at-rest, envelope-encryption, kms, customer-managed-keys, tde, full-disk-encryption, field-level-encryption, key-hierarchy]
level: practitioner
status: draft
description: "Choose the right layer for encryption at rest (disk, storage service, database, field) and key ownership model, knowing what threat each layer actually addresses."
sources: ["CompTIA Security+ SY0-701 objectives 1.4 and 3.3 (encryption levels)", "NIST SP 800-111 Storage encryption for end user devices", "NIST SP 800-57 Part 1 key management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encryption at rest design

**Goal:** encryption that defends against the threats you actually have, rather than a
checkbox that leaves data readable to anyone with application or admin access.

## Layers and what they protect against
| Layer | Examples | Protects against | Does not protect against |
|---|---|---|---|
| Full disk / volume | BitLocker, LUKS, EBS/managed disk encryption | Stolen device or disk, discarded media | Anyone with OS or cloud API access |
| Storage service | S3 SSE-KMS, Azure Storage SSE, GCS CMEK | Provider media theft; with CMK, access control via key policy | Principals allowed to decrypt |
| Database (TDE) | SQL Server TDE, Oracle TDE | Stolen data files and backups | DB users and SQL injection |
| Field / application level | App-side encryption, Always Encrypted, client-side encryption | DB admins, backups, SQLi on encrypted columns | Compromised application holding keys |
| Tokenisation | Payment vaults | Scope reduction (PCI) | Vault compromise |

Pick the highest layer needed for the threat: for "DBAs and cloud admins must not read card
numbers", only field-level or tokenisation works.

## Keys
- **Envelope encryption**: data keys encrypt data; a key-encryption key (KEK) in KMS/HSM encrypts data keys. Rotation of the KEK does not require re-encrypting data.
- **Provider-managed vs customer-managed (CMK) vs external (BYOK/HYOK)**: CMK gives you key policy, audit of each use, and the ability to revoke (crypto-shred). External key stores add sovereignty at the cost of availability risk.
- Separate key administrators from data administrators; log every decrypt (CloudTrail KMS events).

## Gotchas
- "Encrypted at rest" for cloud services is usually on by default and stops only physical theft: do not oversell it in risk assessments.
- Losing a CMK (deleted key, expired external key) is data loss: use deletion waiting periods and backups of key material where allowed.
- Backups and replicas need the same encryption and key access planning.
- Application-level encryption breaks search and indexing; plan for blind indexes or tokenised lookups.

## Verify
- [ ] Each sensitive data store documents layer, key type, key owner and who can decrypt.
- [ ] Key policies reviewed; decrypt events monitored for unusual principals.
