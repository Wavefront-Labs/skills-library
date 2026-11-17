---
id: computing-software.cryptography-implementation.applied-cryptography.application-field-level-encryption
name: application-field-level-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, data-at-rest-encryption, cryptographic-storage, field-level-encryption, column-encryption, envelope-encryption, aad, pii, owasp]
level: advanced
status: draft
description: "Encrypt sensitive database fields in the application: AEAD with row/column-bound AAD, per-tenant data keys from KMS, schema sizing, and query/ops trade-offs."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://www.mongodb.com/docs/manual/core/csfle/", "https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/what-is-database-encryption-sdk.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application field-level encryption

Disk/TDE encryption protects against stolen disks and backups; it does nothing
against SQL injection, a compromised DB account or a curious DBA, because the
database decrypts for any authorised query. Field-level encryption (FLE)
encrypts selected columns in the application so the database only ever sees
ciphertext.

## Design

1. **Pick fields**: secrets and high-risk PII (national IDs, bank numbers,
   health data, tokens). Not everything - every encrypted field loses
   indexing, sorting, range queries and DB-side validation.
2. **Algorithm**: AES-256-GCM or XChaCha20-Poly1305 via a vetted library (Tink
   AEAD, AWS Database Encryption SDK, libsodium). Random nonce per value.
3. **AAD binds the value to its place**: `table || column || primary key ||
   tenant id`. Without it an attacker with DB write access can copy an
   encrypted SSN from one row into another (or swap columns) and the app will
   happily decrypt it.
4. **Keys**: envelope encryption. A data key per tenant (or per table) wrapped
   by a KMS key; cache unwrapped data keys in memory with a TTL.
5. **Format**: store `version || key id || nonce || ciphertext || tag` (see
   versioned ciphertext format skill), base64 if the column is text.

## Schema sizing

Ciphertext length = plaintext + 12 (nonce, GCM) or 24 (XChaCha) + 16 (tag) +
header (~5-40 bytes for version and key id). Base64 adds 33%. A
`VARCHAR(11)` SSN column becomes roughly `VARCHAR(100)`. Migrations fail on
truncation if you forget.

## Querying

- Equality: add a blind index column (HMAC of normalised value, separate key)
  or use deterministic AES-SIV for that column.
- Range/sort/LIKE: not available with standard crypto; keep such fields
  unencrypted, tokenise, or accept application-side filtering.
- MongoDB Queryable Encryption and SQL Server Always Encrypted provide
  driver-side FLE with limited query support; same AAD/key principles apply.

## Ops

- Logs, ORM debug output and error messages must not print decrypted fields.
- Backups contain ciphertext; key availability is now part of restore.
- Key rotation: rewrap data keys under new KMS key cheaply; re-encrypting
  values requires a background job.

## Verify

- [ ] Swapping an encrypted value between two rows makes decryption fail (AAD works).
- [ ] DB-level dump shows no plaintext for encrypted columns.
- [ ] Column sizes fit max ciphertext length; migration tested with long inputs.
- [ ] Data keys are wrapped by KMS and cached with a bounded TTL.
