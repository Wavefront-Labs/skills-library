---
id: computing-software.cryptography-implementation.crypto-libraries.aws-database-encryption-sdk
name: aws-database-encryption-sdk
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, aws-database-encryption-sdk, dynamodb, client-side-encryption, searchable-encryption, beacons]
level: advanced
status: docs-checked
description: "Use the AWS Database Encryption SDK for DynamoDB client-side encryption: attribute actions, beacons for searchable encrypted attributes, and hierarchical keyrings."
sources: ["https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/what-is-database-encryption-sdk.html", "https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/beacons.html", "https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/use-hierarchical-keyring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Database Encryption SDK

Formerly the DynamoDB Encryption Client. Encrypts and signs items client-side before they reach DynamoDB.

## Attribute actions
- `ENCRYPT_AND_SIGN`: confidential attributes.
- `SIGN_ONLY`: plaintext but tamper-evident.
- `SIGN_AND_INCLUDE_IN_ENCRYPTION_CONTEXT`: signed, and included in the encryption context (the Hierarchical
  keyring's branch key ID supplier can read these fields).
- `DO_NOTHING`: neither signed nor encrypted; beacons cannot be built from these fields.
Changing actions later needs a migration plan; adding new attributes needs config deployed to readers first.

## Searchable encryption (beacons)
- Standard beacon: HMAC-derived, truncated value for an encrypted field (or a virtual field joining several
  fields); supports equality searches. Beacons are built only from ENCRYPT_AND_SIGN, SIGN_ONLY or
  SIGN_AND_INCLUDE_IN_ENCRYPTION_CONTEXT fields.
- Compound beacons combine literal plaintext strings and standard beacons for richer queries, e.g. a field plus a
  sort key.
- Beacon length controls false positives versus leakage: shorter beacons hide frequency but return more
  candidates to filter. Use the SDK's beacon length guidance; never use beacons on low-cardinality fields
  without analysis.

## Keyrings
- Hierarchical keyring: branch keys live in a key store whose active branch key is decrypted by AWS KMS, then
  cached locally (the examples set a cache limit TTL of 600 seconds); reduces KMS calls. Previous branch key
  versions are used only to decrypt.
- Multi-tenant: a branch key per tenant with a branch key ID supplier (the page strongly recommends it).

## Verify
- [ ] Item dump in DynamoDB console shows binary ciphertext for encrypted attributes; queries via beacons work.

## Checked
2026-10-28. Confirmed against the AWS Database Encryption SDK developer guide pages (What is, Beacons, Hierarchical
keyring): rename from the DynamoDB Encryption Client, the four attribute actions and which can feed beacons,
standard and compound beacon behaviour, truncated-beacon false positives, branch key ID supplier for multi-tenant
use, 600 second cache limit in the examples, previous branch key versions decrypt only. Removed: `aws_dbe_b_`
prefix, `allowedUnsignedAttributePrefix`, `VersionKey`, the partition and sort key action rule, and the per-item KMS
call remark (not on these pages).
Method: documentation only; no commands were run.
