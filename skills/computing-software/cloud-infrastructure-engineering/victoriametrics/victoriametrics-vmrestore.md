---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmrestore
name: victoriametrics-vmrestore
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmrestore, restore, disaster-recovery, backup, resume]
level: practitioner
status: docs-checked
description: "Restore a VictoriaMetrics backup with vmrestore, including source URLs, resume behaviour and bandwidth flags."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmrestore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmrestore

Steps:
1. Stop VictoriaMetrics; it must not run during a restore.
2. Run vmrestore:

```text
./vmrestore -src=<storageType>://<path/to/backup> -storageDataPath=<local/path/to/restore>
```

3. Start VictoriaMetrics with `-storageDataPath` pointing at the restored folder.

`-src` can be `gs://<bucket>/<path>`, `s3://<bucket>/<path>`, `azblob://<container>/<path>`, S3-compatible storage with `-customS3Endpoint` (and only the bucket in `-src`), or `fs:///absolute/path`. The default `-storageDataPath` is `victoria-metrics-data`.

Existing files in `-storageDataPath` are replaced so the result matches the backup, similar to `rsync --delete`.

Interrupted restores resume when you rerun the same command. With preallocation (v1.139.0+) it resumes from the last complete file; with `-skipFilePreallocation` it resumes at the exact point.

Flags: `-concurrency` (default 10), `-maxBytesPerSecond` (default 0, unlimited), `-skipBackupCompleteCheck` (for backups made before the backup-complete marker file existed), `-credsFilePath`, `-configFilePath`, `-configProfile`, `-customS3Endpoint`, `-s3ForcePathStyle`, `-s3TLSInsecureSkipVerify`, `-deleteAllObjectVersions`.

The page gives no cluster-specific restore steps, so check the cluster documentation before restoring a cluster. Stop VictoriaMetrics before running vmrestore against its data directory.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
