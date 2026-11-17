---
id: computing-software.cloud-infrastructure-engineering.velero.parallel-upload-concurrency
name: parallel-upload-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [parallel-files-upload, parallel-blocks-upload, gomaxprocs, uploaderconfig, kopia]
level: advanced
status: docs-checked
description: "Tune per-volume upload concurrency with --parallel-files-upload and --parallel-blocks-upload, their defaults, scope and memory trade-off."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two backup flags set upload concurrency inside each volume backup.

`--parallel-files-upload` applies to file-system backup and to CSI snapshot data movement with the file system mover (`velero-fs`), which uses Kopia:

```bash
velero backup create fs-backup --default-volumes-to-fs-backup --parallel-files-upload=8
velero backup create fs-snapshot-backup --snapshot-move-data --data-mover=velero-fs --parallel-files-upload=8
```

`--parallel-blocks-upload` applies to the block data mover (`velero-block`):

```bash
velero backup create block-backup --snapshot-move-data --data-mover=velero-block --parallel-blocks-upload=8
```

Defaults: omitted or `0` means `runtime.GOMAXPROCS(0)` in the data mover process when backup processing starts. That can reflect the pod CPU limit rather than the node CPU count. An explicit positive value overrides it, even above GOMAXPROCS.

Scope:
- Per volume uploader, not per backup.
- They do not set the number of concurrent data mover pods; that is node-agent concurrency.
- Backups only. File restore uses `--parallel-files-download`; neither flag changes block restore.

Higher values can raise throughput if CPU, disk and backup storage keep up, but increase buffered data and memory; slow storage leaves more packs buffered. Both flags also exist on `velero schedule create`. In YAML use `spec.uploaderConfig.parallelFilesUpload` and `parallelBlocksUpload` (under `spec.template.uploaderConfig` on a Schedule). There is no global setting.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/backup-reference/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
