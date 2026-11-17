---
id: computing-software.data-engineering.data-warehouse-architecture.encryption-and-key-management
name: encryption-and-key-management
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-security, encryption-at-rest, cmek, kms, tri-secret-secure, column-level-encryption, crypto-shredding, key-rotation]
level: advanced
status: docs-checked
description: "Key ownership for data platforms: AWS KMS key types, BigQuery CMEK and dataset default keys, Snowflake Tri-Secret Secure, and BigQuery AEAD for crypto-shredding."
sources:
  - https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html
  - https://cloud.google.com/bigquery/docs/customer-managed-encryption
  - https://docs.snowflake.com/en/user-guide/security-encryption-tss
  - https://cloud.google.com/bigquery/docs/aead-encryption-concepts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption at rest and key management

**Goal:** the right party controls the keys, and you know the consequence of rotating or revoking them.

## 1. AWS KMS key types
| | Customer managed | AWS managed | AWS owned |
|---|---|---|---|
| Key policy | exclusively controlled by you | controlled by service, viewable by you | controlled and viewable only by the service |
| Lifecycle | you manage rotation, deletion and Region | AWS KMS manages rotation (annual), deletion, Region | service manages them |
| Logging | CloudTrail | CloudTrail | not viewable by you |
| Cost | monthly fee (pro-rated hourly) plus usage | no monthly fee; usage charged | no charge |
- Customer managed keys are recommended when you want full control over lifecycle and usage; AWS owned keys when convenience matters most. Customer managed key rotation is optional; AWS managed key rotation is required yearly (about 365 days).
- AWS managed keys can be used only within the service and by principals in the account; resources encrypted under them cannot be shared with other accounts. AWS managed keys are a legacy type: new services have used AWS owned keys since 2021.
- Services differ in which key types they support; check each service's Encryption at Rest topic.

## 2. BigQuery
- Default: data is encrypted at rest using data encryption keys, which are encrypted with key encryption keys (envelope encryption). With CMEK you control the key encryption keys in Cloud KMS instead of Google.
- All data in BigQuery managed storage supports CMEK; for external data such as Cloud Storage, the external system manages encryption. BigQuery and BigLake tables do not support customer-supplied encryption keys (CSEK).
- A dataset-wide default Cloud KMS key applies to tables created afterwards unless another key is specified. It does not apply to existing tables, and changing it does not modify existing tables. A table's key can be changed with update or cp.
- Feature availability may vary with reservations created under certain BigQuery editions.

## 3. Snowflake Tri-Secret Secure (Business Critical or higher)
- A dual-key model: a Snowflake-maintained key and a customer-managed key (CMK) created on the cloud provider hosting your account form a composite master key that wraps all keys in the account hierarchy (for example table master keys, which derive the file keys that encrypt raw data). The composite key never encrypts raw data directly.
- If the CMK is revoked, Snowflake can no longer decrypt your data; understand your key-safeguarding responsibility before enabling.
- Self-registration flow: create the CMK in the cloud KMS; call SYSTEM$REGISTER_CMK_INFO, SYSTEM$GET_CMK_INFO, SYSTEM$GET_CMK_CONFIG (output is applied as the KMS policy; on Azure pass tenant_id), then SYSTEM$VERIFY_CMK_INFO; finally ask Snowflake Support to enable Tri-Secret Secure for the named account.
- Changing the CMK repeats the registration steps; SYSTEM$GET_CMK_INFO then reports "is being rekeyed".
- Hybrid tables require Dedicated Storage Mode if TSS is or will be enabled.
- AWS external key stores are supported; Snowflake tests and supports only Thales HSM and CipherTrust Cloud Key Manager.

## 4. Column-level encryption and crypto-shredding (BigQuery AEAD)
- AEAD functions encrypt individual values in a table and bind ciphertext to additional authenticated data, verifying integrity and preventing ciphertext substitution.
- Use case from the docs: keep all customers in one table but encrypt each customer's data with a different key, so deleting a key makes its data unreadable (crypto-deletion, or crypto-shredding).
- Keysets hold keys for encryption and decryption (one primary, others secondary) and support key rotation. Envelope encryption functions: KEYS.NEW_WRAPPED_KEYSET, KEYS.ROTATE_WRAPPED_KEYSET, KEYS.REWRAP_KEYSET, KEYS.KEYSET_CHAIN.

## Verify
- [ ] Inventory lists each data store, key type and key owner.
- [ ] Key revocation consequences are agreed, since revoking the CMK makes Snowflake data undecryptable.

## Checked
Method: docs-only read on 2026-11-09 of the AWS KMS concepts page (key types section, first ~100 lines), the Snowflake Tri-Secret Secure page in full, the BigQuery CMEK page (introduction, prerequisites and dataset default section) and the BigQuery AEAD concepts page (introduction through keysets, plus function list). Databricks source dropped (not read). Removed as unstated: TLS and secrets-manager baseline, per-platform table rows for S3/Redshift/Databricks/Azure, separation-of-duties and multi-Region guidance, SQL example, Databricks/Snowflake column functions, deterministic-encryption advice, and the encryption-in-transit tag.
