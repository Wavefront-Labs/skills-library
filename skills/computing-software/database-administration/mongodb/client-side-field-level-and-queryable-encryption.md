---
id: computing-software.database-administration.mongodb.client-side-field-level-and-queryable-encryption
name: client-side-field-level-and-queryable-encryption
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, client-side-field-level-encryption, queryable-encryption, csfle, kms, data-encryption-key, automatic-encryption, crypt-shared]
level: practitioner
status: docs-checked
description: "Encrypt sensitive MongoDB fields in the driver with CSFLE or Queryable Encryption: key vault, KMS providers, encrypted fields map, and query support."
sources:
  - https://www.mongodb.com/docs/manual/core/csfle/
  - https://www.mongodb.com/docs/manual/core/queryable-encryption/
  - https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/manage-keys/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side field level and Queryable Encryption

**Goal:** fields like SSN or card numbers are encrypted before leaving the app; the server, DBAs, backups and logs never see plaintext.

## Pieces
- **Customer Master Key (CMK)** in a KMS (AWS KMS, Azure Key Vault, GCP KMS, any KMIP-compliant KMS, or the local key provider).
- **Data Encryption Keys (DEKs)** stored encrypted by the CMK in a key vault collection (e.g. `encryption.__keyVault`, unique index on `keyAltNames`).
- Driver with automatic encryption + `crypt_shared` library (or `mongocryptd`).

## CSFLE vs Queryable Encryption
| | CSFLE (4.2+) | Queryable Encryption (7.0+) |
|---|---|---|
| Equality queries | Only on deterministically encrypted fields | Yes, randomized encryption |
| Range queries | No | Yes (`queryType: "range"` on date, decimal, double, int, long fields) |
| Automatic encryption | Atlas and Enterprise Advanced (Community: explicit encryption only) | Same (QE needs 7.0+ on a replica set or sharded cluster, not a standalone) |
| Schema | JSON schema with `encrypt` per field | `encryptedFields` on the collection (QE also supports prefix, suffix and substring queries on string fields) |

## Queryable Encryption sketch (Node)
```javascript
const kmsProviders = { aws: { accessKeyId, secretAccessKey } };
const encryptedFieldsMap = { "hr.employees": { fields: [
  { path: "ssn", bsonType: "string", queries: { queryType: "equality" } },
  { path: "salary", bsonType: "int", queries: { queryType: "range", min: 0, max: 1000000 } } ] } };
const client = new MongoClient(uri, { autoEncryption: {
  keyVaultNamespace: "encryption.__keyVault", kmsProviders, encryptedFieldsMap,
  extraOptions: { cryptSharedLibPath: "/opt/mongo_crypt_v1.so" } } });
// create the collection via ClientEncryption.createEncryptedCollection(...) so DEKs are generated
await client.db("hr").collection("employees").find({ ssn: "123-45-6789" }).toArray();
```

## Operations
- Rotate DEKs with `clientEncryption.rewrapManyDataKey()` when the CMK rotates (no data re-encryption).
- Crypto-shredding: delete a DEK and data encrypted with it is unrecoverable (per-customer DEKs for GDPR erasure).
- Back up the key vault with the data, but guard the CMK separately.

## Gotchas
- Encrypted values are stored as BinData, so only the documented query operators, aggregation stages and expressions work on them; shard keys must not be encrypted fields. Check the manual's supported-operations and limitations pages for CSFLE and QE.
- QE adds metadata collections (`enxcol_.<coll>.esc` and `enxcol_.<coll>.ecoc`) and storage overhead; compact with `compactStructuredEncryptionData`.
- A client without encryption config sees the encrypted fields as BinData values, not errors.

## Verify
Query the collection from a plain mongosh: the field shows as binary data; through the configured client it returns plaintext and the equality query works.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: QE needs MongoDB 7.0+ on a replica set or sharded cluster (not standalone), CSFLE 4.2+ (Atlas and Enterprise Advanced support automatic encryption, Community explicit only), CSFLE equality only on deterministic fields, QE range queries on date/decimal/double/int/long and prefix/suffix/substring on strings, KMS providers (AWS, Azure, GCP, KMIP, local), key vault unique partial index on keyAltNames, KeyVault.rewrapManyDataKey decrypts and re-encrypts DEKs with the CMK, enxcol_.<collection>.esc and .ecoc metadata collections, compactStructuredEncryptionData, shard keys must not be encrypted, crypt_shared library preferred over mongocryptd, Node.js autoEncryption options including extraOptions.cryptSharedLibPath. Removed the unconfirmed 8.0 range version and BinData subtype claims.

Method: documentation only; no commands were run.
