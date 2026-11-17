---
id: computing-software.data-engineering.apache-hadoop.hdfs-encryption-zones
name: hdfs-encryption-zones
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, encryption, kms, encryption-zones, security]
level: advanced
status: docs-checked
description: "HDFS transparent encryption: zone keys, per-file DEK/EDEK, creating zones with hdfs crypto, rename and trash behaviour, distcp via /.reserved/raw, and key rolling."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/TransparentEncryption.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS encryption zones

An encryption zone is a directory whose contents are transparently encrypted on write and decrypted on read, tied to one encryption zone key. Each file has its own DEK; HDFS handles only the EDEK, stored in the file metadata on the NameNode, and the client asks the Hadoop KMS to decrypt it (the KMS checks the client's access to the zone key version). DataNodes see only encrypted bytes. Zones can nest: a file's EDEK uses the key of the closest ancestor zone. A KMS with a backing key store is a prerequisite.

Setup (the page's example):

```
hadoop key create mykey                       # normal user
hdfs crypto -createZone -keyName mykey -path /zone   # superuser; path must be an empty directory
hdfs crypto -listZones                        # superuser only
hdfs crypto -getFileEncryptionInfo -path /zone/helloWorld
```

Uppercase key names are unsupported. Clients use `hadoop.security.key.provider.path` (the NameNode can return the provider via getServerDefaults). Defaults: `hadoop.security.crypto.cipher.suite` = `AES/CTR/NoPadding` (SM4/CTR/NoPadding is also supported), `hadoop.security.crypto.buffer.size` = 8192, `dfs.namenode.list.encryption.zones.num.responses` = 100. Existing data is encrypted by copying it into a zone, e.g. with distcp.

Renames across zone boundaries (into, out of, or between zones) are refused; renames within one zone, or entirely outside zones, are allowed. Each zone has its own `.Trash` under the zone directory (createZone provisions it). For zones created before Hadoop 2.8.0, run `hdfs crypto -provisionTrash -path /zone`.

DistCp: superusers use the virtual prefix `/.reserved/raw/` to copy without key access and with byte-identical results, and must preserve xattrs with `-px` because the EDEK is exposed as an extended attribute there. When copying into an encrypted location checksums differ (new EDEK), so use `-skipcrccheck -update`.

Key rolling: `hadoop key roll <keyName>` (key admin), then as superuser `hdfs crypto -reencryptZone -start -path <zone>` (or `-cancel`), and watch with `-listReencryptionStatus`. Re-encryption does not apply to snapshots. It is NameNode-only and can load the NameNode; tune `dfs.namenode.reencrypt.batch.size` and the `throttle.limit.handler.ratio` / `updater.ratio` settings. Afterwards `-getFileEncryptionInfo` shows the new ezKeyVersionName, as in the page's example.

## Checked

Method: 2026-11-08 compared against the Transparent Encryption page (apache/hadoop trunk markdown, read in full). Commands, defaults, rename and trash rules and distcp guidance match; added the empty-directory, uppercase-key, throttling and KMS-check details. The verify step is now the page's own double-check example.
