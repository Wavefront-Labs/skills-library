---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-backup-to-cloud-sink
name: filer-backup-to-cloud-sink
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [filer-backup, replication-toml, sink, meta-backup]
level: advanced
status: docs-checked
description: "Continuously back up filer data to S3, GCS, Azure, B2 or a local disk with weed filer.backup, configured via replication.toml; resumable."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Async-Backup
  - https://github.com/seaweedfs/seaweedfs/wiki/Async-Filer-Metadata-Backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer backup to cloud sink

`weed filer.backup` subscribes to filer metadata changes, reads the file content and writes to a sink: AWS S3, Google Cloud Storage, Azure, Backblaze B2 or local disk. It replaced `weed filer.replicate` (no external message queue needed).

Setup:
```bash
weed scaffold -config=replication > replication.toml    # keep only the sink you use, enabled = true
weed filer.backup
```
S3 sink keys include `aws_access_key_id`, `aws_secret_access_key` (empty falls back to the shared credentials file), `region`, `bucket` (must exist) and `directory`.

It runs continuously and retries on errors. Progress (the offset) is stored on the filer, so you can stop and restart freely. Azure sinks can use Entra ID instead of account keys.

SSE: it decrypts SSE-S3 and SSE-KMS objects before upload, so the sink gets plaintext; SSE-KMS needs `[kms]` in `security.toml` or `WEED_KMS_*` variables.

Metadata only: `weed filer.meta.backup` copies metadata changes to another store (LevelDB, RocksDB, MySQL, Postgres, Redis, Cassandra) without running a filer.

Verify: write a file through the filer and confirm it appears in the sink bucket shortly after.

## Checked
Checked 2026-11-09: the sink list, replacement of `weed filer.replicate`, scaffold and run commands, S3 sink keys, continuous retrying with the offset stored on the filer, Entra ID for Azure, the SSE-S3 and SSE-KMS decryption behaviour, and the filer.meta.backup description match both pages. Removed the unsupported full-DR pairing advice.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Async-Backup and Async-Filer-Metadata-Backup, both read in full from a local clone of the wiki.
