---
id: computing-software.database-administration.scylladb.security-encryption-at-rest
name: security-encryption-at-rest
category: computing-software
field: database-administration
product: scylladb
tags: [encryption-at-rest, sstables, commitlog, key-provider, kms, kmip]
level: advanced
status: docs-checked
description: "ScyllaDB encryption at rest: what is encrypted and when, system_info_encryption vs user_info_encryption, table-level scylla_encryption_options, ciphers, key providers."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/encryption-at-rest.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encryption at rest

Encryptable: user tables and the system tables `system.batchlog`, `system.paxos`, `system.dicts` (SSTables), plus commit logs and hints. It can be configured per table.

When: SSTables are immutable, so they are encrypted once, at memtable flush, compaction or `nodetool upgradesstables`. Enabling encryption on an existing table only affects SSTables written afterwards; old SSTables stay as they were until rewritten. Algorithm and key provider are stored in each SSTable `Scylla.db` metadata, so SSTables of one table may use different ciphers, keys or none. Reads fetch the descriptor and key provider from that metadata. Backups work the same for encrypted SSTables.

Configuration:
- System and user data are configured separately in `scylla.yaml`: `system_info_encryption` and `user_info_encryption`.
- User data can also be set per table with `scylla_encryption_options` in the schema. Table options override node defaults and apply on all nodes that write the table, while `scylla.yaml` applies to that node only.

Ciphers (`cipher_algorithm` / `secret_key_strength`): `AES/CBC/PKCS5Padding` (default, 128, 192 or 256, default 128), `AES/ECB/PKCS5Padding` (less secure mode), `Blowfish/CBC/PKCS5Padding` (128; 64-bit block can leak after a few GB under one key). The default AES/CBC 128 is strongly recommended.

`key_provider` values: `LocalFileSystemKeyProviderFactory` (default; key on the same machine as the data, not for production), `ReplicatedKeyProviderFactory` (deprecated), `KmipKeyProviderFactory`, `KmsKeyProviderFactory` (AWS KMS), `GcpKeyProviderFactory`, `AzureKeyProviderFactory`.


## Checked

2026-11-04: encrypted artifacts, when encryption happens, the Scylla.db metadata, scylla.yaml versus table-level options, cipher table and the key provider names confirmed against the ScyllaDB encryption-at-rest documentation page; the backup remark against the backup procedure page. Removed the unsupported closing line about restoring with the same keys.

Method: documentation only; no commands were run.
