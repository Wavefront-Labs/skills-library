---
id: computing-software.database-administration.mongodb.encryption-at-rest-with-kmip
name: encryption-at-rest-with-kmip
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, encryption-at-rest-mongodb, kmip, mongodb-security, wiredtiger-encryption, key-rotation]
level: practitioner
status: docs-checked
description: "Enable MongoDB Enterprise encrypted storage engine with a KMIP key server, rotate master keys, and migrate an existing replica set to encryption with rolling resyncs."
sources:
  - https://www.mongodb.com/docs/manual/core/security-encryption-at-rest/
  - https://www.mongodb.com/docs/manual/tutorial/configure-encryption/
  - https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption at rest with KMIP

**Goal:** WiredTiger data files encrypted with the Enterprise encrypted storage engine (AES256-CBC by default; AES256-GCM is also supported on Linux), with the master key held in an external KMIP server, not on the database host.

## Configure (new or resynced node)
```yaml
security:
  enableEncryption: true
  kmip:
    serverName: kmip.corp.example
    port: 5696
    serverCAFile: /etc/mongodb/kmip-ca.pem
    clientCertificateFile: /etc/mongodb/kmip-client.pem
    # keyIdentifier: <existing key id>   # omit on first start to have a key created
```
On first start mongod creates a master key in KMIP and logs `Created KMIP key with id: <UID>`; record it. Database keys are internal to the server, encrypted with the master key; only the master key is external and MongoDB never pages it to disk. To reuse an existing KMIP key set `security.kmip.keyIdentifier`.

## Existing data cannot be encrypted in place
Encrypt a replica set by rolling resync:
1. Pick a secondary, stop it, empty its dbPath.
2. Start with encryption options; it initial-syncs and writes encrypted files.
3. Repeat for each secondary, then step down the primary and do it last.

## Key rotation
KMIP master key rotation re-encrypts the internal keystore and leaves the database keys unchanged, so the data set is not re-encrypted:
```bash
mongod --config /etc/mongod.conf --kmipRotateMasterKey     # with a new --kmipKeyIdentifier, or omit it to request a new key
```
mongod exits when the rotation and keystore re-encryption finish; restart it without `--kmipRotateMasterKey` (or remove `security.kmip.rotateMasterKey`). Do secondaries one at a time, then step down the primary and rotate it last. Database keys change only by rotating the member out: start a new mongod with a new key, `rs.add()` it so initial sync re-encrypts the data with new database keys, then remove the old member and delete its data (one member at a time).

## Local keyfile option
`encryptionKeyFile` takes a base64-encoded keyfile holding a single 16 or 32 character string, readable only by the mongod owner. The manual says the keyfile method does not meet most regulatory key management guidelines.

## Gotchas
- With AES256-GCM, a filesystem restore needs the database keys rolled over (`--eseDatabaseKeyRollover`) so no key and counter block are reused.
- Secure management of the keys is critical: data encrypted with a lost master key cannot be read. Master and database keys are not replicated and encryption is not applied over the wire, so use per-node keys and TLS.
- The encrypted storage engine is MongoDB Enterprise only; Atlas manages its own encryption at rest.

## Verify
`db.adminCommand({getCmdLineOpts: 1}).parsed.security.enableEncryption` is true, the log shows `Encryption key manager initialized using master key with id: <UID>`.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: encrypted storage engine is Enterprise only, AES256-CBC default and AES256-GCM on Linux, only the master key is external, KMIP options (enableEncryption, kmip.serverName/port/serverCAFile/clientCertificateFile/keyIdentifier), log messages for key creation and initialisation, existing data encrypted by rolling initial sync, kmipRotateMasterKey procedure (mongod exits, restart without the flag, primary last), database-key rotation by replacing a member, encryptionKeyFile format, eseDatabaseKeyRollover for GCM filesystem restores. Removed unconfirmed vendor names, mongodump-plaintext and strings-check claims.

Method: documentation only; no commands were run.
