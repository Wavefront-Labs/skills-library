---
id: computing-software.cloud-infrastructure-engineering.minio.sse-overview
name: sse-overview
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, sse-overview, server-side-encryption, secure-erasure, key-locking, external-key, sse-strategies, kms]
level: practitioner
status: docs-checked
description: "Compare MinIO server-side encryption SSE-KMS, SSE-S3 and SSE-C, the TLS requirement, irreversibility of enabling, and how sealing or deleting keys locks or erases objects."
sources: ["https://github.com/minio/docs/blob/main/source/administration/server-side-encryption.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO server-side encryption overview

SSE encrypts objects during writes on the server (encryption at rest) and supports compliance needs for secure locking and erasure. MinIO's implementation uses the MinIO Key Encryption Service (KES) with an external Key Management System (KMS), or client-managed keys, and is API-compatible with AWS SSE. **SSE requires TLS** to be enabled.

## Strategies
- **SSE-KMS (recommended).** Automatic bucket-default encryption with a specific External Key (EK) held in the KMS; clients may override with an explicit key per write, or specify a key per write on buckets with no default. Most granular. The docs state it cannot be disabled once enabled.
- **SSE-S3.** Bucket-default encryption using *one* EK for the whole deployment; clients can also request SSE on a write. Same note about not disabling.
- **SSE-C.** The client supplies the key on each write; no bucket-default setting, and the client does all key management.

KES-based strategies list supported KMS targets such as AWS Secrets Manager, Azure Key Vault, Entrust KeyControl, Fortanix SDKMS, Google Cloud Secret Manager, HashiCorp Vault and Thales CipherTrust Manager.

## Secure erasure and locking
MinIO needs both the KMS and the EK to decrypt. So you can:
- seal the KMS (locks all SSE-KMS and SSE-S3 objects while sealed),
- seal or unmount an EK (locks objects protected by it),
- delete an EK (objects permanently unreadable; typically irreversible, may help meet secure-deletion rules).

Details per strategy: `computing-software.cloud-infrastructure-engineering.minio.sse-kms`, `...sse-s3`, `...sse-c`, and KES setup in `computing-software.cloud-infrastructure-engineering.minio.kes-configuration`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Server-Side Encryption of Objects page (server-side-encryption.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
