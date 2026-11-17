---
id: computing-software.data-engineering.apache-nifi.repository-encryption
name: repository-encryption
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, encryption-at-rest, repositories, keystore, nifi-properties]
level: advanced
status: docs-checked
description: "Encrypt NiFi content, FlowFile and provenance repositories with nifi.repository.encryption.* keys, KEYSTORE key provider, and the per-repository cipher and class names."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repository encryption

Setting `nifi.repository.encryption.protocol.version=1` enables encryption for all repositories (absent disables it). Also set:
- `nifi.repository.encryption.key.id` (example `primary-key`)
- `nifi.repository.encryption.key.provider=KEYSTORE`
- `nifi.repository.encryption.key.provider.keystore.location` (example `conf/repository.p12`)
- `nifi.repository.encryption.key.provider.keystore.password` (use a placeholder; the same password must open the store and each key entry; KeyStore types PKCS12 `.p12` and BCFKS `.bcfks`)

Implementations and ciphers:
| Repository | Cipher | Class |
|---|---|---|
| Content | AES/CTR/NoPadding | `org.apache.nifi.content.EncryptedFileSystemRepository` |
| FlowFile | AES/GCM/NoPadding | `org.apache.nifi.wali.EncryptedSequentialAccessWriteAheadLog` |
| Swap | AES/GCM/NoPadding | `org.apache.nifi.controller.EncryptedFileSystemSwapManager` |
| Provenance | AES/GCM/NoPadding | `org.apache.nifi.provenance.EncryptedWriteAheadProvenanceRepository` |

Verify: the repository implementation properties reference the Encrypted classes and NiFi starts and processes data.

## Checked

Checked against the NiFi Administration Guide, Repository Encryption sections and system properties: protocol version 1, the four key properties, KEYSTORE as the only provider, the ciphers and the four class names match. Removed the unsupported "protect with encrypt-config" advice and added the keystore type and password rules from the property table.

Method: docs-only read of cited pages, 2026-11-08
