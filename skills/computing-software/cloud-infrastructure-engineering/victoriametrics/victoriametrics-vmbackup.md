---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmbackup
name: victoriametrics-vmbackup
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmbackup, backup, snapshot, incremental-backup, s3, gcs, azure-blob, server-side-copy]
level: practitioner
status: docs-checked
description: "Back up VictoriaMetrics from snapshots with vmbackup: full, incremental and smart hourly plus daily schemes to GCS, S3, Azure or filesystem."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmbackup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmbackup

vmbackup builds backups from instant snapshots for single-node and cluster, without stopping VictoriaMetrics.

```text
./vmbackup -storageDataPath=/path/to/data -snapshot.createURL=http://localhost:8428/snapshot/create -dst=gs://<bucket>/<path>
```

`-storageDataPath` must match VictoriaMetrics. `-snapshot.createURL` creates and later deletes the snapshot. For a cluster run vmbackup on every vmstorage node (port 8482), each with its own `-dst`; in Kubernetes use a sidecar. Backups of single-node cannot be restored into a cluster or the reverse.

Destinations: `gs://`, `s3://`, `azblob://`, S3-compatible storage (MinIO, Ceph) and `fs:///absolute/path` (not inside `-storageDataPath`).

Backup types: full; full with server-side copy (`-origin=gs://<bucket>/<existing-backup>`); incremental (point `-dst` at an existing backup and only new data uploads). The recommended smart scheme is hourly `-dst=.../latest` plus a daily `-origin=.../latest -dst=.../<YYYYMMDD>` server-side copy; do not run the hourly job while the daily one runs. Glacier-style classes make server-side copy slow and costly.

How it works: create snapshot, compare snapshot, `-dst` and `-origin`, delete stale files in `-dst`, server-side copy shared files, upload the rest in 1 GiB chunks, delete the snapshot.

Credentials: `-credsFilePath`; Azure uses `AZURE_STORAGE_ACCOUNT_NAME` and `AZURE_STORAGE_ACCOUNT_KEY`. MinIO: `-customS3Endpoint=http://localhost:9000` with only the bucket in `-dst`.

Tuning: `-concurrency` (default 10), `-maxBytesPerSecond`, `-filestream.disableFadvise`, `-snapshotName`, `-s3StorageClass`, `-deleteAllObjectVersions`. vmbackup does not manage retention; delete old backups yourself or use the enterprise vmbackupmanager. Interrupted runs resume when rerun with the same arguments.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
