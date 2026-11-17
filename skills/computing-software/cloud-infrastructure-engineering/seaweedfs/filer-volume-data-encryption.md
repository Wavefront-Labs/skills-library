---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-volume-data-encryption
name: filer-volume-data-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [encryptvolumedata, gdpr, aes256-gcm, encryption]
level: practitioner
status: docs-checked
description: "Encrypt file chunks at rest on volume servers with weed filer -encryptVolumeData: per-chunk AES-256-GCM keys held in filer store metadata."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Data-Encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer volume data encryption

```bash
weed filer -encryptVolumeData
```
Keys are randomly generated at write time, one 256-bit cipher key per file chunk, used with AES256-GCM, so different files have different keys. The keys are stored as metadata in the filer store. Volume servers have no concept of encryption: they treat encrypted blocks like any other and never see unencrypted data, in storage or in transmission, so the page says volume servers can be placed anywhere.

Consequences:
- As long as the filer store is not exposed, it is nearly impossible to guess the keys for all files; protect the filer store.
- Forgetting data (the page's GDPR example) is possible by deleting the metadata, even if volume data sits on glacial storage and is cumbersome to dig out.
- The page motivates the option by volumes that may be tiered to the cloud, or volume servers that may be hacked.

## Checked

2026-11-08. Confirmed against the Filer Data Encryption wiki page. Removed the unsupported claims about Cloud Tier and Cloud Drive mounts, the S3 SSE comparison and the raw chunk read check.

Method: documentation only; no commands were run.
